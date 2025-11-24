import asyncio
import logging
from datetime import datetime
from playwright.async_api import async_playwright


# --------------------------------------------------------
# Logging Setup
# --------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [Session-%(name)s] - %(levelname)s - %(message)s'
)


# --------------------------------------------------------
# Single Browser Test
# --------------------------------------------------------
class SimpleBrowserTest:
    def __init__(self, start_url: str, session_id: int, gui_display_seconds: int = 10):
        self.start_url = start_url
        self.session_id = session_id
        self.gui_display_seconds = gui_display_seconds
        self.page = None
        self.logger = logging.getLogger(f"{session_id}")
        self.result = None
        self.duration = 0

    # --------------------------
    # COOKIE CONSENT HANDLER
    # --------------------------
    async def handle_cookie_consent(self):
        self.logger.info("Checking cookie consent...")

        selectors = [
            "button:has-text('Accept All')",
            "button:has-text('ACCEPT ALL')",
            "text=/accept all/i",
            "[data-testid*='accept']",
            "button[class*='accept']",
            "//button[contains(text(), 'Accept')]",
        ]

        try:
            for s in selectors:
                try:
                    btn = self.page.locator(s)
                    if await btn.count() > 0:
                        await btn.click(timeout=2000)
                        self.logger.info("🟢 Cookie consent accepted")
                        await asyncio.sleep(1)
                        return True
                except:
                    continue
        except:
            pass

        self.logger.info("No cookie dialog found")
        return False

    # --------------------------
    # ERROR CHECKERS
    # --------------------------
    async def check_high_demand_error(self):
        try:
            msg = await self.page.locator(
                "text=/very high demand|cannot be booked/i"
            ).first.text_content(timeout=1500)
            if msg:
                return True
        except:
            return False
        return False

    async def check_finish_other_error(self):
        try:
            msg = await self.page.locator(
                "text=/finish other started bookings/i"
            ).first.text_content(timeout=1500)
            if msg:
                return True
        except:
            return False
        return False

    # --------------------------
    # GUI REPLAY WITH SESSION STATE
    # --------------------------
    async def show_gui(self, context, playwright_instance):
        checkpoint_url = self.page.url
        storage = await context.storage_state()

        browser_gui = await playwright_instance.chromium.launch(
            headless=False,
            slow_mo=50
        )

        context_gui = await browser_gui.new_context(
            storage_state=storage
        )

        page_gui = await context_gui.new_page()
        await page_gui.goto(checkpoint_url, wait_until="domcontentloaded")

        self.logger.info("GUI opened with restored session. Keeping open...")
        await asyncio.sleep(self.gui_display_seconds)
        await browser_gui.close()

    # --------------------------
    # MAIN TEST LOGIC
    # --------------------------
    async def run_test(self):
        async with async_playwright() as p:
            browser = None
            try:
                start_time = datetime.now()

                # Start headless browser
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context()
                self.page = await context.new_page()

                # Go to exam page
                self.logger.info("Opening URL...")
                await self.page.goto(self.start_url, timeout=3000)

                # Handle cookies
                await asyncio.sleep(0.5)
                await self.handle_cookie_consent()

                # Click "Select modules"
                self.logger.info("Clicking Select Modules...")
                selectors = [
                    "text=Select modules",
                    "button:has-text('Select modules')",
                ]
                clicked = False
                for s in selectors:
                    try:
                        await self.page.click(s, timeout=3000)
                        clicked = True
                        break
                    except:
                        continue

                if not clicked:
                    self.result = "button_not_found"
                    return self.result

                await asyncio.sleep(1)

                # Error checks
                if await self.check_high_demand_error():
                    self.result = "high_demand"
                    return self.result

                if await self.check_finish_other_error():
                    self.result = "finish_other"
                    return self.result

                # If reached here → SUCCESS
                self.result = "success"
                self.logger.info("SUCCESS - Opening GUI browser...")

                await self.show_gui(context, p)

                return self.result

            except Exception as e:
                self.logger.error(f"ERROR: {str(e)}")
                self.result = "exception"
                return "exception"

            finally:
                end = datetime.now()
                self.duration = (end - start_time).total_seconds()
                if browser:
                    await browser.close()


# --------------------------------------------------------
# Manager for Parallel Execution
# --------------------------------------------------------
class SimpleTestManager:
    def __init__(self, start_url: str, num_sessions: int, gui_display_seconds: int = 10):
        self.start_url = start_url
        self.num_sessions = num_sessions
        self.gui_display_seconds = gui_display_seconds
        self.results = {}
        self.logger = logging.getLogger("Manager")

    async def run_single(self, sid: int):
        test = SimpleBrowserTest(self.start_url, sid, self.gui_display_seconds)
        await test.run_test()

        self.results[sid] = {
            "result": test.result,
            "duration": test.duration
        }

    async def run_all_parallel(self):
        tasks = [self.run_single(i + 1) for i in range(self.num_sessions)]
        await asyncio.gather(*tasks)


# --------------------------------------------------------
# MAIN
# --------------------------------------------------------
async def main():
    start_url = "https://www.goethe.de/ins/in/en/spr/prf/gzb2.cfm?examId=585ACE89868FA9D5D6DD50962CC95A5527D4DB74EC96A9E201FE01A982C6C3A8DFCEB8C5DF167A1B88B8FBD20FDE42D6EEAEDB9701D704CCF57D8712CA81CDEA"
    gui_seconds = 20000000

    n = int(input("Enter number of parallel browsers: "))

    manager = SimpleTestManager(start_url, n, gui_seconds)
    await manager.run_all_parallel()

    print("\nRESULTS:")
    for sid, r in manager.results.items():
        print(f"Session {sid}: {r['result']} in {r['duration']:.1f}s")


if __name__ == "__main__":
    asyncio.run(main())
