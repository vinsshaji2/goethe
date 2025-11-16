"""
Simple Parallel Browser Script
Opens N parallel browser sessions with the URL
"""

import asyncio
import logging
from datetime import datetime
from playwright.async_api import async_playwright
import stealth_config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [Session-%(name)s] - %(levelname)s - %(message)s'
)


class SimpleBrowserSession:
    """Simple browser session that just opens a URL."""

    def __init__(self, start_url: str, session_id: int, proxy: str = None, gui_display_seconds: int = 10):
        """
        Initialize browser session.

        Args:
            start_url: The URL to open
            session_id: Unique session identifier
            proxy: Proxy server address (format: "username:password@host:port")
            gui_display_seconds: How many seconds to wait after clicking button before stopping
        """
        self.start_url = start_url
        self.session_id = session_id
        self.proxy = proxy
        self.gui_display_seconds = gui_display_seconds
        self.logger = logging.getLogger(f"{session_id}")

    async def handle_cookie_consent(self, page):
        """Handle cookie consent dialog if it appears."""
        try:
            self.logger.info("Checking for cookie consent dialog...")

            # Multiple selectors for cookie acceptance
            accept_selectors = [
                "button:has-text('Accept All')",
                "text=/accept all/i",
                "[data-testid*='accept']",
                "button[class*='accept']",
                "//button[contains(text(), 'Accept')]"
            ]

            for selector in accept_selectors:
                try:
                    button = page.locator(selector)
                    if await button.count() > 0:
                        self.logger.info("✅ Cookie consent dialog found, clicking Accept All")
                        await button.click(timeout=5000)
                        await asyncio.sleep(1)
                        return True
                except Exception:
                    continue

            self.logger.info("No cookie consent dialog found")
            return False

        except Exception as e:
            self.logger.warning(f"Cookie consent handling warning: {str(e)}")
            return False

    async def check_high_demand_error(self, page):
        """Check for 'very high demand' error message."""
        try:
            high_demand_text = await page.locator(
                "text=/very high demand|cannot be booked at the moment/i").first.text_content(timeout=2000)
            if high_demand_text:
                self.logger.error("❌ HIGH DEMAND ERROR DETECTED - Will not open GUI")
                return True
        except Exception:
            pass
        return False

    async def check_finish_other_bookings_error(self, page):
        """Check for 'finish other started bookings' error message."""
        try:
            finish_bookings_text = await page.locator(
                "text=/finish other started bookings|Please finish other started bookings/i").first.text_content(
                timeout=2000)
            if finish_bookings_text:
                self.logger.error("❌ FINISH OTHER BOOKINGS ERROR DETECTED - Will not open GUI")
                return True
        except Exception:
            pass
        return False

    # async def check_modules_available(self, page):
    #     """Check if any module checkboxes are available on the page."""
    #     try:
    #         # Wait for checkbox wrapper to appear
    #         await page.wait_for_selector('.cs-input__checkboxes-wrapper', timeout=5000)
    #
    #         # Check for any module checkboxes
    #         module_names = ['reading', 'listening', 'writing', 'speaking']
    #
    #         for module in module_names:
    #             checkbox_selector = f'input[id="{module}"]'
    #             checkbox = await page.query_selector(checkbox_selector)
    #
    #             if checkbox:
    #                 is_disabled = await checkbox.get_attribute('disabled')
    #
    #                 # Check if label contains "fully booked"
    #                 label_selector = f'label[for="{module}"]'
    #                 label = await page.query_selector(label_selector)
    #                 is_fully_booked = False
    #
    #                 if label:
    #                     label_text = await label.text_content()
    #                     if label_text and 'fully booked' in label_text.lower():
    #                         is_fully_booked = True
    #
    #                 # If module is available (not disabled and not fully booked)
    #                 if not is_disabled and not is_fully_booked:
    #                     self.logger.info(f"✅ Module available: {module.upper()}")
    #                     return True
    #
    #         self.logger.warning("⚠️  No modules available - all are disabled or fully booked")
    #         return False
    #
    #     except Exception as e:
    #         self.logger.warning(f"⚠️  Could not find module checkboxes: {str(e)}")
    #         return False

    async def click_select_modules(self, page):
        """Try to click 'Select modules' button."""
        select_button_selectors = [
            'text="Select modules"',
            'button:has-text("Select modules")',
            'a:has-text("Select modules")',
            "//button[contains(text(), 'Select modules')]",
            "//a[contains(text(), 'Select modules')]",
        ]

        for selector in select_button_selectors:
            try:
                button = page.locator(selector)
                if await button.count() > 0:
                    await button.click(timeout=5000)
                    self.logger.info("✅ Successfully clicked 'Select modules' button")
                    return True
            except Exception:
                continue

        return False

    async def clear_and_reload(self, context, page):
        """Clear cookies, cache and reload the page."""
        try:
            self.logger.info("🔄 Clearing cookies and cache...")

            # Clear cookies
            await context.clear_cookies()

            # Clear cache using CDP (Chrome DevTools Protocol)
            # cdp = await context.new_cdp_session(page)
            # await cdp.send('Network.clearBrowserCache')
            # await cdp.send('Network.clearBrowserCookies')

            # Reload page
            self.logger.info("🔄 Reloading page...")
            await page.reload(wait_until='domcontentloaded', timeout=30000)
            await asyncio.sleep(.5)

            self.logger.info("✅ Cache cleared and page reloaded")
            return True

        except Exception as e:
            self.logger.error(f"❌ Error clearing cache: {str(e)}")
            return False

    async def show_success_gui(self, playwright_instance, storage_state, checkpoint_url):
        """
        Show GUI browser at the checkpoint where success occurred.

        Args:
            playwright_instance: The Playwright instance
            storage_state: Saved session state
            checkpoint_url: URL where success occurred
        """
        try:
            self.logger.info(f"🖥️  Opening GUI browser for {self.gui_display_seconds} seconds...")

            # Get fingerprint for GUI browser
            fingerprint = stealth_config.get_ultra_random_fingerprint()
            http_headers = stealth_config.get_random_http_headers(
                fingerprint['locale'],
                fingerprint['user_agent']
            )

            # Launch GUI browser
            browser_gui = await playwright_instance.chromium.launch(
                headless=False,
                slow_mo=50,
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--disable-dev-shm-usage',
                    '--no-sandbox',
                    '--disable-web-security',
                    '--start-maximized',  # Start maximized
                ]
            )

            # Create context with restored session
            context_options = {
                'viewport': {'width': 1920, 'height': 1080},  # Fixed: Use proper viewport size
                'user_agent': fingerprint['user_agent'],
                'locale': fingerprint['locale'],
                'timezone_id': fingerprint['timezone_id'],
                'permissions': [],
                'storage_state': storage_state,
                'ignore_https_errors': True,
                'java_script_enabled': True,
                'device_scale_factor': fingerprint['device_scale_factor'],
                'has_touch': fingerprint['has_touch'],
                'is_mobile': False,
                'color_scheme': fingerprint['color_scheme'],
                'extra_http_headers': http_headers
            }

            # Add proxy if provided
            # if self.proxy:
            #     if '@' in self.proxy:
            #         auth_part, server_part = self.proxy.split('@')
            #         username, password = auth_part.split(':')
            #         context_options['proxy'] = {
            #             'server': f'http://{server_part}',
            #             'username': username,
            #             'password': password
            #         }
            #     else:
            #         context_options['proxy'] = {
            #             'server': f'http://{self.proxy}'
            #         }

            context_gui = await browser_gui.new_context(**context_options)
            page_gui = await context_gui.new_page()

            # Apply stealth script
            stealth_script = stealth_config.get_stealth_script()
            await page_gui.add_init_script(stealth_script)

            # Navigate to checkpoint
            await page_gui.goto(checkpoint_url, wait_until='domcontentloaded', timeout=30000)
            self.logger.info("✅ GUI browser opened with preserved session")

            # Wait for specified seconds
            self.logger.info(f"⏳ Keeping GUI open for {self.gui_display_seconds} seconds...")
            await asyncio.sleep(self.gui_display_seconds)

            # Close GUI browser
            await browser_gui.close()
            self.logger.info("🔒 GUI browser closed")

        except Exception as e:
            self.logger.error(f"Error showing GUI: {str(e)}")

    async def run_session(self):
        """Open browser and navigate to URL."""
        async with async_playwright() as p:
            browser_headless = None
            try:
                start_time = datetime.now()

                self.logger.info("Starting browser session in HEADLESS mode...")

                # Get ultra-random fingerprint
                fingerprint = stealth_config.get_ultra_random_fingerprint()
                http_headers = stealth_config.get_random_http_headers(
                    fingerprint['locale'],
                    fingerprint['user_agent']
                )

                # if self.proxy:
                #     self.logger.info(f"Using Proxy: {self.proxy}")

                # Launch browser in HEADLESS mode
                browser_headless = await p.chromium.launch(
                    headless=True,  # Start headless
                    slow_mo=50,
                    args=[
                        '--disable-blink-features=AutomationControlled',
                        '--disable-dev-shm-usage',
                        '--no-sandbox',
                        '--disable-web-security',
                    ]
                )

                # Create context with fingerprint and proxy
                context_options = {
                    'viewport': fingerprint['viewport'],
                    'user_agent': fingerprint['user_agent'],
                    'locale': fingerprint['locale'],
                    'timezone_id': fingerprint['timezone_id'],
                    'permissions': [],
                    'ignore_https_errors': True,
                    'java_script_enabled': True,
                    'device_scale_factor': fingerprint['device_scale_factor'],
                    'has_touch': fingerprint['has_touch'],
                    'is_mobile': False,
                    'color_scheme': fingerprint['color_scheme'],
                    'extra_http_headers': http_headers
                }

                # Add proxy if provided (with authentication)
                # if self.proxy:
                #     if '@' in self.proxy:
                #         auth_part, server_part = self.proxy.split('@')
                #         username, password = auth_part.split(':')
                #         context_options['proxy'] = {
                #             'server': f'http://{server_part}',
                #             'username': username,
                #             'password': password
                #         }
                #     else:
                #         # context_options['proxy'] = {
                #         #                         #     'server': f'http://{self.proxy}'
                #         # }
                #         pass
                context_headless = await browser_headless.new_context(**context_options)
                page = await context_headless.new_page()

                # Apply stealth script
                stealth_script = stealth_config.get_stealth_script()
                await page.add_init_script(stealth_script)

                # Navigate to URL
                self.logger.info(f"Opening: {self.start_url}")
                await page.goto(self.start_url, wait_until='domcontentloaded', timeout=30000)
                await asyncio.sleep(2)

                # Continuously try to click 'Select modules' button
                attempt = 0
                max_attempts = 100  # Maximum attempts to prevent infinite loop
                success = False

                while attempt < max_attempts:
                    attempt += 1
                    self.logger.info(f"🔍 Attempt {attempt}: Looking for 'Select modules' button...")


                    # await asyncio.sleep(1)

                    # Try to click 'Select modules' button
                    if await self.click_select_modules(page):
                        self.logger.info(f"✅ 'Select modules' button clicked on attempt {attempt}")

                        # Wait 10 seconds after clicking
                        self.logger.info(f"⏳ Waiting {self.gui_display_seconds} seconds after button click...")
                        await asyncio.sleep(.5)

                        # Check for errors FIRST
                        self.logger.info("🔍 Checking for errors...")

                        if await self.check_high_demand_error(page):
                            self.logger.error("❌ HIGH DEMAND ERROR - Skipping GUI and stopping this session")
                            break

                        if await self.check_finish_other_bookings_error(page):
                            self.logger.error("❌ FINISH OTHER BOOKINGS ERROR - Skipping GUI and stopping this session")
                            break

                        # Check if modules are available
                        self.logger.info("🔍 Checking for available modules...")
                        # if await self.check_modules_available(page):
                        #     self.logger.info("✅✅✅ SUCCESS! Modules are available!")
                        success = True

                        # Save session state and URL
                        checkpoint_url = page.url
                        storage_state = await context_headless.storage_state()
                        self.logger.info("💾 Session state saved")

                        # Close headless browser
                        await browser_headless.close()
                        browser_headless = None

                        # Open GUI browser with saved state
                        await self.show_success_gui(p, storage_state, checkpoint_url)
                        # Handle cookie consent first
                        await self.handle_cookie_consent(page)
                        # else:
                        #     self.logger.error("❌ No modules available - Skipping GUI and stopping this session")

                        break
                    else:
                        self.logger.warning(f"⚠️  'Select modules' button not found on attempt {attempt}")

                        # Clear cookies, cache and reload
                        await self.clear_and_reload(context_headless, page)
                        await asyncio.sleep(2)

                        # Continue to next attempt
                        continue

                if not success:
                    self.logger.error(f"❌ Failed to find 'Select modules' button after {max_attempts} attempts")
                else:
                    end_time = datetime.now()
                    duration = (end_time - start_time).total_seconds()
                    self.logger.info(f"✅ Total Duration: {duration:.2f}s")
                    self.logger.info("✅ Session completed successfully!")

            except Exception as e:
                self.logger.error(f"❌ Error: {str(e)}")

            finally:
                if browser_headless:
                    # await browser_headless.close()
                    await asyncio.sleep(1000000000)

class ParallelBrowserManager:
    """Manage multiple parallel browser sessions."""

    def __init__(self, start_url: str, num_sessions: int, proxies: list = None, gui_display_seconds: int = 100000000000):
        """
        Initialize manager.

        Args:
            start_url: The URL to open
            num_sessions: Number of parallel browser sessions
            proxies: List of proxy addresses to use
            gui_display_seconds: How many seconds to display GUI on success
        """
        self.start_url = start_url
        self.num_sessions = num_sessions
        self.proxies = proxies or []
        self.gui_display_seconds = gui_display_seconds
        self.logger = logging.getLogger("Manager")

    async def run_single_session(self, session_id: int):
        """Run a single browser session."""
        # Assign proxy to session (cycle through proxies if more sessions than proxies)
        proxy = None
        if self.proxies:
            proxy_index = (session_id - 1) % len(self.proxies)
            proxy = self.proxies[proxy_index]

        session = SimpleBrowserSession(self.start_url, session_id, proxy, self.gui_display_seconds)
        await session.run_session()

    async def run_all_parallel(self):
        """Run all browser sessions in parallel."""
        self.logger.info("=" * 80)
        self.logger.info(f"STARTING {self.num_sessions} PARALLEL BROWSER SESSIONS")
        if self.proxies:
            self.logger.info(f"Using {len(self.proxies)} authenticated proxies")
        else:
            self.logger.info("No proxies configured - using direct connection")
        self.logger.info("=" * 80)
        self.logger.info("")

        # Create tasks for all sessions
        tasks = [
            self.run_single_session(i + 1)
            for i in range(self.num_sessions)
        ]

        # Run all in parallel
        await asyncio.gather(*tasks, return_exceptions=True)


# ============================================================================
# PROXY GENERATION
# ============================================================================

def generate_authenticated_proxies(num_proxies: int = 1000):
    """
    Generate authenticated proxy addresses using Decodo proxy service.

    Args:
        num_proxies: Number of proxy addresses to generate (uses different ports)

    Returns:
        List of authenticated proxy URLs
    """
    username = 'spw4p88v6c'
    password = 'fDwWo7mIm04xKmh5~e'
    proxy_host = 'dc.decodo.com'

    proxies = []
    base_port = 10001

    for i in range(num_proxies):
        port = base_port + i
        proxy_url = f"{username}:{password}@{proxy_host}:{port}"
        proxies.append(proxy_url)

    print(f"✅ Generated {len(proxies)} authenticated proxy addresses")
    return proxies


# ============================================================================
# MAIN EXECUTION
# ============================================================================

async def main():
    """Main entry point."""

    # Configuration
    start_url = 'https://www.goethe.de/ins/in/en/spr/prf/gzb2.cfm?examId=590D9988DEDCAF83D7D805CA7CCE5C537DD2DF7DEBCDABE201F400AA81959DAED8C8EEC4DF422D47DAB8FD8452D11F80E6FB8BC15E8503CDF12B85429CDEC0E9'
    gui_display_seconds = 10000000000000  # Wait time after button click & GUI display time

    # Generate authenticated proxies
    # proxies = generate_authenticated_proxies(num_proxies=100)

    print("\n" + "=" * 80)
    print("PARALLEL BROWSER WITH SELECT MODULE AUTO-CLICKER")
    print("=" * 80)
    print("Features:")
    print("  ✅ N parallel browser sessions (HEADLESS)")
    print("  ✅ Auto-handles cookie consent")
    print("  ✅ Continuously searches for 'Select modules' button")
    print("  ✅ Auto-clears cookies/cache and reloads on failure")
    print("  ✅ Waits 10 seconds after button click (STOPS REFRESHING)")
    print("  ✅ Checks for errors (High Demand, Finish Other Bookings)")
    print("  ✅ Validates module availability (checkboxes)")
    print("  ✅ Opens GUI browser ONLY if modules are available")
    print("  ✅ Unique stealth fingerprint per session")
    print("  ✅ Proxy support with authentication")
    print("=" * 80)

    try:
        n = int(input("\nEnter number of parallel browsers (N): "))
        if n <= 0:
            print("❌ Number must be greater than 0")
            return
    except ValueError:
        print("❌ Invalid input. Please enter a number.")
        return

    print(f"\n🚀 Starting {n} parallel browser sessions...")
    # print(f"🌐 Proxies: {len(proxies)} authenticated proxies available")
    print(f"🔒 Mode: HEADLESS → GUI on Success ({gui_display_seconds}s)")
    print(f"⏳ After button click: Wait {gui_display_seconds}s (NO REFRESH)")
    print(f"⚠️  Press Ctrl+C to stop all sessions")
    print("\n" + "=" * 80 + "\n")

    # Create and run manager
    manager = ParallelBrowserManager(start_url=start_url,num_sessions=n, proxies=None, gui_display_seconds=10000000000000)
    await manager.run_all_parallel()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Closing all browsers...")
    except Exception as e:
        print(f"\n\n❌ Fatal error: {str(e)}")


