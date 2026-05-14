# Lessons Learned — ATTICUS Training

This document captures dependency conflicts, environment bugs, and hard-won fixes
encountered during ATTICUS training runs. Read this before you start.

For issues common to all Ronin 48 models (RunPod environment, bitsandbytes, torchvision,
QLoRA dependency conflicts), see [ABBY's LESSONS_LEARNED.md](https://codeberg.org/Ronin48/ABBY/raw/branch/main/LESSONS_LEARNED.md) —
it has the most complete record of the first training run.

---

## ATTICUS-Specific Notes

### Training Monitor Blind Spot — Read Before Launching

The training monitor has a failure mode where it silently misses crashes that happen before
the GPU ever activates (disk full, bad import, OOM during model load). It reports
`GPU 0% | active=False` and assumes the pod is still initializing. This burned credits
and wasted time across multiple training runs before it was fixed.

The monitor now has pre-flight checks (volume size, HF cache mount, free space) and a
stuck-pod alert (Telegram after 45 min with no GPU activity). But verify your volume size
before launching — the pre-flight check is the first line of defense.

See [ABBY Error #20](https://codeberg.org/Ronin48/ABBY/raw/branch/main/LESSONS_LEARNED.md)
for the full incident writeup and fix details.

**Rule: `GPU 0% | active=False` after 20+ minutes = crashed. SSH in and check `/workspace/logs/train.log`.**

---

## Contributing

If you hit a new error and fix it, please add it here. The people walking behind
you will thank you.
