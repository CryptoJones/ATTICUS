# ATTICUS — Limitations, Scope, and Use Guidance

Read this before deploying ATTICUS in any operational context.

---

## What ATTICUS Does

Given a case description, ATTICUS identifies potential constitutional violations, evidentiary weaknesses, defense strategy considerations, and applicable case law relevant to criminal defense analysis.

## What ATTICUS Does Not Do

- **ATTICUS is not a licensed attorney.** Its outputs do not constitute legal advice and do not create an attorney-client relationship.
- **ATTICUS cannot read the record.** It works from the facts you provide. It has no access to police reports, discovery, transcripts, or physical evidence.
- **ATTICUS does not know your jurisdiction.** Constitutional law varies by federal circuit, state court of appeals, and individual judge. Outputs reflect general principles unless you specify jurisdiction.
- **ATTICUS has a training data cutoff.** Recent Supreme Court decisions, new circuit precedents, and legislative changes may not be reflected.
- **ATTICUS can hallucinate case citations.** Every case name, citation, and holding must be verified in Westlaw, Lexis, or a primary source before being used in any filing. Do not cite cases from ATTICUS output without verifying them.
- **ATTICUS does not know your client.** Individualized advice based on a specific client's history, prior record, and circumstances requires attorney judgment.
- **ATTICUS cannot replace voir dire, negotiation, or courtroom judgment.** It is a research and analysis tool, not a litigator.

---

## Scope of Practice

ATTICUS is designed to assist licensed attorneys and supervised law students in:

- Identifying potential Fourth, Fifth, Sixth, and Fourteenth Amendment violations
- Analyzing evidentiary weaknesses in the prosecution's case
- Surfacing defense strategy considerations for case review
- Constitutional case law research (subject to verification)
- Training and scenario-based learning for law students and public defender offices

**ATTICUS outputs must be reviewed and verified by a licensed attorney before use in any filing, motion, or client communication.**

---

## For Public Defender Offices Considering Deployment

Before deploying ATTICUS:

- Have supervising attorneys audit outputs against current circuit precedent for your jurisdiction
- Establish a written policy requiring attorney review of all ATTICUS outputs before they are used
- Brief all users on the hallucination risk for case citations — this is the highest-risk failure mode
- Do not allow law students or paralegals to use ATTICUS outputs without attorney review
- Establish a feedback loop so attorneys can flag incorrect outputs for future training improvement

---

## Known Limitations

| Area | Limitation |
|------|-----------|
| Citation accuracy | High hallucination risk — always verify every citation |
| Jurisdiction specificity | Circuit and state-specific precedent may not be distinguished without prompting |
| Currency | Training data cutoff; recent decisions not included |
| Client-specific factors | Prior record, plea history, and individual circumstances not modeled |
| Sentencing | Guideline calculations, departures, and variances require qualified analysis |
| Training size | Fine-tuned on a small dataset; unusual charges and novel legal theories may degrade performance |

---

## A Note on Citation Verification

ATTICUS, like all large language models, can generate case citations that do not exist or that misstate a holding. **This is the single most dangerous failure mode for legal use.**

Before using any case cited by ATTICUS:

1. Verify the case exists in Westlaw or Lexis
2. Verify the citation is correct
3. Verify the holding matches what ATTICUS stated
4. Verify the case has not been overruled or distinguished

No citation from ATTICUS should ever appear in a filing without this verification.

---

## Version and Training Data

| Field | Value |
|-------|-------|
| Base model | meta-llama/Llama-3.3-70B-Instruct |
| Fine-tune method | QLoRA (4-bit) |
| Adapter | [Ronin48LLC/atticus-lora-adapter](https://huggingface.co/Ronin48LLC/atticus-lora-adapter) |
| Training date | May 2026 |
| Training data cutoff | See base model documentation |

---

## Reporting Errors

If ATTICUS produces legally incorrect, misleading, or potentially harmful output:

- **GitHub:** [CryptoJones/ATTICUS/issues](https://github.com/CryptoJones/ATTICUS/issues)
- **Codeberg:** [Ronin48/ATTICUS/issues](https://codeberg.org/Ronin48/ATTICUS/issues)

Include the input, the output, and the correct legal answer with a citation to authority.
