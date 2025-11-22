"""
Goethe Booking Optimized — Fixed TargetClosedError

Key fixes:
- Use event listeners (on("disconnected"), on("close")) instead of is_closed() checks
- Proper exception filtering to suppress expected closure errors
- Better cleanup in finally block
"""

import asyncio
import logging
import json
import os
from datetime import datetime, timedelta

# Defensive imports
PLAYWRIGHT_AVAILABLE = True
try:
    from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
except Exception as e:
    PLAYWRIGHT_AVAILABLE = False
    async_playwright = None
    PlaywrightTimeoutError = Exception
    _playwright_import_error = e

try:
    from vins import stealth_config
except Exception:
    class _StubStealthConfig:
        @staticmethod
        def get_ultra_random_fingerprint():
            return {
                'viewport': {'width': 1200, 'height': 800},
                'user_agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
                'locale': 'en-US',
                'timezone_id': 'Europe/Berlin',
                'device_scale_factor': 1,
                'has_touch': False,
                'color_scheme': 'light'
            }
        @staticmethod
        def get_random_http_headers(locale, ua):
            return {'accept-language': locale, 'user-agent': ua}
        @staticmethod
        def get_stealth_script():
            return '() => {}'
    stealth_config = _StubStealthConfig()

logging.basicConfig(level=logging.INFO, format="%(asctime)s - [%(name)s] - %(levelname)s - %(message)s")
logger = logging.getLogger('goethe_optimized')

BLOCKED_RESOURCE_TYPES = {"image", "font", "stylesheet", "media"}
DEFAULT_NAV_TIMEOUT = 15000
SHORT_WAIT = 2500
AVAILABILITY_RETRY_BASE = 2
MAX_CONTEXT_CONCURRENCY = 8
GPU_ARGS = ["--use-gl=desktop", "--enable-gpu", "--ignore-gpu-blocklist", "--enable-zero-copy"]

def generate_authenticated_proxies(num_proxies: int = 100):
    username = 'spw4p88v6c'
    password = 'fDwWo7mIm04xKmh5~e'
    proxy_host = 'dc.decodo.com'
    return [f"{username}:{password}@{proxy_host}:{10001 + i}" for i in range(num_proxies)]

def load_accounts(accounts_file: str = "accounts.json"):
    try:
        if not os.path.exists(accounts_file):
            logger.warning(f"Accounts file '{accounts_file}' not found.")
            return []
        with open(accounts_file, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading accounts: {e}")
        return []

async def route_handler(route, request):
    try:
        if getattr(request, 'resource_type', None) in BLOCKED_RESOURCE_TYPES:
            await route.abort()
        else:
            await route.continue_()
    except Exception:
        try:
            await route.continue_()
        except Exception:
            pass

HELP_INSTALL_MSG = """
Playwright is not installed. Install with:
  pip install -U playwright
  playwright install chromium
"""

def is_target_closed_error(e):
    """Check if exception is a TargetClosedError"""
    err_str = str(e).lower()
    return 'target' in err_str and 'closed' in err_str

class AvailabilityChecker:
    def __init__(self, start_url, browser=None, proxy=None, logger=None):
        self.start_url = start_url
        self.browser = browser
        self.proxy = proxy
        self.logger = logger or logging.getLogger('AvailabilityChecker')

    async def check_availability(self, max_attempts=40):
        if not PLAYWRIGHT_AVAILABLE:
            self.logger.info('(dry-run) availability check')
            return False
        attempt, backoff = 0, AVAILABILITY_RETRY_BASE
        while attempt < max_attempts:
            attempt += 1
            self.logger.info(f'Availability attempt #{attempt}')
            ctx = None
            try:
                fp = stealth_config.get_ultra_random_fingerprint()
                hdrs = stealth_config.get_random_http_headers(fp['locale'], fp['user_agent'])
                ctx_opts = {
                    'viewport': fp['viewport'], 'user_agent': fp['user_agent'],
                    'locale': fp['locale'], 'timezone_id': fp['timezone_id'],
                    'ignore_https_errors': True, 'java_script_enabled': True,
                    'device_scale_factor': fp['device_scale_factor'],
                    'has_touch': fp['has_touch'], 'is_mobile': False,
                    'color_scheme': fp['color_scheme'], 'extra_http_headers': hdrs,
                }
                if self.proxy:
                    if '@' in self.proxy:
                        auth, srv = self.proxy.split('@')
                        u, p = auth.split(':')
                        ctx_opts['proxy'] = {'server': f'http://{srv}', 'username': u, 'password': p}
                    else:
                        ctx_opts['proxy'] = {'server': f'http://{self.proxy}'}
                ctx = await self.browser.new_context(**ctx_opts)
                page = await ctx.new_page()
                await page.route('**/*', route_handler)
                await page.add_init_script(stealth_config.get_stealth_script())
                await page.goto(self.start_url, wait_until='domcontentloaded', timeout=DEFAULT_NAV_TIMEOUT)
                for sel in ['button:has-text("Select modules")', 'text="Select modules"', "//button[contains(text(), 'Select modules')]"]:
                    try:
                        if await page.locator(sel).count() > 0 and await page.locator(sel).first.is_visible(timeout=SHORT_WAIT):
                            self.logger.info('Select modules visible')
                            await ctx.close()
                            return True
                    except Exception:
                        continue
                await ctx.close()
            except Exception as e:
                self.logger.debug(f'Check exception: {e}')
                if ctx:
                    try: await ctx.close()
                    except: pass
            await asyncio.sleep(min(backoff, 30))
            backoff *= 1.2
        return False

class MultipleBrowserTest:
    def __init__(self, start_url, session_id, browser=None, proxy=None, account=None, keep_alive_hours=2.0, logger=None):
        self.start_url = start_url
        self.session_id = session_id
        self.browser = browser
        self.proxy = proxy
        self.account = account
        self.keep_alive_hours = keep_alive_hours
        self.logger = logger or logging.getLogger(f'Session-{session_id}')
        self.page = self.context = self.result = None
        self.duration = 0
        self.success_timestamp = None

    async def run_test(self):
        if not PLAYWRIGHT_AVAILABLE:
            self.logger.info(f'(dry-run) session {self.session_id}')
            self.result, self.duration = 'dry_run', 0.01
            return self.result
        start_time = datetime.now()
        try:
            fp = stealth_config.get_ultra_random_fingerprint()
            hdrs = stealth_config.get_random_http_headers(fp['locale'], fp['user_agent'])
            ctx_opts = {
                'viewport': fp['viewport'], 'user_agent': fp['user_agent'],
                'locale': fp['locale'], 'timezone_id': fp['timezone_id'],
                'ignore_https_errors': True, 'java_script_enabled': True,
                'device_scale_factor': fp['device_scale_factor'],
                'has_touch': fp['has_touch'], 'is_mobile': False,
                'color_scheme': fp['color_scheme'], 'extra_http_headers': hdrs,
            }
            if self.proxy:
                if '@' in self.proxy:
                    auth, srv = self.proxy.split('@')
                    u, p = auth.split(':')
                    ctx_opts['proxy'] = {'server': f'http://{srv}', 'username': u, 'password': p}
                else:
                    ctx_opts['proxy'] = {'server': f'http://{self.proxy}'}
            self.context = await self.browser.new_context(**ctx_opts)
            await self.context.add_init_script(stealth_config.get_stealth_script())
            self.page = await self.context.new_page()
            await self.page.route('**/*', route_handler)
            await self.page.goto(self.start_url, wait_until='domcontentloaded', timeout=DEFAULT_NAV_TIMEOUT)
            if not await self._click_select_modules():
                self.result = 'button_not_found'
                self.duration = (datetime.now() - start_time).total_seconds()
                try: await self.context.close()
                except: pass
                return self.result
            if await self._check_high_demand_error():
                self.result = 'high_demand_error'
                self.duration = (datetime.now() - start_time).total_seconds()
                try: await self.context.close()
                except: pass
                return self.result
            self.result = 'success'
            self.success_timestamp = datetime.now()
            storage = await self.context.storage_state()
            try: await self.context.close()
            except: pass
            asyncio.create_task(self._safe_keepalive(storage))
            self.duration = (datetime.now() - start_time).total_seconds()
            return self.result
        except Exception as e:
            self.logger.error(f'Exception: {e}')
            self.result = 'exception'
            self.duration = (datetime.now() - start_time).total_seconds()
            if self.context:
                try: await self.context.close()
                except: pass
            return self.result

    async def _click_select_modules(self):
        for sel in ['button:has-text("Select modules")', 'text="Select modules"', "//button[contains(text(), 'Select modules')]"]:
            try:
                await self.page.wait_for_selector(sel, state='visible', timeout=SHORT_WAIT)
                await self.page.click(sel, timeout=5000)
                self.logger.info('Clicked Select modules')
                return True
            except Exception:
                continue
        self.logger.warning('Select modules not clickable')
        return False

    async def _check_high_demand_error(self):
        try:
            return await self.page.locator("text=/very high demand|cannot be booked at the moment/i").count() > 0
        except Exception:
            return False

    async def _safe_keepalive(self, storage):
        """Wrapper to suppress TargetClosedError from keep-alive task"""
        try:
            await self._open_gui_and_keep_alive(storage)
        except Exception as e:
            if not is_target_closed_error(e):
                self.logger.error(f"Keep-alive error: {e}")

    async def _open_gui_and_keep_alive(self, storage_state):
        sem = MultipleTestManager.gui_semaphore
        browser_gui = None
        gui_closed = False

        async with sem:
            try:
                p = MultipleTestManager.playwright_instance
                if not p:
                    return

                fp = stealth_config.get_ultra_random_fingerprint()
                hdrs = stealth_config.get_random_http_headers(fp['locale'], fp['user_agent'])

                browser_gui = await p.chromium.launch(headless=False, args=["--disable-blink-features=AutomationControlled", *GPU_ARGS])

                def on_disconnected():
                    nonlocal gui_closed
                    gui_closed = True
                browser_gui.on("disconnected", on_disconnected)

                context_gui = await browser_gui.new_context(
                    viewport=fp['viewport'], user_agent=fp['user_agent'],
                    locale=fp['locale'], timezone_id=fp['timezone_id'],
                    storage_state=storage_state, extra_http_headers=hdrs,
                    ignore_https_errors=True,
                )
                page_gui = await context_gui.new_page()

                def on_page_close():
                    nonlocal gui_closed
                    gui_closed = True
                page_gui.on("close", on_page_close)

                await page_gui.add_init_script(stealth_config.get_stealth_script())

                try:
                    await page_gui.goto(self.start_url, wait_until='domcontentloaded', timeout=DEFAULT_NAV_TIMEOUT)
                except Exception as e:
                    self.logger.debug(f'GUI nav failed: {e}')
                    if browser_gui:
                        try: await browser_gui.close()
                        except: pass
                    return

                self.logger.info(f'GUI opened for session {self.session_id}')
                end_time = datetime.now() + timedelta(hours=self.keep_alive_hours)

                while datetime.now() < end_time and not gui_closed:
                    try:
                        await asyncio.sleep(300)
                        if gui_closed:
                            break
                        await page_gui.evaluate("() => { window.scrollBy(0, 10); window.scrollBy(0, -10); }")
                    except Exception as e:
                        if is_target_closed_error(e):
                            gui_closed = True
                            break
                        await asyncio.sleep(5)

                self.logger.info(f'GUI keep-alive ended for session {self.session_id}')

            except Exception as e:
                if not is_target_closed_error(e):
                    self.logger.error(f'GUI error: {e}')
            finally:
                if browser_gui and not gui_closed:
                    try: await browser_gui.close()
                    except: pass

class MultipleTestManager:
    gui_semaphore = asyncio.Semaphore(MAX_CONTEXT_CONCURRENCY)
    playwright_instance = None

    def __init__(self, start_url, num_sessions, proxies=None, accounts=None, keep_alive_hours=2.0):
        self.start_url = start_url
        self.num_sessions = num_sessions
        self.proxies = proxies or []
        self.accounts = accounts or []
        self.keep_alive_hours = keep_alive_hours
        self.results = {}
        self.logger = logging.getLogger('Manager')
        self.browser = None

    async def run_with_availability_check(self):
        if not PLAYWRIGHT_AVAILABLE:
            self.logger.info('(dry-run) — playwright missing')
            sem = asyncio.Semaphore(min(self.num_sessions, MAX_CONTEXT_CONCURRENCY))
            tasks = [asyncio.create_task(self._run_with_semaphore(i + 1, sem)) for i in range(min(self.num_sessions, 4))]
            await asyncio.gather(*tasks)
            self._print_summary()
            logger.info(HELP_INSTALL_MSG)
            return
        async with async_playwright() as p:
            MultipleTestManager.playwright_instance = p
            self.browser = await p.chromium.launch(headless=True, args=['--disable-dev-shm-usage', '--no-sandbox', '--disable-web-security', '--disable-blink-features=AutomationControlled'])
            proxy = self.proxies[0] if self.proxies else None
            checker = AvailabilityChecker(self.start_url, self.browser, proxy)
            if not await checker.check_availability():
                self.logger.error('Availability not detected. Exiting.')
                try: await self.browser.close()
                except: pass
                return
            sem = asyncio.Semaphore(MAX_CONTEXT_CONCURRENCY)
            tasks = [asyncio.create_task(self._run_with_semaphore(i + 1, sem)) for i in range(self.num_sessions)]
            await asyncio.gather(*tasks)
            try: await self.browser.close()
            except: pass
            self._print_summary()

    async def _run_with_semaphore(self, session_id, sem):
        async with sem:
            proxy = self.proxies[(session_id - 1) % len(self.proxies)] if self.proxies else None
            account = self.accounts[(session_id - 1) % len(self.accounts)] if self.accounts else None
            test = MultipleBrowserTest(self.start_url, session_id, self.browser, proxy, account, self.keep_alive_hours)
            result = await test.run_test()
            self.results[session_id] = {'session_id': session_id, 'result': result, 'duration': test.duration, 'proxy': proxy, 'success_timestamp': test.success_timestamp}

    def _print_summary(self):
        self.logger.info('=== SUMMARY ===')
        counts, total = {}, 0
        for sid, d in sorted(self.results.items()):
            counts[d['result']] = counts.get(d['result'], 0) + 1
            total += d.get('duration', 0)
            self.logger.info(f"Session {sid}: {d['result']} (dur={d['duration']:.2f}s)")
        self.logger.info(f"Totals: {counts}")
        if self.num_sessions:
            self.logger.info(f"Avg duration: {total / self.num_sessions:.2f}s")

async def main():
    start_url = os.environ.get('START_URL') or 'https://www.goethe.de/ins/in/en/spr/prf/gzb2.cfm?examId=5F0ECCDAD6DAF286DCD85E927E980A007AD2D729EB97AEB101AC05F9D79098F88FCDEA998D10794BDAECAFD703DE4980EBADDBC3538C549CA62C8617CC83CFE6'
    num_sessions = int(os.environ.get('NUM_SESSIONS', '4'))
    keep_alive_hours = float(os.environ.get('KEEP_ALIVE_HOURS', '10000'))
    proxies = generate_authenticated_proxies(100)
    accounts = load_accounts('accounts.json')
    manager = MultipleTestManager(start_url, num_sessions, proxies, accounts, keep_alive_hours)
    await manager.run_with_availability_check()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Interrupted by user')
    except Exception as e:
        if not PLAYWRIGHT_AVAILABLE:
            logger.error(f'Playwright import error: {_playwright_import_error}')
            logger.info(HELP_INSTALL_MSG)
        else:
            logger.exception(e)