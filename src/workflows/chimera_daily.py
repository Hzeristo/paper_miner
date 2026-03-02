"""Top-level facade workflow for daily Chimera execution."""

from __future__ import annotations

import html
import logging
from typing import Any

from src.core.config import Settings
from src.io_adapter.telegram_notifier import TelegramNotifier
from src.llm_gateway.prompt_manager import PromptManager
from src.workflows.batch_filter import run_batch_filter
from src.workflows.fetch_arxiv import run_arxiv_fetch
from src.workflows.ingest_pdfs import run_pdf_ingestion

logger = logging.getLogger(__name__)


def run_daily_pipeline() -> None:
    """Run ingestion, triage, and summary notification in one pipeline."""
    logger.info("=== Chimera Daily Pipeline Started ===")
    settings = Settings()

    # Step 0: Arxiv Fetching
    input_dir = settings.arxivpdf_dir or (settings.project_root / "papers" / "arxivpdf")
    new_pdfs_count = run_arxiv_fetch(target_dir=input_dir)
    logger.info("Arxiv fetching completed. new_pdfs_count=%s", new_pdfs_count)

    # Stage 1: Ingestion
    raw_output_dir = settings.md_papers_raw_dir or (
        settings.project_root / "papers" / "md_papers_raw"
    )
    clean_dir = settings.md_papers_dir or (
        settings.project_root / "papers" / "md_papers"
    )
    ingested_count = run_pdf_ingestion(
        input_dir=input_dir,
        output_dir=raw_output_dir,
        clean_dir=clean_dir,
    )
    logger.info("Ingestion completed. success_count=%s", ingested_count)

    # Stage 2: Triage
    stats = run_batch_filter(md_papers_dir=clean_dir)
    logger.info("Triage completed. stats=%s", stats)

    # Stage 3: Notification
    prompt_manager = PromptManager()
    report_message = _render_daily_report(
        prompt_manager=prompt_manager,
        stats=stats,
        new_pdfs_count=new_pdfs_count,
    )
    notifier = TelegramNotifier(settings=settings)
    notifier.send_summary(html_message=report_message)


def _render_daily_report(
    prompt_manager: PromptManager,
    stats: dict[str, Any],
    new_pdfs_count: int,
) -> str:
    """Render Telegram-safe HTML summary from external template."""
    total = int(stats.get("total", 0))
    must_read = int(stats.get("must_read", 0))
    reject = int(stats.get("reject", 0))

    items_raw = stats.get("must_read_items", [])
    must_read_items: list[dict[str, Any]] = []
    if isinstance(items_raw, list):
        for item in items_raw:
            if not isinstance(item, dict):
                continue
            score = item.get("score", 0)
            title = item.get("title", "")
            novelty = item.get("novelty", "")
            must_read_items.append(
                {
                    "score": int(score) if isinstance(score, (int, float, str)) else 0,
                    "title": html.escape(str(title), quote=False),
                    "novelty": html.escape(str(novelty), quote=False),
                }
            )

    # Backward compatible fallback when only must_read_titles exists.
    if not must_read_items:
        titles_raw = stats.get("must_read_titles", [])
        if isinstance(titles_raw, list):
            must_read_items = [
                {
                    "score": 0,
                    "title": html.escape(str(title), quote=False),
                    "novelty": "N/A",
                }
                for title in titles_raw
            ]

    return prompt_manager.render(
        "tasks/daily_summary_telegram_html.j2",
        new_pdfs_count=int(new_pdfs_count),
        total=total,
        must_read=must_read,
        reject=reject,
        must_read_items=must_read_items,
    )
