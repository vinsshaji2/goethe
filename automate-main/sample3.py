"""
Multiple Browser Test Script with Pre-Check
- Continuously monitors for "Select modules" button availability
- Launches parallel instances only when button is confirmed available
- Keeps successful sessions alive for 2 hours
- Optimized performance and error handling
"""

import asyncio
import logging
import json
from datetime import datetime, timedelta
from playwright.async_api import async_playwright
from vins import stealth_config
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [%(name)s] - %(levelname)s - %(message)s'
)


class AvailabilityChecker:
    """Continuously checks if booking is available before launching parallel tests."""

    def __init__(self, start_url: str, proxy: str = None):
        self.start_url = start_url
        self.proxy = proxy
        self.logger = logging.getLogger("AvailabilityChecker")
        self.page = None
        self.context = None
        self.browser = None

    async def check_availability(self):
        """
        Continuously check if 'Select modules' button is available.
        Returns True when button is found, clears cache/cookies and retries if not.
        """
        async with async_playwright() as p:
            attempt = 0

            while True:
                attempt += 1
                self.logger.info(f"🔍 Availability Check - Attempt #{attempt}")

                try:
                    # Get fingerprint
                    fingerprint = stealth_config.get_ultra_random_fingerprint()
                    http_headers = stealth_config.get_random_http_headers(
                        fingerprint['locale'],
                        fingerprint['user_agent']
                    )

                    # Launch browser
                    self.browser = await p.chromium.launch(
                        headless=True,
                        args=[
                            '--disable-blink-features=AutomationControlled',
                            '--disable-dev-shm-usage',
                            '--no-sandbox',
                            '--disable-web-security',
                        ]
                    )

                    # Create context
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

                    # Add proxy if provided
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

                    self.context = await self.browser.new_context(**context_options)
                    self.page = await self.context.new_page()

                    # Apply stealth script
                    stealth_script = stealth_config.get_stealth_script()
                    await self.page.add_init_script(stealth_script)

                    # Navigate to URL
                    self.logger.info("📡 Navigating to booking page...")
                    await self.page.goto(self.start_url, wait_until='domcontentloaded', timeout=30000)
                    await asyncio.sleep(2)

                    # Handle cookie consent
                    await self._handle_cookie_consent()
                    await asyncio.sleep(1)

                    # Check for "Select modules" button
                    select_button_selectors = [
                        'text="Select modules"',
                        'button:has-text("Select modules")',
                        'a:has-text("Select modules")',
                        '[data-testid*="select-module"]',
                        '//button[contains(text(), "Select modules")]',
                        '//a[contains(text(), "Select modules")]'
                    ]

                    button_found = False
                    for selector in select_button_selectors:
                        try:
                            element = self.page.locator(selector)
                            count = await element.count()
                            if count > 0:
                                is_visible = await element.first.is_visible(timeout=2000)
                                if is_visible:
                                    self.logger.info("✅ 'Select modules' button FOUND and VISIBLE!")
                                    button_found = True
                                    break
                        except Exception:
                            continue

                    if button_found:
                        self.logger.info("🎉 BOOKING IS AVAILABLE! Proceeding to launch parallel instances...")
                        await self.browser.close()
                        return True
                    else:
                        self.logger.warning("❌ 'Select modules' button NOT found")

                        # Check for error messages
                        if await self._check_high_demand_error():
                            self.logger.warning("⚠️  High demand error detected")

                        if await self._check_finish_other_bookings_error():
                            self.logger.warning("⚠️  'Finish other bookings' error detected")

                        # Close browser and clear everything
                        await self.browser.close()

                        # Wait before retry
                        retry_delay = 5
                        self.logger.info(f"⏳ Waiting {retry_delay}s before retry (clearing cache/cookies)...")
                        await asyncio.sleep(retry_delay)

                except Exception as e:
                    self.logger.error(f"❌ Error during availability check: {str(e)}")
                    if self.browser:
                        await self.browser.close()
                    await asyncio.sleep(5)

    async def _handle_cookie_consent(self):
        """Handle cookie consent dialog if it appears."""
        try:
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
                        await button.click(timeout=5000)
                        await asyncio.sleep(1)
                        return True
                except Exception:
                    continue
            return False
        except Exception as e:
            self.logger.warning(f"Cookie consent handling warning: {str(e)}")
            return False

    async def _check_high_demand_error(self):
        """Check for 'very high demand' error message."""
        try:
            high_demand_text = await self.page.locator(
                "text=/very high demand|cannot be booked at the moment/i"
            ).first.text_content(timeout=2000)
            return bool(high_demand_text)
        except Exception:
            return False

    async def _check_finish_other_bookings_error(self):
        """Check for 'finish other started bookings' error message."""
        try:
            finish_bookings_text = await self.page.locator(
                "text=/finish other started bookings|Please finish other started bookings/i"
            ).first.text_content(timeout=2000)
            return bool(finish_bookings_text)
        except Exception:
            return False


class MultipleBrowserTest:
    """Test booking on multiple browsers with optimized performance."""

    def __init__(self, start_url: str, session_id: int, proxy: str = None,
                 gui_display_seconds: int = 5, account: dict = None,
                 keep_alive_hours: float = 2.0):
        self.start_url = start_url
        self.session_id = session_id
        self.proxy = proxy
        self.gui_display_seconds = gui_display_seconds
        self.account = account
        self.keep_alive_hours = keep_alive_hours
        self.page = None
        self.logger = logging.getLogger(f"Session-{session_id}")
        self.required_modules = ['reading']  # Simplified - only reading
        self.result = None
        self.duration = 0
        self.module_status = {}
        self.success_timestamp = None

    async def run_test(self):
        """Run the complete test with keep-alive for successful sessions."""
        async with async_playwright() as p:
            browser = None
            try:
                start_time = datetime.now()

                self.logger.info("=" * 60)
                self.logger.info(f"Starting test - Required modules: {', '.join(self.required_modules)}")

                # Get fingerprint
                fingerprint = stealth_config.get_ultra_random_fingerprint()
                http_headers = stealth_config.get_random_http_headers(
                    fingerprint['locale'],
                    fingerprint['user_agent']
                )

                if self.proxy:
                    self.logger.info(f"Using Proxy: {self.proxy}")

                # Launch browser
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

                # Create context
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

                # Add proxy if provided
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

                # Apply stealth script
                stealth_script = stealth_config.get_stealth_script()
                await self.page.add_init_script(stealth_script)

                # Navigate to URL
                self.logger.info("Navigating to booking page...")
                await self.page.goto(self.start_url, wait_until='domcontentloaded', timeout=30000)
                await asyncio.sleep(1)

                # Handle cookie consent
                await self._handle_cookie_consent()
                await asyncio.sleep(1)

                # Click "Select modules" button
                self.logger.info("Clicking 'Select modules' button...")
                if not await self._click_select_modules():
                    self.result = 'button_not_found'
                    end_time = datetime.now()
                    self.duration = (end_time - start_time).total_seconds()
                    return self.result

                await asyncio.sleep(2)

                # Check for errors
                if await self._check_high_demand_error():
                    self.result = 'high_demand_error'
                    end_time = datetime.now()
                    self.duration = (end_time - start_time).total_seconds()
                    return self.result

                if await self._check_finish_other_bookings_error():
                    self.result = 'bad_error'
                    end_time = datetime.now()
                    self.duration = (end_time - start_time).total_seconds()
                    return self.result

                # Check and validate checkboxes
                self.logger.info("Validating module checkboxes...")
                # validation_result = await self._check_and_validate_checkboxes()
                #
                # if validation_result in ('success', 'partial_success'):
                #     self.result = 'success'
                #     self.success_timestamp = datetime.now()
                #
                #     # Show GUI and keep session alive
                await self._show_success_gui_and_keep_alive(context, p)
                # elif validation_result == 'checkbox_error':
                #     self.result = 'checkbox_error'
                # else:
                #     self.result = 'unknown_error'

                end_time = datetime.now()
                self.duration = (end_time - start_time).total_seconds()

                self.logger.info(f"Test completed - Result: {self.result} - Duration: {self.duration:.2f}s")
                return self.result

            except Exception as e:
                self.logger.error(f"Exception occurred: {str(e)}")
                self.result = 'exception'
                end_time = datetime.now()
                self.duration = (end_time - start_time).total_seconds() if 'start_time' in locals() else 0
                return self.result

            finally:
                if browser:
                    # await browser.close()
                    pass
    async def _show_success_gui_and_keep_alive(self, context_headless, playwright_instance):
        """Show GUI and keep the successful session alive for specified hours."""
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

            self.logger.info(f"🖥️  Opening GUI browser and keeping alive for {self.keep_alive_hours} hours...")

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

            await page_gui.goto(checkpoint_url, wait_until='domcontentloaded', timeout=30000)
            self.logger.info(f"✅ GUI browser opened at checkpoint")

            await asyncio.sleep(1)
            await self._handle_cookie_consent_on_page(page_gui)

            # Perform booking steps
            await self._complete_booking_flow(page_gui)

            # Keep alive for specified hours
            keep_alive_seconds = self.keep_alive_hours * 3600
            end_time = datetime.now() + timedelta(seconds=keep_alive_seconds)

            self.logger.info(f"⏰ Keeping session alive until {end_time.strftime('%Y-%m-%d %H:%M:%S')}")

            # Periodic activity to keep session alive
            while datetime.now() < end_time:
                remaining = (end_time - datetime.now()).total_seconds()
                self.logger.info(f"⏳ Session alive - {remaining / 60:.1f} minutes remaining...")

                # Gentle page activity every 5 minutes
                await asyncio.sleep(300)
                try:
                    await page_gui.evaluate("() => { window.scrollBy(0, 10); window.scrollBy(0, -10); }")
                except:
                    pass

            self.logger.info("⏰ Keep-alive period ended")
            await browser_gui.close()
            self.logger.info("🔒 GUI browser closed")

        except Exception as e:
            self.logger.error(f"Error in GUI and keep-alive: {str(e)}")

    async def _complete_booking_flow(self, page):
        """Complete the booking flow steps."""
        cookie_selectors = [
            "button:has-text('Accept All')",
            "text=/accept all/i",
            "[data-testid*='accept']",
            "button[class*='accept']",
            "//button[contains(text(), 'Accept')]"
        ]

        continue_selectors = [
            "button[name='continue']",
            "button:has-text('Continue')",
            "text=/^continue$/i",
            "[data-testid*='continue']",
            "//button[contains(text(), 'Continue')]"
        ]

        # # Step 1: Click Continue
        # self.logger.info("Step 1: Clicking Continue...")
        # for selector in continue_selectors:
        #     try:
        #         await page.wait_for_selector(selector, state="visible", timeout=10000)
        #         await page.click(selector, timeout=10000)
        #         self.logger.info("✅ Clicked Continue")
        #         await asyncio.sleep(3)
        #         break
        #     except:
        #         continue

        await self._handle_cookie_consent_on_page(page)

        # # Step 2: Book for myself
        # self.logger.info("Step 2: Clicking 'Book for myself'...")
        # book_selectors = [
        #     "button#i4d2d",
        #     "button:has-text('BOOK FOR MYSELF')",
        #     "text=/book for myself/i"
        # ]
        #
        # for selector in book_selectors:
        #     try:
        #         await page.wait_for_selector(selector, state="visible", timeout=10000)
        #         await page.click(selector, timeout=10000)
        #         self.logger.info("✅ Clicked 'Book for myself'")
        #         await asyncio.sleep(3)
        #         break
        #     except:
        #         continue

        # await self._handle_cookie_consent_on_page(page)

        # Step 3: Login
        # if self.account:
        #     self.logger.info("Step 3: Logging in...")
        #     try:
        #         await page.wait_for_selector("input#username", timeout=15000)
        #         await page.fill("input#username", self.account['id'])
        #         await asyncio.sleep(1)
        #         await page.fill("input#password", self.account['password'])
        #         await asyncio.sleep(1)
        #         await page.click("input[name='submit'][value='Log in']")
        #         self.logger.info("✅ Login completed")
        #         await asyncio.sleep(5)
        #
        #         # Handle discard dialog
        #         try:
        #             discard_button = page.locator("text=/discard other booking/i")
        #             if await discard_button.count() > 0:
        #                 await discard_button.click(timeout=5000)
        #                 await asyncio.sleep(2)
        #         except:
        #             pass
        #
        #     except Exception as e:
        #         self.logger.error(f"Login failed: {str(e)}")
        #
        # # Continue with remaining steps...
        # self.logger.info("✅ Booking flow completed - Session at payment page")

    async def _handle_cookie_consent(self):
        """Handle cookie consent on current page."""
        return await self._handle_cookie_consent_on_page(self.page)

    async def _handle_cookie_consent_on_page(self, page):
        """Handle cookie consent on specified page."""
        try:
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
                        await button.click(timeout=5000)
                        await asyncio.sleep(1)
                        return True
                except:
                    continue
            return False
        except Exception as e:
            self.logger.warning(f"Cookie consent handling: {str(e)}")
            return False

    async def _click_select_modules(self):
        """Click the 'Select modules' button."""
        select_button_selectors = [
            'text="Select modules"',
            'button:has-text("Select modules")',
            'a:has-text("Select modules")',
        ]

        for selector in select_button_selectors:
            try:
                await self.page.click(selector, timeout=5000)
                self.logger.info("✅ 'Select modules' button clicked")
                return True
            except:
                continue

        self.logger.error("❌ Could not click 'Select modules' button")
        return False

    async def _check_high_demand_error(self):
        """Check for high demand error."""
        try:
            text = await self.page.locator(
                "text=/very high demand|cannot be booked at the moment/i"
            ).first.text_content(timeout=2000)
            if text:
                self.logger.error("❌ HIGH DEMAND ERROR")
                return True
        except:
            pass
        return False

    async def _check_finish_other_bookings_error(self):
        """Check for finish bookings error."""
        try:
            text = await self.page.locator(
                "text=/finish other started bookings|Please finish other started bookings/i"
            ).first.text_content(timeout=2000)
            if text:
                self.logger.error("❌ BAD ERROR")
                return True
        except:
            pass
        return False

    async def _check_and_validate_checkboxes(self):
        """Check module availability."""
        try:
            await self.page.wait_for_selector('.cs-input__checkboxes-wrapper', timeout=15000)

            for module in ['reading', 'listening', 'writing', 'speaking']:
                self.module_status[module] = await self._get_module_status(module)

            available_modules = [
                m for m, status in self.module_status.items()
                if status.get('available', False)
            ]

            if available_modules:
                self.logger.info(f"✅ Available modules: {', '.join(available_modules)}")
                return 'partial_success'
            else:
                self.logger.error("❌ No modules available")
                return 'checkbox_error'
        except Exception as e:
            self.logger.error(f"Error checking checkboxes: {str(e)}")
            return None

    async def _get_module_status(self, module_name: str):
        """Get module availability status."""
        try:
            checkbox_selector = f'input[id="{module_name}"]'
            checkbox = await self.page.query_selector(checkbox_selector)

            if not checkbox:
                return {'exists': False, 'available': False, 'checked': False}

            is_disabled = await checkbox.get_attribute('disabled')
            is_checked = await checkbox.get_attribute('checked')

            label_selector = f'label[for="{module_name}"]'
            label = await self.page.query_selector(label_selector)

            is_fully_booked = False
            if label:
                label_text = await label.text_content()
                if label_text and 'fully booked' in label_text.lower():
                    is_fully_booked = True

            return {
                'exists': True,
                'available': not is_disabled and not is_fully_booked,
                'checked': is_checked is not None,
                'disabled': is_disabled is not None,
                'fully_booked': is_fully_booked
            }
        except Exception as e:
            self.logger.error(f"Error reading module status for {module_name}: {e}")
            return {'exists': False, 'available': False, 'checked': False}


class MultipleTestManager:
    """Manage multiple parallel browser tests with availability pre-check."""

    def __init__(self, start_url: str, num_sessions: int, proxies: list = None,
                 gui_display_seconds: int = 5, accounts: list = None,
                 keep_alive_hours: float = 2.0):
        self.start_url = start_url
        self.num_sessions = num_sessions
        self.proxies = proxies or []
        self.gui_display_seconds = gui_display_seconds
        self.accounts = accounts or []
        self.keep_alive_hours = keep_alive_hours
        self.sessions = []
        self.results = {}
        self.logger = logging.getLogger("Manager")

    async def run_with_availability_check(self):
        """Run availability check first, then launch all parallel instances."""
        self.logger.info("=" * 80)
        self.logger.info("STEP 1: CHECKING BOOKING AVAILABILITY")
        self.logger.info("=" * 80)

        # Use first proxy for availability check
        proxy = self.proxies[0] if self.proxies else None

        # Run availability checker
        checker = AvailabilityChecker(self.start_url, proxy)
        is_available = await checker.check_availability()

        if not is_available:
            self.logger.error("❌ Availability check failed")
            return

        self.logger.info("\n" + "=" * 80)
        self.logger.info("STEP 2: LAUNCHING PARALLEL INSTANCES")
        self.logger.info("=" * 80)
        self.logger.info(f"🚀 Starting {self.num_sessions} parallel browser tests")
        if self.proxies:
            self.logger.info(f"🌐 Using {len(self.proxies)} authenticated proxies")
        self.logger.info(f"⏰ Successful sessions will be kept alive for {self.keep_alive_hours} hours")
        self.logger.info("=" * 80 + "\n")

        # Run all parallel sessions
        await self.run_all_parallel()

    async def run_single_session(self, session_id: int):
        """Run a single test session."""
        proxy = None
        if self.proxies:
            proxy_index = (session_id - 1) % len(self.proxies)
            proxy = self.proxies[proxy_index]

        account = None
        if self.accounts:
            account_index = (session_id - 1) % len(self.accounts)
            account = self.accounts[account_index]

        test = MultipleBrowserTest(
            self.start_url, session_id, proxy,
            self.gui_display_seconds, account, self.keep_alive_hours
        )
        await test.run_test()

        self.results[session_id] = {
            'session_id': session_id,
            'result': test.result,
            'duration': test.duration,
            'required_modules': test.required_modules,
            'module_status': test.module_status,
            'proxy': proxy,
            'success_timestamp': test.success_timestamp
        }

    async def run_all_parallel(self):
        """Run all test sessions in parallel."""
        tasks = [
            self.run_single_session(i + 1)
            for i in range(self.num_sessions)
        ]

        await asyncio.gather(*tasks, return_exceptions=True)
        self.print_statistics()

    def print_statistics(self):
        """Print comprehensive statistics."""
        self.logger.info("\n" + "=" * 80)
        self.logger.info("FINAL STATISTICS")
        self.logger.info("=" * 80)

        result_counts = {
            'success': 0,
            'high_demand_error': 0,
            'bad_error': 0,
            'checkbox_error': 0,
            'exception': 0,
            'unknown_error': 0,
            'button_not_found': 0
        }

        total_duration = 0

        for session_id, data in sorted(self.results.items()):
            result = data.get('result')
            if result and result in result_counts:
                result_counts[result] += 1
            duration = data.get('duration', 0)
            total_duration += duration

        # Print session results
        self.logger.info("\nSESSION-BY-SESSION RESULTS:")
        self.logger.info("-" * 80)

        for session_id, data in sorted(self.results.items()):
            result_emoji = {
                'success': '✅',
                'high_demand_error': '❌',
                'bad_error': '❌',
                'checkbox_error': '❌',
                'exception': '❌',
                'unknown_error': '❌',
                'button_not_found': '❌'
            }

            emoji = result_emoji.get(data.get('result'), '❓')
            result_str = data.get('result', 'unknown')
            duration = data.get('duration', 0)
            modules = data.get('required_modules', [])
            modules_str = ', '.join([m.upper() for m in modules]) if modules else 'N/A'

            timestamp_str = ""
            if data.get('success_timestamp'):
                timestamp_str = f" | Started: {data['success_timestamp'].strftime('%H:%M:%S')}"

            self.logger.info(f"Session {session_id:2d}: {emoji} {result_str:20s} | "
                             f"Duration: {duration:6.2f}s{timestamp_str}")

        # Print summary
        avg_duration = total_duration / self.num_sessions if self.num_sessions > 0 else 0
        success_pct = (result_counts['success'] / self.num_sessions * 100) if self.num_sessions > 0 else 0
        high_demand_pct = (result_counts['high_demand_error'] / self.num_sessions * 100) if self.num_sessions > 0 else 0
        bad_error_pct = (result_counts['bad_error'] / self.num_sessions * 100) if self.num_sessions > 0 else 0
        checkbox_pct = (result_counts['checkbox_error'] / self.num_sessions * 100) if self.num_sessions > 0 else 0
        button_pct = (result_counts['button_not_found'] / self.num_sessions * 100) if self.num_sessions > 0 else 0
        exception_pct = (result_counts['exception'] / self.num_sessions * 100) if self.num_sessions > 0 else 0
        unknown_pct = (result_counts['unknown_error'] / self.num_sessions * 100) if self.num_sessions > 0 else 0
        try :
            self.logger.info("\n" + "-" * 80)
            self.logger.info("RESULT SUMMARY:")
            self.logger.info("-" * 80)
            self.logger.info(f"✅ Success:               {result_counts['success']:3d} ({success_pct:5.1f}%)")
            self.logger.info(f"❌ High Demand Error:     {result_counts['high_demand_error']:3d} ({high_demand_pct:5.1f}%)")
            self.logger.info(f"❌ Bad Error:             {result_counts['bad_error']:3d} ({bad_error_pct:5.1f}%)")
            self.logger.info(f"❌ Checkbox Error:        {result_counts['checkbox_error']:3d} ({checkbox_pct:5.1f}%)")
            self.logger.info(f"❌ Button Not Found:      {result_counts['button_not_found']:3d} ({button_pct:5.1f}%)")
            self.logger.info(f"❌ Exception:             {result_counts['exception']:3d} ({exception_pct:5.1f}%)")
            self.logger.info(f"❌ Unknown Error:         {result_counts['unknown_error']:3d} ({unknown_pct:5.1f}%)")
            self.logger.info(f"\nTotal Sessions:           {self.num_sessions}")
            self.logger.info(f"Average Duration:         {avg_duration:.2f}s")
            self.logger.info(f"Total Duration:           {total_duration:.2f}s")
        except Exception as e:
            print(e)

        # Print keep-alive info for successful sessions
        successful_sessions = [
            data for data in self.results.values()
            if data['result'] == 'success' and data.get('success_timestamp')
        ]

        if successful_sessions:
            self.logger.info("\n" + "-" * 80)
            self.logger.info(f"KEEP-ALIVE INFO ({len(successful_sessions)} successful sessions):")
            self.logger.info("-" * 80)
            for data in successful_sessions:
                end_time = data['success_timestamp'] + timedelta(hours=self.keep_alive_hours)
                self.logger.info(
                    f"Session {data['session_id']:2d}: Alive until {end_time.strftime('%Y-%m-%d %H:%M:%S')}")

        self.logger.info("\n" + "=" * 80)


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def generate_authenticated_proxies(num_proxies: int = 1000):
    """Generate authenticated proxy addresses using Decodo proxy service."""
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
    print(f"   Using Decodo proxy service: {proxy_host}")
    print(f"   Port range: {base_port} - {base_port + num_proxies - 1}")
    return proxies


def load_accounts(accounts_file: str = "accounts.json"):
    """Load accounts from JSON file."""
    try:
        if not os.path.exists(accounts_file):
            print(f"⚠️  Accounts file '{accounts_file}' not found. Running without login.")
            return []

        with open(accounts_file, 'r') as f:
            accounts = json.load(f)

        print(f"✅ Loaded {len(accounts)} accounts from {accounts_file}")
        return accounts
    except Exception as e:
        print(f"❌ Error loading accounts: {str(e)}")
        return []


# ============================================================================
# MAIN EXECUTION
# ============================================================================

async def main():
    """Main entry point."""

    # Configuration
    start_url = 'https://www.goethe.de/ins/in/en/spr/prf/gzb2.cfm?examId=5F0ECCDAD6DAF286DCD85E927E980A007AD2D729EB97AEB101AC05F9D79098F88FCDEA998D10794BDAECAFD703DE4980EBADDBC3538C549CA62C8617CC83CFE6'
    gui_display_seconds = 2000
    keep_alive_hours = 2.0  # Keep successful sessions alive for 2 hours

    # Generate proxies and load accounts
    proxies = generate_authenticated_proxies(num_proxies=100)
    # proxies = []
    accounts = load_accounts("accounts.json")

    print("\n" + "=" * 80)
    print("OPTIMIZED MULTIPLE BROWSER TEST WITH AVAILABILITY PRE-CHECK")
    print("=" * 80)
    print("Key Features:")
    print("  ✅ Pre-check: Waits for 'Select modules' button before launching")
    print("  ✅ Auto-retry: Clears cache/cookies and retries until available")
    print("  ✅ Smart launch: All parallel instances start only when ready")
    print("  ✅ Keep-alive: Successful sessions maintained for 2 hours")
    print("  ✅ Optimized: Reduced redundant checks and improved performance")
    print("  ✅ Stealth: Ultra-random fingerprints per session")
    print("=" * 80)
    print(f"Proxies: {len(proxies)} authenticated proxies (Decodo)")
    print(f"Accounts: {len(accounts)} loaded from accounts.json")
    print(f"Keep-alive: {keep_alive_hours} hours for successful sessions")
    print("=" * 80)

    try:
        n = int(input("\nEnter number of parallel browsers (N): "))
        if n <= 0:
            print("❌ Number must be greater than 0")
            return
    except ValueError:
        print("❌ Invalid input. Please enter a number.")
        return

    print(f"\n🚀 Configuration:")
    print(f"   • Parallel Sessions: {n}")
    print(f"   • Proxies: {len(proxies)}")
    print(f"   • Accounts: {len(accounts)}")
    print(f"   • Keep-Alive: {keep_alive_hours} hours")
    print(f"   • GUI Display: {gui_display_seconds} seconds on success")
    print("\n" + "=" * 80)
    print("STARTING AVAILABILITY CHECK...")
    print("=" * 80 + "\n")

    # Create and run manager with availability check
    manager = MultipleTestManager(
        start_url, n, proxies, gui_display_seconds, accounts, keep_alive_hours
    )
    await manager.run_with_availability_check()

    print("\n✅ All tests completed!")
    print(f"💡 Successful sessions will remain active for {keep_alive_hours} hours")
    print("   You can monitor them in the GUI windows that remain open.")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user.")
    except Exception as e:
        print(f"\n\n❌ Fatal error: {str(e)}")