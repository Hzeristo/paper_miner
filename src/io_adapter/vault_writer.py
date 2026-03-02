"""Vault writer for persisting knowledge nodes into Obsidian inbox."""

from __future__ import annotations

import logging
import re
from pathlib import Path

from src.core.config import Settings
from src.core.paper import Paper
from src.core.verdict import PaperAnalysisResult
from src.llm_gateway.prompt_manager import PromptManager

logger = logging.getLogger(__name__)

_ILLEGAL_FILENAME_CHARS = r'[\\/:*?"<>|]'
_MAX_BASENAME_LENGTH = 100


class VaultWriter:
    """Render and persist paper knowledge nodes as markdown files."""

    def __init__(self, settings: Settings, prompt_manager: PromptManager) -> None:
        if settings.vault_root is None:
            raise ValueError("`vault_root` is required to initialize VaultWriter.")

        self.vault_inbox_dir: Path = settings.vault_root / "inbox"
        self.prompt_manager = prompt_manager
        self.vault_inbox_dir.mkdir(parents=True, exist_ok=True)

    def write_knowledge_node(self, paper: Paper, analysis: PaperAnalysisResult) -> Path:
        """Render `knowledge_node.j2` and write it to Obsidian inbox."""
        rendered = self.prompt_manager.render(
            "templates/knowledge_node.j2",
            paper=paper,
            analysis=analysis,
        )
        safe_basename = self._sanitize_filename(paper.title)
        output_path = self.vault_inbox_dir / f"{safe_basename}.md"
        output_path.write_text(rendered, encoding="utf-8")
        logger.info("Knowledge node written to: %s", output_path)
        return output_path

    @staticmethod
    def _sanitize_filename(title: str) -> str:
        """Convert a paper title into a cross-platform-safe markdown filename."""
        normalized = re.sub(_ILLEGAL_FILENAME_CHARS, "_", title).strip()
        normalized = re.sub(r"\s+", " ", normalized)
        if not normalized:
            normalized = "untitled_paper"
        return normalized[:_MAX_BASENAME_LENGTH].rstrip(" .")
