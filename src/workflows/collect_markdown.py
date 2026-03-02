"""Workflow for promoting one raw MinerU folder into a clean markdown paper."""

from __future__ import annotations

import logging
from pathlib import Path

from src.core.config import Settings
from src.core.paper import Paper
from src.io_adapter.paper_loader import PaperLoader

logger = logging.getLogger(__name__)


def _normalize_against_project(path: Path, settings: Settings) -> Path:
    """Normalize paths against project root to avoid CWD-dependent behavior."""
    expanded = path.expanduser()
    if expanded.is_absolute():
        return expanded.resolve()
    return (settings.project_root / expanded).resolve()


def run_collect_paper(
    raw_paper_dir: Path,
    clean_dir: Path | None = None,
    paper_stem: str | None = None,
) -> tuple[Path, Paper]:
    """Promote one raw paper folder and materialize it into a typed Paper model."""
    settings = Settings()
    loader = PaperLoader()

    normalized_raw = _normalize_against_project(raw_paper_dir, settings)
    target_clean_dir = clean_dir or (settings.project_root / "papers" / "md_papers")
    normalized_clean = _normalize_against_project(target_clean_dir, settings)
    final_stem = paper_stem.strip() if paper_stem else normalized_raw.name

    if not normalized_raw.exists() or not normalized_raw.is_dir():
        raise FileNotFoundError(f"Raw paper directory does not exist: {normalized_raw}")
    if not final_stem:
        raise ValueError("paper_stem cannot be empty after normalization.")
    if normalized_clean.exists() and not normalized_clean.is_dir():
        raise ValueError(
            f"clean_dir must be a directory path, got file: {normalized_clean}"
        )

    clean_md = loader.extract_and_clean(
        raw_paper_dir=normalized_raw,
        clean_dir=normalized_clean,
        paper_stem=final_stem,
    )
    paper = loader.load_paper(clean_md)
    logger.info(
        "Collect workflow completed. clean_md=%s paper_id=%s", clean_md, paper.id
    )
    return clean_md, paper
