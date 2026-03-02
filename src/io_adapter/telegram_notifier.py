"""Telegram notification adapter for daily summaries."""

from __future__ import annotations

import logging
from urllib import parse, request

from src.core.config import Settings

logger = logging.getLogger(__name__)


class TelegramNotifier:
    """Best-effort Telegram sender. Failures never break workflow exit."""

    def __init__(self, settings: Settings) -> None:
        self._bot_token = (
            settings.tg_bot_token.get_secret_value()
            if settings.tg_bot_token is not None
            else None
        )
        self._chat_id = (
            settings.tg_chat_id.get_secret_value()
            if settings.tg_chat_id is not None
            else None
        )
        if not self._bot_token or not self._chat_id:
            logger.warning(
                "Telegram bot token/chat id missing; notification will be skipped."
            )

    def send_summary(self, html_message: str) -> None:
        """Send HTML summary to Telegram in a non-critical path."""
        try:
            if not self._bot_token or not self._chat_id:
                return

            api_url = f"https://api.telegram.org/bot{self._bot_token}/sendMessage"
            payload = parse.urlencode(
                {
                    "chat_id": self._chat_id,
                    "text": html_message,
                    "parse_mode": "HTML",
                }
            ).encode("utf-8")
            req = request.Request(
                api_url,
                data=payload,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                method="POST",
            )
            with request.urlopen(req, timeout=10) as response:
                status_code = getattr(response, "status", None)
                if status_code is not None and status_code >= 400:
                    logger.error(
                        "Telegram sendMessage returned HTTP status %s", status_code
                    )
        except Exception as exc:
            logger.error("Failed to send Telegram summary notification: %s", exc)
