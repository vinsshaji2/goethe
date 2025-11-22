"""
Multiple Browser Test Script
Runs booking tests on N parallel browsers with random module selection
Provides comprehensive statistics of all test results
"""

import asyncio
import logging
import json
from datetime import datetime
from playwright.async_api import async_playwright
from vins import stealth_config
import os


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [Session-%(name)s] - %(levelname)s - %(message)s'
)


class MultipleBrowserTest:
    """Test booking on multiple browsers with random module selection."""
    
    def __init__(self, start_url: str, session_id: int, headless: bool = False, proxy: str = None, gui_display_seconds: int = 5, account: dict = None):
        """
        Initialize browser test session.
        
        Args:
            start_url: The URL to start from
            session_id: Unique session identifier
            headless: Whether to run in headless mode (ignored - always starts headless)
            proxy: Proxy server address (format: "host:port")
            gui_display_seconds: How many seconds to display GUI on success
            account: Account credentials dict with 'id' and 'password' keys
        """
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
        """Generate fixed module selection: listening, writing, speaking (excluding reading)."""
        # Always use these three modules for all sessions
        # selected = ['listening', 'reading', 'writing', 'speaking']
        selected = ['reading']
        return selected
    
    async def handle_cookie_consent(self):
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
                    button = self.page.locator(selector)
                    if await button.count() > 0:
                        self.logger.info("Cookie consent dialog found, clicking Accept All")
                        await button.click(timeout=5000)
                        await asyncio.sleep(1)
                        return True
                except Exception:
                    continue
            
            self.logger.info("No cookie consent dialog found (already accepted or not present)")
            return False
            
        except Exception as e:
            self.logger.warning(f"Cookie consent handling warning: {str(e)}")
            return False
    
    async def check_high_demand_error(self):
        """Check for 'very high demand' error message."""
        try:
            high_demand_text = await self.page.locator("text=/very high demand|cannot be booked at the moment/i").first.text_content(timeout=2000)
            if high_demand_text:
                self.logger.error("❌ HIGH DEMAND ERROR DETECTED")
                return True
        except Exception:
            pass
        return False
    
    async def check_finish_other_bookings_error(self):
        """Check for 'finish other started bookings' error message."""
        try:
            finish_bookings_text = await self.page.locator("text=/finish other started bookings|Please finish other started bookings/i").first.text_content(timeout=2000)
            if finish_bookings_text:
                self.logger.error("❌ BAD ERROR DETECTED")
                return True
        except Exception:
            pass
        return False

    async def get_module_status(self, module_name: str):
        """Get the availability status of a specific module."""
        try:
            # Fixed selector (removed spaces)
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

    async def check_and_validate_checkboxes(self):
        """Check if at least one required module is available."""
        try:
            pass
            # await self.page.wait_for_selector('.cs-input__checkboxes-wrapper', timeout=15000)
            #
            # # Get status for all modules
            # for module in ['reading', 'listening', 'writing', 'speaking']:
            #     self.module_status[module] = await self.get_module_status(module)
            #
            # available_modules = [
            #     m for m, status in self.module_status.items()
            #     if status.get('available', False)
            # ]
            # unavailable_modules = [
            #     m for m, status in self.module_status.items()
            #     if not status.get('available', False)
            # ]
            #
            # if available_modules:
            #     self.logger.info(f"✅ SUCCESS: Available modules: {', '.join(available_modules)}")
            #     if unavailable_modules:
            #         self.logger.warning(f"⚠️ Unavailable modules: {', '.join(unavailable_modules)}")
            #     return 'partial_success'
            # else:
            #     self.logger.error("❌ No modules available at this time")
            #     return 'checkbox_error'

        except Exception as e:
            self.logger.error(f"Error checking checkboxes: {str(e)}")
            return None

    async def show_success_gui_at_checkpoint(self, context_headless, playwright_instance, display_seconds: int = 5):
        """
        Show GUI browser at the exact checkpoint where success occurred with preserved session state.
        
        Args:
            context_headless: The headless browser context that achieved success
            playwright_instance: The Playwright instance to launch new browser
            display_seconds: How many seconds to display the GUI
        """
        try:
            # Save the current checkpoint URL
            checkpoint_url = self.page.url
            self.logger.info(f"💾 Saving session state from checkpoint: {checkpoint_url}")
            
            # Save the complete session state (cookies, localStorage, sessionStorage)
            storage_state = await context_headless.storage_state()
            self.logger.info("✅ Session state saved successfully")
            
            # Get the fingerprint for GUI browser
            fingerprint = stealth_config.get_ultra_random_fingerprint()
            http_headers = stealth_config.get_random_http_headers(
                fingerprint['locale'],
                fingerprint['user_agent']
            )
            
            # Launch a new visible browser with saved session state
            self.logger.info(f"🖥️  Opening GUI browser at checkpoint for {display_seconds} seconds...")
            
            browser_gui = await playwright_instance.chromium.launch(
                headless=False,  # GUI mode
                slow_mo=50,
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--disable-dev-shm-usage',
                    '--no-sandbox',
                    '--disable-web-security',
                ]
            )
            
            # Create context with fingerprint, proxy, and restored session state
            context_options = {
                'viewport': fingerprint['viewport'],
                'user_agent': fingerprint['user_agent'],
                'locale': fingerprint['locale'],
                'timezone_id': fingerprint['timezone_id'],
                'permissions': [],
                'storage_state': storage_state,  # Restore cookies/localStorage/sessionStorage
                'ignore_https_errors': True,
                'java_script_enabled': True,
                'device_scale_factor': fingerprint['device_scale_factor'],
                'has_touch': fingerprint['has_touch'],
                'is_mobile': False,
                'color_scheme': fingerprint['color_scheme'],
                'extra_http_headers': http_headers
            }
            
            # Add proxy if provided (with authentication)
            if self.proxy:
                # Proxy format: username:password@host:port
                # Parse username, password, host, port
                if '@' in self.proxy:
                    auth_part, server_part = self.proxy.split('@')
                    username, password = auth_part.split(':')
                    context_options['proxy'] = {
                        'server': f'http://{server_part}',
                        'username': username,
                        'password': password
                    }
                else:
                    # No authentication
                    context_options['proxy'] = {
                        'server': f'http://{self.proxy}'
                    }
            
            context_gui = await browser_gui.new_context(**context_options)
            page_gui = await context_gui.new_page()
            
            # Apply stealth script
            stealth_script = stealth_config.get_stealth_script()
            await page_gui.add_init_script(stealth_script)
            
            # Navigate to the checkpoint URL with preserved session
            await page_gui.goto(checkpoint_url, wait_until='domcontentloaded', timeout=300000)
            self.logger.info(f"✅ GUI browser opened at checkpoint with preserved session state")
            
            # Handle cookie consent if it appears
            self.logger.info("Checking for cookie consent dialog...")
            await asyncio.sleep(1)
            cookie_accept_selectors = [
                "button:has-text('Accept All')",
                "text=/accept all/i",
                "[data-testid*='accept']",
                "button[class*='accept']",
                "//button[contains(text(), 'Accept')]"
            ]
            
            for selector in cookie_accept_selectors:
                try:
                    button = page_gui.locator(selector)
                    if await button.count() > 0:
                        self.logger.info("Cookie consent dialog found, clicking Accept All")
                        await button.click(timeout=5000)
                        await asyncio.sleep(1)
                        self.logger.info("✅ Accepted cookies")
                        break
                except Exception:
                    continue

            # Sleep before the next action
            await asyncio.sleep(20000000000000000)

            # Step 3: Click continue button (after selecting modules)
            self.logger.info("Attempting to click 'Continue' button...")
            continue_selectors = [
                "button[name='continue']",
                "button:has-text('Continue')",
                "text=/^continue$/i",
                "[data-testid*='continue']",
                "//button[contains(text(), 'Continue')]",
                "input[type='submit'][value*='Continue']",
                "button[type='button']:has-text('Continue')"
            ]
            
            continue_clicked = False
            for selector in continue_selectors:
                try:
                    await page_gui.wait_for_selector(selector, state="visible", timeout=10000)
                    await page_gui.click(selector, timeout=10000)
                    self.logger.info(f"✅ Successfully clicked 'Continue' button")
                    continue_clicked = True
                    break
                except Exception:
                    continue
            
            if not continue_clicked:
                self.logger.warning("⚠️  Could not find 'Continue' button")
            else:
                # Wait for navigation after continue (increased for slow proxies)
                await asyncio.sleep(3)
                
                # Check for cookie consent after Step 3
                self.logger.info("Checking for cookie consent after Step 3...")
                await asyncio.sleep(1)
                for selector in cookie_accept_selectors:
                    try:
                        button = page_gui.locator(selector)
                        if await button.count() > 0:
                            self.logger.info("Cookie consent dialog found after Step 3, clicking Accept All")
                            await button.click(timeout=5000)
                            await asyncio.sleep(1)
                            self.logger.info("✅ Accepted cookies after Step 3")
                            break
                    except Exception:
                        continue
                
                # Step 4: Book for myself
                self.logger.info("Attempting to click 'Book for myself' button...")
                book_for_myself_selectors = [
                    "button#i4d2d",
                    "button:has-text('BOOK FOR MYSELF')",
                    "text=/book for myself/i",
                    "button[class*='cs-button'][class*='cs-layer__button']",
                    "[data-testid*='book-myself']",
                    "//button[contains(text(), 'BOOK FOR MYSELF')]"
                ]
                
                book_clicked = False
                for selector in book_for_myself_selectors:
                    try:
                        await page_gui.wait_for_selector(selector, state="visible", timeout=10000)
                        await page_gui.click(selector, timeout=10000)
                        self.logger.info(f"✅ Successfully clicked 'Book for myself' button")
                        book_clicked = True
                        break
                    except Exception:
                        continue
                
                if not book_clicked:
                    self.logger.warning("⚠️  Could not find 'Book for myself' button")
                else:
                    # Wait for navigation after book for myself (increased for slow proxies)
                    await asyncio.sleep(3)
                    
                    # Check for cookie consent after Step 4
                    self.logger.info("Checking for cookie consent after Step 4...")
                    await asyncio.sleep(1)
                    for selector in cookie_accept_selectors:
                        try:
                            button = page_gui.locator(selector)
                            if await button.count() > 0:
                                self.logger.info("Cookie consent dialog found after Step 4, clicking Accept All")
                                await button.click(timeout=5000)
                                await asyncio.sleep(1)
                                self.logger.info("✅ Accepted cookies after Step 4")
                                break
                        except Exception:
                            continue
                    
                    # Step 5: Login
                    if self.account:
                        self.logger.info("Step 5: Attempting to login...")
                        try:
                            # Wait for login form (increased timeout for slow proxies)
                            await page_gui.wait_for_selector("input#username", timeout=15000)
                            self.logger.info("Login form found")
                            
                            # Fill email
                            await page_gui.fill("input#username", self.account['id'])
                            self.logger.info(f"Filled email: {self.account['id']}")
                            await asyncio.sleep(1)
                            
                            # Fill password
                            await page_gui.fill("input#password", self.account['password'])
                            self.logger.info("Filled password")
                            await asyncio.sleep(1)
                            
                            # Click login button
                            await page_gui.click("input[name='submit'][value='Log in']")
                            self.logger.info("Clicked login button")
                            await asyncio.sleep(5)
                            
                            # Handle session dialog if present
                            try:
                                discard_button = page_gui.locator("text=/discard other booking/i")
                                if await discard_button.count() > 0:
                                    self.logger.info("Session dialog detected, clicking 'Discard other booking'")
                                    await discard_button.click(timeout=5000)
                                    await asyncio.sleep(2)
                            except Exception:
                                pass
                            
                            self.logger.info("✅ Login completed successfully")
                            
                            # Step 6: Handle "Discard other booking" dialog if it appears (additional check)
                            self.logger.info("Step 6: Checking for additional 'Discard other booking' dialog...")
                            await asyncio.sleep(2)
                            try:
                                discard_selectors = [
                                    "button:has-text('DISCARD OTHER BOOKING')",
                                    "text=/discard other booking/i",
                                    "button:has-text('Discard other booking')",
                                    "//button[contains(text(), 'DISCARD OTHER BOOKING')]",
                                    "button[class*='cs-button']:has-text('DISCARD')"
                                ]
                                
                                for selector in discard_selectors:
                                    try:
                                        button = page_gui.locator(selector)
                                        if await button.count() > 0:
                                            self.logger.info("Found additional 'Discard other booking' dialog, clicking...")
                                            await button.click(timeout=5000)
                                            self.logger.info("✅ Successfully clicked 'Discard other booking'")
                                            await asyncio.sleep(2)
                                            break
                                    except Exception:
                                        continue
                            except Exception as e:
                                self.logger.info(f"No additional discard dialog (normal): {str(e)}")
                            
                            # Step 7: Additional continues and navigation
                            self.logger.info("Step 7: Clicking continue (Booking)...")
                            continue_clicked_booking = False
                            for selector in continue_selectors:
                                try:
                                    await page_gui.wait_for_selector(selector, state="visible", timeout=10000)
                                    await page_gui.click(selector, timeout=10000)
                                    self.logger.info(f"✅ Successfully clicked 'Continue' (Booking)")
                                    continue_clicked_booking = True
                                    await asyncio.sleep(3)
                                    break
                                except Exception:
                                    continue
                            
                            if not continue_clicked_booking:
                                self.logger.warning("⚠️  Could not find Continue button (Booking)")
                            
                            # Click continue (Payment)
                            self.logger.info("Step 7: Clicking continue (Payment)...")
                            continue_clicked_payment = False
                            for selector in continue_selectors:
                                try:
                                    await page_gui.wait_for_selector(selector, state="visible", timeout=10000)
                                    await page_gui.click(selector, timeout=10000)
                                    self.logger.info(f"✅ Successfully clicked 'Continue' (Payment)")
                                    continue_clicked_payment = True
                                    await asyncio.sleep(3)
                                    break
                                except Exception:
                                    continue
                            
                            if not continue_clicked_payment:
                                self.logger.warning("⚠️  Could not find Continue button (Payment)")
                            
                            # Step 8: Handle payment (stops at payment page)
                            self.logger.info("Step 8: Starting payment process...")
                            order_selectors = [
                                "button#MFBAYXaHYKSrnuxTmzU",
                                "button:has-text('ORDER, SUBJECT TO CHARGE')",
                                "text=/order.*subject.*charge/i",
                                "button[class*='cs-button'][class*='arrow_next']",
                                "//button[contains(text(), 'ORDER') and contains(text(), 'CHARGE')]"
                            ]
                            
                            order_clicked = False
                            for selector in order_selectors:
                                try:
                                    await page_gui.wait_for_selector(selector, state="visible", timeout=10000)
                                    await page_gui.click(selector, timeout=10000)
                                    self.logger.info("✅ Successfully clicked 'ORDER, SUBJECT TO CHARGE' button")
                                    self.logger.info("✅ Reached payment page - BOOKING SUCCESSFUL!")
                                    order_clicked = True
                                    await asyncio.sleep(5)
                                    break
                                except Exception:
                                    continue
                            
                            if not order_clicked:
                                self.logger.warning("⚠️  Could not click 'ORDER, SUBJECT TO CHARGE' button")
                            else:
                                self.logger.info("="*60)
                                self.logger.info("✅✅✅ BOOKING PROCESS COMPLETED SUCCESSFULLY! ✅✅✅")
                                self.logger.info("="*60)
                            
                        except Exception as e:
                            self.logger.error(f"Login or subsequent steps failed: {str(e)}")
                    else:
                        self.logger.warning("⚠️  No account credentials provided, skipping login")
            
            # Wait for 15 seconds
            self.logger.info("⏳ Waiting 15 seconds...")
            await asyncio.sleep(15)
            
            # Close GUI browser
            await browser_gui.close()
            self.logger.info("🔒 GUI browser closed")
            
        except Exception as e:
            self.logger.error(f"Error showing GUI at checkpoint: {str(e)}")
    
    async def run_test(self):
        """Run the complete test."""
        async with async_playwright() as p:
            browser = None
            try:
                start_time = datetime.now()
                
                self.logger.info("="*60)
                self.logger.info(f"Starting test - Required modules: {', '.join(self.required_modules)}")
                
                # Get ultra-random fingerprint
                fingerprint = stealth_config.get_ultra_random_fingerprint()
                http_headers = stealth_config.get_random_http_headers(
                    fingerprint['locale'],
                    fingerprint['user_agent']
                )
                
                self.logger.info(f"Fingerprint: {fingerprint['user_agent'][:50]}...")
                self.logger.info(f"Viewport: {fingerprint['viewport']['width']}x{fingerprint['viewport']['height']}")
                if self.proxy:
                    self.logger.info(f"Using Proxy: {self.proxy}")
                
                # Launch browser (always start headless)
                browser = await p.chromium.launch(
                    headless=True,  # Always start in headless mode
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
                    'storage_state': None,
                    'ignore_https_errors': True,
                    'java_script_enabled': True,
                    'device_scale_factor': fingerprint['device_scale_factor'],
                    'has_touch': fingerprint['has_touch'],
                    'is_mobile': False,
                    'color_scheme': fingerprint['color_scheme'],
                    'extra_http_headers': http_headers
                }
                
                # Add proxy if provided (with authentication)
                if self.proxy:
                    # Proxy format: username:password@host:port
                    # Parse username, password, host, port
                    if '@' in self.proxy:
                        auth_part, server_part = self.proxy.split('@')
                        username, password = auth_part.split(':')
                        context_options['proxy'] = {
                            'server': f'http://{server_part}',
                            'username': username,
                            'password': password
                        }
                    else:
                        # No authentication
                        context_options['proxy'] = {
                            'server': f'http://{self.proxy}'
                        }
                
                context = await browser.new_context(**context_options)
                
                await context.clear_cookies()
                await context.clear_permissions()
                
                self.page = await context.new_page()
                
                # Apply stealth script
                stealth_script = stealth_config.get_stealth_script()
                await self.page.add_init_script(stealth_script)
                
                # Navigate to URL
                self.logger.info("Navigating to booking page...")
                await self.page.goto(self.start_url, wait_until='domcontentloaded', timeout=300000)
                await asyncio.sleep(1)
                
                # Handle cookie consent first
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
                
                if await self.check_high_demand_error():
                    self.result = 'high_demand_error'
                    end_time = datetime.now()
                    self.duration = (end_time - start_time).total_seconds()
                    return self.result
                
                if await self.check_finish_other_bookings_error():
                    self.result = 'bad_error'
                    end_time = datetime.now()
                    self.duration = (end_time - start_time).total_seconds()
                    return self.result
                
                # Check and validate checkboxes
                self.logger.info("Validating module checkboxes...")
                # validation_result = await self.check_and_validate_checkboxes()

                # if validation_result in ('success', 'partial_success'):
                #     self.result = 'success'
                await self.show_success_gui_at_checkpoint(context, p, display_seconds=self.gui_display_seconds)
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
                    await browser.close()


class MultipleTestManager:
    """Manage multiple parallel browser tests."""
    
    def __init__(self, start_url: str, num_sessions: int, headless: bool = False, proxies: list = None, gui_display_seconds: int = 5, accounts: list = None):
        """
        Initialize manager.
        
        Args:
            start_url: The booking URL
            num_sessions: Number of parallel browser sessions
            headless: Whether to run browsers in headless mode (ignored - always starts headless)
            proxies: List of proxy addresses to use
            gui_display_seconds: How many seconds to display GUI on success
            accounts: List of account dicts with 'id' and 'password' keys
        """
        self.start_url = start_url
        self.num_sessions = num_sessions
        self.headless = headless
        self.proxies = proxies or []
        self.gui_display_seconds = gui_display_seconds
        self.accounts = accounts or []
        self.sessions = []
        self.results = {}
        self.logger = logging.getLogger("Manager")
    
    async def run_single_session(self, session_id: int):
        """Run a single test session."""
        # Assign proxy to session (cycle through proxies if more sessions than proxies)
        proxy = None
        if self.proxies:
            proxy_index = (session_id - 1) % len(self.proxies)
            proxy = self.proxies[proxy_index]
        
        # Assign account to session (cycle through accounts if more sessions than accounts)
        account = None
        if self.accounts:
            account_index = (session_id - 1) % len(self.accounts)
            account = self.accounts[account_index]
        
        test = MultipleBrowserTest(self.start_url, session_id, self.headless, proxy, self.gui_display_seconds, account)
        await test.run_test()
        
        # Store results
        self.results[session_id] = {
            'session_id': session_id,
            'result': test.result,
            'duration': test.duration,
            'required_modules': test.required_modules,
            'module_status': test.module_status,
            'proxy': proxy
        }
    
    async def run_all_parallel(self):
        """Run all test sessions in parallel."""
        self.logger.info("="*80)
        self.logger.info(f"STARTING {self.num_sessions} PARALLEL BROWSER TESTS")
        if self.proxies:
            self.logger.info(f"Using {len(self.proxies)} authenticated proxies (Decodo)")
        else:
            self.logger.info("No proxies configured - using direct connection")
        self.logger.info("="*80)
        self.logger.info("")
        
        # Create tasks for all sessions
        tasks = [
            self.run_single_session(i + 1)
            for i in range(self.num_sessions)
        ]
        
        # Run all in parallel
        await asyncio.gather(*tasks, return_exceptions=True)
        
        # Print statistics
        # self.print_statistics()
    
    # def print_statistics(self):
    #     """Print comprehensive statistics."""
    #     self.logger.info("\n" + "="*80)
    #     self.logger.info("FINAL STATISTICS")
    #     self.logger.info("="*80)
    #
    #     # Count results
    #     result_counts = {
    #         'success': 0,
    #         'high_demand_error': 0,
    #         'bad_error': 0,
    #         'checkbox_error': 0,
    #         'exception': 0,
    #         'unknown_error': 0
    #     }
    #
    #     total_duration = 0
    #     module_usage = {'reading': 0, 'listening': 0, 'writing': 0, 'speaking': 0}
    #     module_availability = {
    #         'reading': {'available': 0, 'unavailable': 0},
    #         'listening': {'available': 0, 'unavailable': 0},
    #         'writing': {'available': 0, 'unavailable': 0},
    #         'speaking': {'available': 0, 'unavailable': 0}
    #     }
    #
    #     # Process results
    #     for session_id, data in sorted(self.results.items()):
    #         result = data['result']
    #         if result in result_counts:
    #             result_counts[result] += 1
    #
    #         total_duration += data['duration']
    #
    #         # Count module usage
    #         for module in data['required_modules']:
    #             module_usage[module] += 1
    #
    #         # Count module availability
    #         for module, status in data['module_status'].items():
    #             if status.get('exists', False):
    #                 if status.get('available', False):
    #                     module_availability[module]['available'] += 1
    #                 else:
    #                     module_availability[module]['unavailable'] += 1
    #
    #     # Print session-by-session results
    #     self.logger.info("\nSESSION-BY-SESSION RESULTS:")
    #     self.logger.info("-" * 80)
    #
    #     for session_id, data in sorted(self.results.items()):
    #         result_emoji = {
    #             'success': '✅',
    #             'high_demand_error': '❌',
    #             'bad_error': '❌',
    #             'checkbox_error': '❌',
    #             'exception': '❌',
    #             'unknown_error': '❌'
    #         }
    #
    #         emoji = result_emoji.get(data['result'], '❓')
    #         modules_str = ', '.join([m.upper() for m in data['required_modules']])
    #
    #         self.logger.info(f"Session {session_id:2d}: {emoji} {data['result']:20s} | "
    #                        f"Modules: {modules_str:40s} | Duration: {data['duration']:6.2f}s")
        
        # # Print summary statistics
        # avg_duration = total_duration / self.num_sessions if self.num_sessions > 0 else 0
        # try:
        #     self.logger.info("\n" + "-" * 80)
        #     self.logger.info("RESULT SUMMARY:")
        #     self.logger.info("-" * 80)
        #     self.logger.info(f"✅ Success:               {result_counts['success']:3d} ({result_counts['success']/self.num_sessions*100:5.1f}%)")
        #     self.logger.info(f"❌ High Demand Error:     {result_counts['high_demand_error']:3d} ({result_counts['high_demand_error']/self.num_sessions*100:5.1f}%)")
        #     self.logger.info(f"❌ Bad Error:             {result_counts['bad_error']:3d} ({result_counts['bad_error']/self.num_sessions*100:5.1f}%)")
        #     self.logger.info(f"❌ Checkbox Error:        {result_counts['checkbox_error']:3d} ({result_counts['checkbox_error']/self.num_sessions*100:5.1f}%)")
        #     self.logger.info(f"❌ Exception:             {result_counts['exception']:3d} ({result_counts['exception']/self.num_sessions*100:5.1f}%)")
        #     self.logger.info(f"❌ Unknown Error:         {result_counts['unknown_error']:3d} ({result_counts['unknown_error']/self.num_sessions*100:5.1f}%)")
        #     self.logger.info(f"\nTotal Sessions:           {self.num_sessions}")
        #     self.logger.info(f"Average Duration:         {avg_duration:.2f}s")
        #     self.logger.info(f"Total Duration:           {total_duration:.2f}s")
        #
        #     # Print module usage statistics
        #     self.logger.info("\n" + "-" * 80)
        #     self.logger.info("MODULE USAGE (How many times each module was required):")
        #     self.logger.info("-" * 80)
        #     for module in ['reading', 'listening', 'writing', 'speaking']:
        #         percentage = (module_usage[module] / self.num_sessions * 100) if self.num_sessions > 0 else 0
        #         self.logger.info(f"{module.upper():10s}: {module_usage[module]:3d} times ({percentage:5.1f}%)")
        #
        #     # Print module availability statistics
        #     self.logger.info("\n" + "-" * 80)
        #     self.logger.info("MODULE AVAILABILITY (Across all sessions):")
        #     self.logger.info("-" * 80)
        #     for module in ['reading', 'listening', 'writing', 'speaking']:
        #         available = module_availability[module]['available']
        #         unavailable = module_availability[module]['unavailable']
        #         total = available + unavailable
        #
        #         if total > 0:
        #             available_pct = (available / total * 100)
        #             self.logger.info(f"{module.upper():10s}: Available {available:3d}/{total:3d} ({available_pct:5.1f}%)")
        #         else:
        #             self.logger.info(f"{module.upper():10s}: No data")
        #
        #     self.logger.info("\n" + "="*80)
        # except Exception as e:
        #     print(e)


# ============================================================================
# PROXY AND ACCOUNT LOADING
# ============================================================================

def generate_authenticated_proxies(num_proxies: int = 1000):
    """
    Generate authenticated proxy addresses using Decodo proxy service.
    
    Args:
        num_proxies: Number of proxy addresses to generate (uses different ports)
    
    Returns:
        List of authenticated proxy URLs
    """
    username = 'spii5uqapq'
    password = 'fwThVwm=4g8is04FeZ'
    proxy_host = 'gate.decodo.com'
    
    # Generate proxies with different ports (starting from 10001)
    proxies = []
    base_port = 10001
    
    for i in range(num_proxies):
        port = base_port + i
        # Format: http://username:password@host:port
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
    start_url = 'https://www.goethe.de/ins/in/en/spr/prf/gzb2.cfm?examId=0C009CD886DDA9D3DF895F917B9D58047C83DB7FEAC7ACB00EFE02AE84C39DF48DC8EDC8DD10784A8EE7AFD305D318D5E8AD87C35FD0039AA52F821E9C84CBBA'
    headless = False  # Always starts headless, shows GUI on success
    gui_display_seconds = 200000000  # How many seconds to display GUI on success
    
    # Generate authenticated proxies and load accounts
    proxies = generate_authenticated_proxies(num_proxies=100)  # Generate 100 authenticated proxies
    accounts = load_accounts("accounts.json")
    
    print("\n" + "="*80)
    print("MULTIPLE BROWSER TEST - PARALLEL EXECUTION")
    print("="*80)
    print("Features:")
    print("  ✅ N parallel browser sessions")
    print("  ✅ Headless execution with GUI proof on success")
    print("  ✅ Session state preservation (cookies/storage)")
    print("  ✅ Random module selection per session")
    print("  ✅ Ultra-random fingerprints per session")
    print("  ✅ Comprehensive error detection")
    print("  ✅ Detailed statistics and analysis")
    print("="*80)
    print(f"Mode: Headless → GUI on Success ({gui_display_seconds}s)")
    print("="*80)
    
    try:
        n = int(input("\nEnter number of parallel browsers (N): "))
        if n <= 0:
            print("❌ Number must be greater than 0")
            return
    except ValueError:
        print("❌ Invalid input. Please enter a number.")
        return
    
    print(f"\n🚀 Starting {n} parallel browser tests...")
    print(f"📊 Each session will test: LISTENING, READING")
    print(f"🔒 Each session will use unique stealth fingerprint")
    print(f"🌐 Proxies: {len(proxies)} authenticated proxies generated")
    print(f"👤 Accounts: {len(accounts)} loaded from accounts.json")
    print(f"�️  Mode: Headless → GUI on Success ({gui_display_seconds}s)")
    print("\n" + "="*80 + "\n")
    
    # Create and run manager
    manager = MultipleTestManager(start_url, n, headless, proxies, gui_display_seconds, accounts)
    await manager.run_all_parallel()
    
    print("\n✅ All tests completed!")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user.")
    except Exception as e:
        print(f"\n\n❌ Fatal error: {str(e)}")
