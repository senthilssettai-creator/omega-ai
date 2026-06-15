from pathlib import Path
from typing import Any

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

from ..config import Settings

class BrowserAgent:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.snapshot_dir = Path("./browser_snapshots")
        self.snapshot_dir.mkdir(parents=True, exist_ok=True)

    def visit(self, url: str) -> str:
        try:
            with sync_playwright() as playwright:
                browser = playwright.chromium.launch(headless=self.settings.playwright_headless)
                page = browser.new_page()
                page.goto(url, wait_until="domcontentloaded", timeout=30000)
                title = page.title()
                file_path = self._save_snapshot(page, url)
                browser.close()
            return f"Visited {url} with title '{title}'. Snapshot saved to {file_path}."
        except PlaywrightTimeoutError as exc:
            return f"Timeout while visiting {url}: {exc}"

    def fill_form(self, url: str, field_map: dict[str, str], submit_selector: str | None = None) -> str:
        try:
            with sync_playwright() as playwright:
                browser = playwright.chromium.launch(headless=self.settings.playwright_headless)
                page = browser.new_page()
                page.goto(url, wait_until="domcontentloaded", timeout=30000)
                for selector, value in field_map.items():
                    page.fill(selector, value)
                if submit_selector:
                    page.click(submit_selector)
                else:
                    page.evaluate("() => document.querySelector('form')?.submit()")
                file_path = self._save_snapshot(page, url)
                browser.close()
            return f"Filled form at {url}. Snapshot saved to {file_path}."
        except PlaywrightTimeoutError as exc:
            return f"Timeout while filling form at {url}: {exc}"

    def extract_text(self, url: str, selector: str) -> str:
        try:
            with sync_playwright() as playwright:
                browser = playwright.chromium.launch(headless=self.settings.playwright_headless)
                page = browser.new_page()
                page.goto(url, wait_until="domcontentloaded", timeout=30000)
                element = page.query_selector(selector)
                text = element.inner_text().strip() if element else ""
                browser.close()
            return text
        except PlaywrightTimeoutError as exc:
            return f"Timeout while extracting text from {url}: {exc}"

    def _save_snapshot(self, page: Any, url: str) -> str:
        sanitized = url.replace("https://", "").replace("http://", "").replace("/", "_")
        path = self.snapshot_dir / f"{sanitized}.html"
        path.write_text(page.content(), encoding="utf-8")
        return str(path)
