# playwright_parallel_slot_watcher.py
"""
Parallel slot watcher with:
 - infinite retries until slot appears (or until you stop)
 - logging to file + console
 - screenshot capture on success/error/timeout
 - CPU/RAM optimizations: reuse browser + concurrency limit
 - auto-restart stuck sessions with watchdog
 - FIXED success URL capture + GUI restore correctness
"""

import asyncio
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional, Union

from playwright.async_api import async_playwright, Page, Browser, Error as PlaywrightError

# ---------------------------
# CONFIGURATION
# ---------------------------
START_URL = "https://www.goethe.de/ins/in/en/spr/prf/gzb2.cfm?examId=5F0ECCDAD6DAF286DCD85E927E980A007AD2D729EB97AEB101AC05F9D79098F88FCDEA998D10794BDAECAFD703DE4980EBADDBC3538C549CA62C8617CC83CFE6"
NUM_SESSIONS = 10
CONCURRENCY_LIMIT = 8
REUSE_BROWSER = True
GUI_DISPLAY_SECONDS = 200
SESSION_TIMEOUT = 50
MAX_RESTARTS = 5
STOP_ON_FIRST_SUCCESS = True

SCREENSHOT_DIR = Path("screenshots")
LOG_DIR = Path("logs")

SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------
# LOGGING
# ---------------------------
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_file = LOG_DIR / f"slot_watcher_{timestamp}.log"

logger = logging.getLogger("slot_watcher")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)

fh = logging.FileHandler(log_file)
fh.setFormatter(formatter)
logger.addHandler(fh)


def screenshot_path(session_id: int, tag: str) -> Path:
    return SCREENSHOT_DIR / f"sess{session_id:03d}_{tag}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"


# ---------------------------
# CORE SESSION LOGIC
# ---------------------------
class SlotSession:
    def __init__(self, session_id: int, start_url: str, gui_display_seconds: int = 20):
        self.session_id = session_id
        self.start_url = start_url
        self.gui_display_seconds = gui_display_seconds
        self._attempts = 0
        self.result: Optional[str] = None

    # ---------------------------
    # COOKIE HANDLER
    # ---------------------------
    async def handle_cookie_consent(self, page: Page):
        selectors = [
            "button:has-text('Accept All')",
            "button:has-text('ACCEPT ALL')",
            "text=/accept all/i",
            "[data-testid*='accept']",
            "button[class*='accept']",
            "//button[contains(., 'Accept')]",
            "text=/accept/i"
        ]
        for selector in selectors:
            try:
                btn = page.locator(selector)
                if await btn.count() > 0:
                    await btn.first.click(timeout=3000)
                    logger.info(f"[{self.session_id}] Cookie accepted using {selector}")
                    await asyncio.sleep(0.5)
                    return True
            except:
                pass
        return False

    # ---------------------------
    # ERROR CHECKER
    # ---------------------------
    async def check_errors(self, page: Page):
        try:
            if await page.locator("text=/high demand|cannot be booked/i").first.count():
                return "high_demand"
            if await page.locator("text=/finish other started bookings/i").first.count():
                return "finish_other"
            return None
        except:
            return None

    # ---------------------------
    # CLICK "SELECT MODULES"
    # ---------------------------
    async def find_and_click_select_modules(self, page: Page, max_retries: int = 25) -> bool:
        selectors = [
            "text=Select modules",
            "button:has-text('Select modules')",
            "text=/select modules/i"
        ]
        for attempt in range(1, max_retries + 1):
            for s in selectors:
                try:
                    await page.click(s, timeout=2000)
                    await asyncio.sleep(0.5)
                    logger.info(f"[{self.session_id}] Clicked Select modules ({s}) [Attempt {attempt}]")
                    return True
                except:
                    pass

            # Retry logic
            logger.info(f"[{self.session_id}] Button not found. Clearing cookies + reloading...")
            await page.context.clear_cookies()
            try:
                await page.goto(self.start_url, wait_until="domcontentloaded", timeout=60000)
                await asyncio.sleep(1)
                await self.handle_cookie_consent(page)
            except Exception as e:
                logger.warning(f"[{self.session_id}] Reload error: {e}")

        return False

    # ---------------------------
    # RUN ONE ATTEMPT (FULL FIXED VERSION)
    # ---------------------------
    async def run_once(self, browser: Browser):
        self._attempts += 1
        ctx = None
        page = None
        try:
            ctx = await browser.new_context()
            page = await ctx.new_page()
            await page.goto(self.start_url, wait_until="domcontentloaded", timeout=60000)
            await asyncio.sleep(0.4)

            await self.handle_cookie_consent(page)

            found = await self.find_and_click_select_modules(page)
            if not found:
                await page.screenshot(path=str(screenshot_path(self.session_id, "no_button")))
                await ctx.close()
                return "button_not_found"

            await page.wait_for_load_state("domcontentloaded")
            await asyncio.sleep(0.4)

            err = await self.check_errors(page)
            if err:
                await page.screenshot(path=str(screenshot_path(self.session_id, f"error_{err}")))
                await ctx.close()
                return err

            # ⬇⬇⬇ FIXED SUCCESS LOGIC ⬇⬇⬇
            await page.wait_for_load_state("networkidle")
            checkpoint_url = page.url

            if checkpoint_url.strip() == self.start_url.strip():
                logger.warning(f"[{self.session_id}] FALSE SUCCESS — URL did not change")
                await ctx.close()
                return "retry"

            await page.screenshot(path=str(screenshot_path(self.session_id, "success")))

            storage = await ctx.storage_state()

            # DO NOT CLOSE CONTEXT NOW — return ctx
            return ("success", storage, checkpoint_url, ctx)

        except Exception as e:
            logger.exception(f"[{self.session_id}] Run exception: {e}")
            if page:
                try:
                    await page.screenshot(path=str(screenshot_path(self.session_id, "exception")))
                except:
                    pass
            if ctx:
                await ctx.close()
            return "exception"

    # ---------------------------
    # GUI DISPLAY
    # ---------------------------
    async def open_gui_with_storage(self, playwright_instance, storage_state, checkpoint_url):
        browser_gui = await playwright_instance.chromium.launch(headless=False, slow_mo=50)
        ctx_gui = await browser_gui.new_context(storage_state=storage_state)
        pg = await ctx_gui.new_page()
        try:
            await pg.goto(checkpoint_url, wait_until="domcontentloaded", timeout=60000)
        except:
            pass
        logger.info(f"[{self.session_id}] GUI OPENED at {checkpoint_url}")
        await asyncio.sleep(self.gui_display_seconds)
        await browser_gui.close()


# ---------------------------
# MANAGER
# ---------------------------
class SlotManager:
    def __init__(self, start_url, num_sessions, concurrency_limit, reuse_browser,
                 gui_display_seconds, session_timeout, max_restarts, stop_on_first_success):

        self.start_url = start_url
        self.num_sessions = num_sessions
        self.concurrency_limit = concurrency_limit
        self.reuse_browser = reuse_browser
        self.gui_display_seconds = gui_display_seconds
        self.session_timeout = session_timeout
        self.max_restarts = max_restarts
        self.stop_on_first_success = stop_on_first_success

        self._stop_event = asyncio.Event()
        self._results = {}
        self._restarts = {i + 1: 0 for i in range(num_sessions)}

    async def _worker(self, sid, browser, playwright_instance):
        session = SlotSession(sid, self.start_url, gui_display_seconds=self.gui_display_seconds)

        while not self._stop_event.is_set():
            if self._restarts[sid] > self.max_restarts:
                self._results[sid] = {"result": "gave_up", "attempts": session._attempts}
                return

            try:
                logger.info(f"[{sid}] Starting attempt #{self._restarts[sid] + 1}")
                coro = session.run_once(browser)
                res = await asyncio.wait_for(coro, timeout=self.session_timeout)

                if isinstance(res, tuple) and res[0] == "success":
                    _, storage_state, checkpoint_url, ctx = res
                    logger.info(f"[{sid}] SUCCESS at {checkpoint_url}")

                    await session.open_gui_with_storage(playwright_instance, storage_state, checkpoint_url)

                    await ctx.close()

                    self._results[sid] = {"result": "success", "attempts": session._attempts}

                    if self.stop_on_first_success:
                        self._stop_event.set()
                    return

                elif isinstance(res, str):
                    logger.info(f"[{sid}] RESULT: {res}")
                    if res == "retry":
                        await asyncio.sleep(1)
                        continue
                    if res in ("high_demand", "finish_other", "button_not_found"):
                        await asyncio.sleep(2)
                        continue
                    if res == "exception":
                        self._restarts[sid] += 1
                        continue

            except asyncio.TimeoutError:
                logger.warning(f"[{sid}] TIMEOUT — restarting session")
                self._restarts[sid] += 1
                continue

    async def run_until_success(self):
        async with async_playwright() as p:
            browser = None
            if self.reuse_browser:
                browser = await p.chromium.launch(headless=True)
                logger.info("[Manager] Shared browser launched")

            sem = asyncio.Semaphore(self.concurrency_limit)

            async def wrapper(sid):
                async with sem:
                    local_browser = browser
                    if not self.reuse_browser:
                        local_browser = await p.chromium.launch(headless=True)
                    try:
                        await self._worker(sid, local_browser, p)
                    finally:
                        if not self.reuse_browser:
                            await local_browser.close()

            workers = [asyncio.create_task(wrapper(i + 1)) for i in range(self.num_sessions)]

            await self._stop_event.wait()

            logger.info("[Manager] Success detected, cancelling workers…")
            for w in workers:
                if not w.done():
                    w.cancel()
            await asyncio.gather(*workers, return_exceptions=True)

            if browser:
                await browser.close()

            logger.info("[Manager] FINAL RESULTS:")
            for sid, info in self._results.items():
                logger.info(f"Session {sid}: {info}")

            return self._results


# ---------------------------
# ENTRYPOINT
# ---------------------------
async def main():
    logger.info("Starting Slot Watcher")

    mgr = SlotManager(
        START_URL,
        NUM_SESSIONS,
        CONCURRENCY_LIMIT,
        REUSE_BROWSER,
        GUI_DISPLAY_SECONDS,
        SESSION_TIMEOUT,
        MAX_RESTARTS,
        STOP_ON_FIRST_SUCCESS
    )

    await mgr.run_until_success()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.warning("Interrupted by user.")
