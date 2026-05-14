#!/usr/bin/env python3
"""ATTICUS QLoRA Fine-tuning Script. Requires A100-80GB or equivalent."""

import argparse
from pathlib import Path

import torch
import yaml
from datasets import load_dataset
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
)
from trl import SFTConfig, SFTTrainer


def load_config(path: str) -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def setup_model(config: dict):
    model_name = config["model"]["name"]
    q = config["quantization"]
    lora_cfg = config["lora"]

    bnb_config = BitsAndBytesConfig(
        load_in_4bit=q["load_in_4bit"],
        bnb_4bit_compute_dtype=getattr(torch, q["bnb_4bit_compute_dtype"]),
        bnb_4bit_quant_type=q["bnb_4bit_quant_type"],
        bnb_4bit_use_double_quant=q["bnb_4bit_use_double_quant"],
    )

    print(f"Loading {model_name}")
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        quantization_config=bnb_config,
        attn_implementation=config["model"].get("attn_implementation", "eager"),
        trust_remote_code=True,
    )

    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    model = prepare_model_for_kbit_training(model, use_gradient_checkpointing=True)
    model = get_peft_model(model, LoraConfig(
        r=lora_cfg["r"],
        lora_alpha=lora_cfg["lora_alpha"],
        lora_dropout=lora_cfg["lora_dropout"],
        target_modules=lora_cfg["target_modules"],
        task_type=lora_cfg["task_type"],
        bias=lora_cfg["bias"],
    ))
    model.print_trainable_parameters()
    return model, tokenizer


def main():
    parser = argparse.ArgumentParser(description="ATTICUS QLoRA Training")
    parser.add_argument("--config", default="configs/training_config.yaml")
    args = parser.parse_args()

    config = load_config(args.config)
    model, tokenizer = setup_model(config)

    tc = config["training"]
    dc = config["data"]

    train_ds = load_dataset("json", data_files=dc["train_file"], split="train")
    eval_ds = load_dataset("json", data_files=dc["eval_file"], split="train") if dc.get("eval_file") else None
    print(f"Train: {len(train_ds)} | Eval: {len(eval_ds) if eval_ds else 0}")

    training_args = SFTConfig(
        max_seq_length=dc.get("max_seq_length", 4096),
        output_dir=tc["output_dir"],
        num_train_epochs=tc["num_train_epochs"],
        per_device_train_batch_size=tc["per_device_train_batch_size"],
        per_device_eval_batch_size=tc.get("per_device_eval_batch_size", 2),
        gradient_accumulation_steps=tc["gradient_accumulation_steps"],
        learning_rate=tc["learning_rate"],
        weight_decay=tc.get("weight_decay", 0.01),
        warmup_ratio=tc.get("warmup_ratio", 0.05),
        lr_scheduler_type=tc.get("lr_scheduler_type", "cosine"),
        logging_steps=tc.get("logging_steps", 10),
        save_steps=tc.get("save_steps", 200),
        eval_steps=tc.get("eval_steps", 200),
        eval_strategy=tc.get("eval_strategy", "steps"),
        save_total_limit=tc.get("save_total_limit", 3),
        bf16=tc.get("bf16", True),
        gradient_checkpointing=tc.get("gradient_checkpointing", True),
        max_grad_norm=tc.get("max_grad_norm", 1.0),
        group_by_length=tc.get("group_by_length", True),
        dataloader_num_workers=tc.get("dataloader_num_workers", 4),
        report_to=tc.get("report_to", "none"),
        seed=config.get("seed", 42),
    )

    trainer = SFTTrainer(
        model=model,
        processing_class=tokenizer,
        args=training_args,
        train_dataset=train_ds,
        eval_dataset=eval_ds,
    )

    print("Starting ATTICUS training...")
    trainer.train()

    final_path = Path(tc["output_dir"]) / "final"
    trainer.save_model(str(final_path))
    tokenizer.save_pretrained(str(final_path))
    print(f"Saved to {final_path}")


if __name__ == "__main__":
    main()
