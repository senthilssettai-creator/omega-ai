from pathlib import Path
from typing import Optional

from playwright.sync_api import sync_playwright
from ..config import Settings

class BrowserAgent:
    def __init__(self, settings: Settings):
        self.settings = settings

    def visit(self, url: str) -> str:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=self.settings.playwright_headless)
            page = browser.new_page()
            page.goto(url, wait_until="domcontentloaded", timeout=30000)
            title = page.title()
            snapshot = self._save_snapshot(page, url)
            browser.close()
        return f"Visited {url} with title '{title}'. Snapshot: {snapshot}"

    def _save_snapshot(self, page, url: str) -> str:
        sanitized = url.replace("https://", "").replace("http://", "").replace("/", "_")
        path = Path(f"browser_snapshots/{sanitized}.html")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(page.content(), encoding="utf-8")
        return str(path)

    def fill_form(self, url: str, field_map: dict[str, str]) -> str:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(headless=self.settings.playwright_headless)
            page = browser.new_page()
            page.goto(url, wait_until="domcontentloaded", timeout=30000)
            for selector, value in field_map.items():
                page.fill(selector, value)
            page.evaluate("() => document.querySelector('form')?.submit()")
            browser.close()
        return f"Filled form at {url} and submitted."