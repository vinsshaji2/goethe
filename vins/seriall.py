"""
Serial Browser Test Script
Runs booking tests one at a time until success
Only opens GUI if URL contains "options"
"""

import asyncio
import logging
import json
from datetime import datetime
from playwright.async_api import async_playwright
from vins import stealth_config
import os

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [Session-%(name)s] - %(levelname)s - %(message)s'
)


class MultipleBrowserTest:
    """Test booking on browser with module selection."""

    def __init__(self, start_url: str, session_id: int, headless: bool = False, proxy: str = None,
                 gui_display_seconds: int = 5, account: dict = None):
        self.start_url = start_url
        self.session_id = session_id
        self.headless = headless
        self.proxy = proxy
        self.gui_display_seconds = gui_display_seconds
        self.account = account
        self.page = None
        self.logger = logging.getLogger(f"{session_id}")
        self.required_modules = self._generate_random_modules()
        self.result = None
        self.duration = 0
        self.module_status = {}

    def _generate_random_modules(self):
        selected = ['reading']
        return selected

    async def handle_cookie_consent(self):
        try:
            self.logger.info("Checking for cookie consent dialog...")
            accept_selectors = [
                "button:has-text('Accept All')",
                "text=/accept all/i",
                "[data-testid*='accept']",
                "button[class*='accept']",
                "//button[contains(text(), 'Accept')]"
            ]
            for selector in accept_selectors:
                try:
                    button = self.page.locator(selector)
                    if await button.count() > 0:
                        self.logger.info("Cookie consent dialog found, clicking Accept All")
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

    async def check_high_demand_error(self):
        try:
            high_demand_text = await self.page.locator(
                "text=/very high demand|cannot be booked at the moment/i").first.text_content(timeout=2000)
            if high_demand_text:
                self.logger.error("❌ HIGH DEMAND ERROR DETECTED")
                return True
        except Exception:
            pass
        return False

    async def check_finish_other_bookings_error(self):
        try:
            finish_bookings_text = await self.page.locator(
                "text=/finish other started bookings|Please finish other started bookings/i").first.text_content(
                timeout=2000)
            if finish_bookings_text:
                self.logger.error("❌ BAD ERROR DETECTED")
                return True
        except Exception:
            pass
        return False

    async def check_url_has_options(self):
        """Check if current URL contains 'options' keyword."""
        current_url = self.page.url
        has_options = 'options' in current_url.lower()
        self.logger.info(f"Current URL: {current_url}")
        self.logger.info(f"URL contains 'options': {has_options}")
        return has_options

    async def show_success_gui_at_checkpoint(self, context_headless, playwright_instance, display_seconds: int = 5):
        try:
            checkpoint_url = self.page.url
            self.logger.info(f"💾 Saving session state from checkpoint: {checkpoint_url}")
            storage_state = await context_headless.storage_state()
            self.logger.info("✅ Session state saved successfully")

            fingerprint = stealth_config.get_ultra_random_fingerprint()
            http_headers = stealth_config.get_random_http_headers(
                fingerprint['locale'],
                fingerprint['user_agent']
            )

            self.logger.info(f"🖥️  Opening GUI browser at checkpoint for {display_seconds} seconds...")

            browser_gui = await playwright_instance.chromium.launch(
                headless=False,
                slow_mo=50,
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--disable-dev-shm-usage',
                    '--no-sandbox',
                    '--disable-web-security',
                ]
            )

            context_options = {
                'viewport': fingerprint['viewport'],
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

            if self.proxy:
                if '@' in self.proxy:
                    auth_part, server_part = self.proxy.split('@')
                    username, password = auth_part.split(':')
                    context_options['proxy'] = {
                        'server': f'http://{server_part}',
                        'username': username,
                        'password': password
                    }
                else:
                    context_options['proxy'] = {'server': f'http://{self.proxy}'}

            context_gui = await browser_gui.new_context(**context_options)
            page_gui = await context_gui.new_page()

            stealth_script = stealth_config.get_stealth_script()
            await page_gui.add_init_script(stealth_script)

            await page_gui.goto(checkpoint_url, wait_until='domcontentloaded', timeout=300000)
            self.logger.info(f"✅ GUI browser opened at checkpoint with preserved session state")

            # Handle cookie consent
            cookie_accept_selectors = [
                "button:has-text('Accept All')",
                "text=/accept all/i",
                "[data-testid*='accept']",
                "button[class*='accept']",
                "//button[contains(text(), 'Accept')]"
            ]
            await asyncio.sleep(1)
            for selector in cookie_accept_selectors:
                try:
                    button = page_gui.locator(selector)
                    if await button.count() > 0:
                        await button.click(timeout=5000)
                        await asyncio.sleep(1)
                        break
                except Exception:
                    continue

            await asyncio.sleep(20000000000000000)

            # Continue with rest of booking flow...
            # (keeping the same logic as before)

            await asyncio.sleep(15)
            await browser_gui.close()
            self.logger.info("🔒 GUI browser closed")

        except Exception as e:
            self.logger.error(f"Error showing GUI at checkpoint: {str(e)}")

    async def run_test(self):
        """Run the complete test. Returns True if successful (URL has 'options')."""
        async with async_playwright() as p:
            browser = None
            try:
                start_time = datetime.now()

                self.logger.info("=" * 60)
                self.logger.info(f"Starting test - Required modules: {', '.join(self.required_modules)}")

                fingerprint = stealth_config.get_ultra_random_fingerprint()
                http_headers = stealth_config.get_random_http_headers(
                    fingerprint['locale'],
                    fingerprint['user_agent']
                )

                self.logger.info(f"Fingerprint: {fingerprint['user_agent'][:50]}...")
                self.logger.info(f"Viewport: {fingerprint['viewport']['width']}x{fingerprint['viewport']['height']}")
                if self.proxy:
                    self.logger.info(f"Using Proxy: {self.proxy}")

                browser = await p.chromium.launch(
                    headless=True,
                    slow_mo=50,
                    args=[
                        '--disable-blink-features=AutomationControlled',
                        '--disable-dev-shm-usage',
                        '--no-sandbox',
                        '--disable-web-security',
                    ]
                )

                context_options = {
                    'viewport': fingerprint['viewport'],
                    'user_agent': fingerprint['user_agent'],
                    'locale': fingerprint['locale'],
                    'timezone_id': fingerprint['timezone_id'],
                    'permissions': [],
                    'storage_state': None,
                    'ignore_https_errors': True,
                    'java_script_enabled': True,
                    'device_scale_factor': fingerprint['device_scale_factor'],
                    'has_touch': fingerprint['has_touch'],
                    'is_mobile': False,
                    'color_scheme': fingerprint['color_scheme'],
                    'extra_http_headers': http_headers
                }

                if self.proxy:
                    if '@' in self.proxy:
                        auth_part, server_part = self.proxy.split('@')
                        username, password = auth_part.split(':')
                        context_options['proxy'] = {
                            'server': f'http://{server_part}',
                            'username': username,
                            'password': password
                        }
                    else:
                        context_options['proxy'] = {'server': f'http://{self.proxy}'}

                context = await browser.new_context(**context_options)
                await context.clear_cookies()
                await context.clear_permissions()

                self.page = await context.new_page()

                stealth_script = stealth_config.get_stealth_script()
                await self.page.add_init_script(stealth_script)

                self.logger.info("Navigating to booking page...")
                await self.page.goto(self.start_url, wait_until='domcontentloaded', timeout=300000)
                await asyncio.sleep(1)

                await self.handle_cookie_consent()
                await asyncio.sleep(1)

                # Click "Select modules" button
                self.logger.info("Clicking 'Select modules' button...")
                select_button_selectors = [
                    'text="Select modules"',
                    'button:has-text("Select modules")',
                    'a:has-text("Select modules")',
                ]

                button_clicked = False
                for selector in select_button_selectors:
                    try:
                        await self.page.click(selector, timeout=5000)
                        button_clicked = True
                        break
                    except Exception:
                        continue

                if button_clicked:
                    self.logger.info("✅ 'Select modules' button clicked")
                    await asyncio.sleep(1)

                # Check for errors AFTER clicking Select modules
                self.logger.info("Checking for errors...")

                has_high_demand = await self.check_high_demand_error()
                has_bad_error = await self.check_finish_other_bookings_error()

                # If NO errors occurred, check if URL has 'options'
                if not has_high_demand and not has_bad_error:
                    self.logger.info("No errors detected, checking URL...")

                    if await self.check_url_has_options():
                        self.logger.info("✅ SUCCESS: URL contains 'options' - Opening GUI!")
                        self.result = 'success'
                        await self.show_success_gui_at_checkpoint(context, p, display_seconds=self.gui_display_seconds)
                        end_time = datetime.now()
                        self.duration = (end_time - start_time).total_seconds()
                        return True  # Successful!
                    else:
                        self.logger.warning("❌ URL does not contain 'options' - Will retry...")
                        self.result = 'no_options_in_url'
                        end_time = datetime.now()
                        self.duration = (end_time - start_time).total_seconds()
                        return False  # Not successful
                else:
                    # Errors occurred
                    if has_high_demand:
                        self.result = 'high_demand_error'
                    elif has_bad_error:
                        self.result = 'bad_error'
                    end_time = datetime.now()
                    self.duration = (end_time - start_time).total_seconds()
                    return False  # Not successful

            except Exception as e:
                self.logger.error(f"Exception occurred: {str(e)}")
                self.result = 'exception'
                end_time = datetime.now()
                self.duration = (end_time - start_time).total_seconds() if 'start_time' in locals() else 0
                return False

            finally:
                if browser:
                    await browser.close()


class SerialTestManager:
    """Manage serial browser tests - runs one at a time until success."""

    def __init__(self, start_url: str, max_attempts: int, headless: bool = False, proxies: list = None,
                 gui_display_seconds: int = 5, accounts: list = None):
        self.start_url = start_url
        self.max_attempts = max_attempts
        self.headless = headless
        self.proxies = proxies or []
        self.gui_display_seconds = gui_display_seconds
        self.accounts = accounts or []
        self.results = {}
        self.logger = logging.getLogger("Manager")

    async def run_serial_until_success(self):
        """Run test sessions one at a time until success or max attempts reached."""
        self.logger.info("=" * 80)
        self.logger.info(f"STARTING SERIAL BROWSER TESTS (Max attempts: {self.max_attempts})")
        if self.proxies:
            self.logger.info(f"Using {len(self.proxies)} authenticated proxies (Decodo)")
        else:
            self.logger.info("No proxies configured - using direct connection")
        self.logger.info("=" * 80)
        self.logger.info("")

        for attempt in range(1, self.max_attempts + 1):
            self.logger.info(f"\n{'=' * 60}")
            self.logger.info(f"ATTEMPT {attempt} of {self.max_attempts}")
            self.logger.info(f"{'=' * 60}")

            # Assign proxy (cycle through proxies)
            proxy = None
            if self.proxies:
                proxy_index = (attempt - 1) % len(self.proxies)
                proxy = self.proxies[proxy_index]

            # Assign account (cycle through accounts)
            account = None
            if self.accounts:
                account_index = (attempt - 1) % len(self.accounts)
                account = self.accounts[account_index]

            # Run test
            test = MultipleBrowserTest(
                self.start_url,
                attempt,
                self.headless,
                proxy,
                self.gui_display_seconds,
                account
            )

            success = await test.run_test()

            # Store result
            self.results[attempt] = {
                'session_id': attempt,
                'result': test.result,
                'duration': test.duration,
                'required_modules': test.required_modules,
                'module_status': test.module_status,
                'proxy': proxy
            }

            if success:
                self.logger.info(f"\n{'=' * 60}")
                self.logger.info(f"✅✅✅ SUCCESS ON ATTEMPT {attempt}! ✅✅✅")
                self.logger.info(f"{'=' * 60}")
                self.print_statistics()
                return True

            self.logger.info(f"❌ Attempt {attempt} failed with result: {test.result}")

            # Small delay between attempts
            if attempt < self.max_attempts:
                self.logger.info("⏳ Waiting 2 seconds before next attempt...")
                await asyncio.sleep(2)

        self.logger.info(f"\n{'=' * 60}")
        self.logger.info(f"❌ ALL {self.max_attempts} ATTEMPTS FAILED")
        self.logger.info(f"{'=' * 60}")
        self.print_statistics()
        return False

    def print_statistics(self):
        """Print summary statistics."""
        self.logger.info("\n" + "-" * 60)
        self.logger.info("SUMMARY:")
        self.logger.info("-" * 60)

        total_duration = 0
        result_counts = {}

        for attempt, data in sorted(self.results.items()):
            result = data['result']
            result_counts[result] = result_counts.get(result, 0) + 1
            total_duration += data['duration']

            emoji = '✅' if result == 'success' else '❌'
            self.logger.info(f"Attempt {attempt:2d}: {emoji} {result:20s} | Duration: {data['duration']:6.2f}s")

        self.logger.info("-" * 60)
        self.logger.info(f"Total attempts: {len(self.results)}")
        self.logger.info(f"Total duration: {total_duration:.2f}s")
        for result, count in result_counts.items():
            self.logger.info(f"  {result}: {count}")


def generate_authenticated_proxies(num_proxies: int = 1000):
    username = 'spii5uqapq'
    password = 'fwThVwm=4g8is04FeZ'
    proxy_host = 'gate.decodo.com'

    proxies = []
    base_port = 10001

    for i in range(num_proxies):
        port = base_port + i
        proxy_url = f"{username}:{password}@{proxy_host}:{port}"
        proxies.append(proxy_url)

    print(f"✅ Generated {len(proxies)} authenticated proxy addresses")
    return proxies


def load_accounts(accounts_file: str = "accounts.json"):
    try:
        if not os.path.exists(accounts_file):
            print(f"⚠️  Accounts file '{accounts_file}' not found.")
            return []
        with open(accounts_file, 'r') as f:
            accounts = json.load(f)
        print(f"✅ Loaded {len(accounts)} accounts from {accounts_file}")
        return accounts
    except Exception as e:
        print(f"❌ Error loading accounts: {str(e)}")
        return []


async def main():
    start_url = 'https://www.goethe.de/ins/in/en/spr/prf/gzb2.cfm?examId=580D9BDA8288A8858A8E06C37C9F0D5527D4DD78EFC5FEEA0CAC00A8D795C8FC8B9BEACE83112A47D5ECFCD507D34ED0EEFAD8C603D1539BA72BD61ECB83CEE6'
    headless = False
    gui_display_seconds = 200000000

    proxies = generate_authenticated_proxies(num_proxies=100)
    accounts = load_accounts("accounts.json")

    print("\n" + "=" * 80)
    print("SERIAL BROWSER TEST - ONE AT A TIME UNTIL SUCCESS")
    print("=" * 80)
    print("Features:")
    print("  ✅ Serial execution (one at a time)")
    print("  ✅ Stops on first success")
    print("  ✅ Only opens GUI if URL contains 'options'")
    print("  ✅ Session state preservation")
    print("  ✅ Different proxy per attempt")
    print("=" * 80)

    try:
        n = int(input("\nEnter max number of attempts: "))
        if n <= 0:
            print("❌ Number must be greater than 0")
            return
    except ValueError:
        print("❌ Invalid input.")
        return

    print(f"\n🚀 Starting serial tests (max {n} attempts)...")
    print(f"🔑 Success condition: URL must contain 'options'")
    print(f"🌐 Proxies: {len(proxies)} available")
    print(f"👤 Accounts: {len(accounts)} loaded")
    print("\n" + "=" * 80 + "\n")

    manager = SerialTestManager(start_url, n, headless, proxies, gui_display_seconds, accounts)
    await manager.run_serial_until_success()

    print("\n✅ Test sequence completed!")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user.")
    except Exception as e:
        print(f"\n\n❌ Fatal error: {str(e)}")