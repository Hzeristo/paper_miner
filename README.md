<h1> 🧬 Project Chimera: The PaperMiner Subsystem</h1>

An asynchronous, crash-tolerant, academically ruthless automated guillotine for papers.

## The Philosophy

Project Chimera is a human-AI symbiotic exocortex preprocessor built to cut noise before cognition.

- **State is Location**: paper lifecycle is encoded by filesystem movement, not by a fragile centralized database.
- **Human in the loop**: LLM makes high-dimensional judgments, but only humans are the final valve for what enters the Vault.
- **Asynchronous by design**: each stage can be rerun independently, resumed after interruption, and audited as files.

## Pipeline Architecture

Core flow (v1.0):

1. **Arxiv Fetcher (获取猎物)**
   - Pull candidate PDFs from arXiv into local inbox directories.
2. **MinerU (物理剥离)**
   - Convert PDF to markdown and strip paper text from binary format.
3. **Filter Engine (LLM 毒舌初筛)**
   - Run first-pass triage (e.g. Reject / Skim / MustRead) with structured outputs.
4. **Paper Router & Vault Writer (打扫战场与写入 Obsidian)**
   - Route files by verdict and write normalized markdown artifacts into the Vault pipeline.

Text pipeline:

`Arxiv Fetcher -> MinerU -> Filter Engine -> Paper Router & Vault Writer`

## Installation & Configuration

### 1) Conda environment

Create and activate a dedicated environment first.

```bash
conda create -n chimera python=3.12 -y
conda activate chimera
pip install -r requirements.txt
```

### 2) 12-Factor App configuration

Use exactly three configuration channels:

- **API Keys -> OS environment variables**
  - Set keys such as `DEEPSEEK_API_KEY`, `OPENAI_API_KEY`, `GEMINI_API_KEY` in your system environment.
- **Telegram token/chat id -> `.env`**
  - Put `TG_BOT_TOKEN` and `TG_CHAT_ID` in `.env` (project root).
- **All paths and runtime knobs -> `config.yaml`**
  - Use `config.yaml` for directories, query settings, and path topology.
  - Keep layout aligned with `config.example.yaml` (if absent in your clone, create it from current `config.yaml` as baseline).

Configuration precedence in runtime is:

`Environment Variables > .env > config.yaml`

This design keeps secrets out of versioned config while preserving reproducible path topology.

## Operation Commands

### Debug

Run a single markdown evaluation target:

```bash
python scripts/evaluate_md.py -i <path>
```

### Daily Cronjob

Run the full daily workflow:

```bash
python scripts/run_daily.py
```

This command is designed to be mounted on OS scheduler infrastructure:

- Windows: **Task Scheduler**
- Linux/macOS: **crontab**

## Practical Notes for Operators

- Keep each stage idempotent: reruns should be safe and predictable.
- Prefer absolute or repo-root-relative paths in `config.yaml`.
- Treat `inbox/`, processed markdown directories, and filtered output as observable state machine nodes.
- Do not bypass human review when writing final knowledge nodes into Obsidian.

