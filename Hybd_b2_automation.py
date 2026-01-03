# -*- coding: utf-8 -*-
import time
from time import sleep

import pandas as pd
from multiprocessing import Process
from playwright.sync_api import sync_playwright

full_module = False
index_number = 2

# Map module names to their XPaths
module_xpaths = {
    "Lesen": "//section[@id='examSection']/div/div[3]/div[4]/form/div/div[3]/div[4]/div[1]/div/label[1]/span[1]",
    "Horen": "//section[@id='examSection']/div/div[3]/div[4]/form/div/div[3]/div[4]/div[1]/div/label[2]/span[1]",
    "Schreiben": "//section[@id='examSection']/div/div[3]/div[4]/form/div/div[3]/div[4]/div[1]/div/label[3]/span[1]",
    "Sprechen": "//section[@id='examSection']/div/div[3]/div[4]/form/div/div[3]/div[4]/div[1]/div/label[4]/span[1]",
}


def login(page, username, password):
    # Base URL
    page.goto("https://hyderabad.german.in/")

    # Accept cookies
    try:
        page.click("//div[7]/div/div/div/button/i")
    except:
        print("No cookie banner found, skipping...")

    # Click Login link
    page.click("text=Login")

    # Fill email & password
    page.fill("#txtLoginEmail", username)
    time.sleep(1.2)
    page.fill("#txtLoginPassword", str(password))
    time.sleep(1.2)

    # Click Login
    page.click("#loginBtn")

    # Accept cookies again (if shown after login)
    try:
        page.click("//div[7]/div/div/div/button/i")
    except:
        print("2 - No cookie banner found, skipping...")


def process_upi_payment(page, upi_id):
    """Handle the UPI payment process in BillDesk iframe"""

    # Wait for BillDesk iframe
    print("Waiting for BillDesk iframe...")
    iframe_el = page.wait_for_selector("iframe", timeout=30000)
    frame = iframe_el.content_frame()

    if not frame:
        time.sleep(2)
        frame = iframe_el.content_frame()

    if not frame:
        raise Exception("Could not access BillDesk iframe")

    print("✓ BillDesk iframe loaded")
    time.sleep(3)

    # Look for nested SDK iframe
    print("Looking for payment UI...")
    sdk_iframe = None
    try:
        sdk_iframe_element = frame.wait_for_selector("iframe#sdk-iframe", timeout=10000)
        if sdk_iframe_element:
            sdk_iframe = sdk_iframe_element.content_frame()
            if sdk_iframe:
                frame = sdk_iframe
                print("✓ Found nested payment iframe")
                time.sleep(2)
    except:
        print("⚠ Using main iframe")

    # Wait for payment options to load
    print("Waiting for payment options...")
    for i in range(15):
        try:
            nav_elements = frame.locator("div[role='navigation']")
            if nav_elements.count() >= 3:
                print(f"✓ Payment options loaded ({nav_elements.count()} options)")
                break
        except:
            pass
        time.sleep(1)

    # Click BHIM UPI option (3rd option, index 2)
    print("\nClicking BHIM UPI option...")
    try:
        upi_option = frame.locator("div[role='navigation']").nth(2)
        upi_option.click()
        print("✓ Clicked BHIM UPI option")
        time.sleep(3)
    except Exception as e:
        print(f"❌ Failed to click UPI option: {e}")
        return False

    # Enter UPI ID
    print(f"\nEntering UPI ID: {upi_id}")
    try:
        upi_input = frame.locator("input#upiId")
        upi_input.clear()
        upi_input.fill(upi_id)

        # Verify
        entered_value = upi_input.input_value()
        if entered_value == upi_id:
            print(f"✓ UPI ID entered: {upi_id}")
        else:
            print(f"⚠ Warning: Entered '{entered_value}' instead of '{upi_id}'")
    except Exception as e:
        print(f"❌ Failed to enter UPI ID: {e}")
        return False

    # Click Pay button - wait a bit for validation
    print("\nClicking Pay button...")
    time.sleep(2)

    try:
        pay_button = None

        selectors_priority = [
            "button[data-testid='collect-pay-button']",
            "button[data-payment-category='upi'][type='submit']",
            "button[data-upi-type='collect']",
        ]

        for selector in selectors_priority:
            try:
                btn = frame.locator(selector).first
                if btn.count() > 0:
                    pay_button = btn
                    print(f"  ✓ Found Pay button using: {selector}")
                    break
            except:
                continue

        # Strategy 2: Find by text pattern
        if not pay_button:
            print("  Searching buttons by text pattern...")
            all_buttons = frame.locator("button[type='submit']").all()

            for btn in all_buttons:
                try:
                    btn_text = btn.inner_text()
                    print(f"    Found button: '{btn_text}'")

                    if ("Pay" in btn_text and (
                            "₹" in btn_text or "Rs" in btn_text or any(char.isdigit() for char in btn_text))):
                        if "QR" not in btn_text and "Show" not in btn_text:
                            pay_button = btn
                            print(f"    ✓ Matched Pay button: '{btn_text}'")
                            break
                except:
                    continue

        # Strategy 3: Fallback method
        if not pay_button:
            print("  Trying fallback method...")
            try:
                all_pay_buttons = frame.locator("button[name='pay-button']").all()
                for btn in all_pay_buttons:
                    text = btn.inner_text()
                    if "QR" not in text and "Show" not in text and "Scan" not in text:
                        pay_button = btn
                        print(f"    ✓ Fallback found: '{text}'")
                        break
            except:
                pass

        # Click the button if found
        if pay_button:
            if pay_button.is_disabled():
                print("  Button is disabled, waiting...")
                try:
                    pay_button.wait_for(state="enabled", timeout=5000)
                    print("  ✓ Button enabled")
                except:
                    print("  ⚠ Button still disabled, clicking anyway...")

            btn_text = pay_button.inner_text()
            print(f"\n  Clicking button: '{btn_text}'")
            pay_button.click()
            print(f"✓ Successfully clicked Pay button!")
            time.sleep(3)
            return True
        else:
            print("❌ Could not find Pay button")

            # Debug: List all buttons
            print("\n  Debug - All buttons found:")
            try:
                all_btns = frame.locator("button").all()
                for i, btn in enumerate(all_btns[:10]):
                    try:
                        text = btn.inner_text()
                        btn_type = btn.get_attribute("type")
                        btn_name = btn.get_attribute("name")
                        print(f"    [{i}] '{text}' type={btn_type} name={btn_name}")
                    except:
                        pass
            except:
                pass

            return False

    except Exception as e:
        print(f"❌ Failed to click Pay button: {e}")
        import traceback
        traceback.print_exc()
        return False


def get_span_text(page, username):
    """
    Retrieve and validate span text with multiple fallback methods.
    Returns the span text if valid, None otherwise.
    """
    try:
        span_xpath = "xpath=//section[@id='examSection']/div/div[3]/div[4]/form/div/div[1]/div[8]/p/span"
        span_locator = page.locator(span_xpath)

        # Wait for element to be visible
        print(f"[{username}] Waiting for span element...")
        span_locator.wait_for(state="visible", timeout=10000)

        # Additional wait for content to populate
        time.sleep(1)

        # Try multiple methods to get the text
        span_text = None

        # Method 1: text_content()
        try:
            span_text = span_locator.text_content()
            if span_text:
                print(f"[{username}] Method 1 (text_content): '{span_text}'")
        except:
            pass

        # Method 2: inner_text()
        if not span_text or not span_text.strip():
            try:
                span_text = span_locator.inner_text()
                if span_text:
                    print(f"[{username}] Method 2 (inner_text): '{span_text}'")
            except:
                pass

        # Method 3: evaluate
        if not span_text or not span_text.strip():
            try:
                span_text = span_locator.evaluate("el => el.textContent")
                if span_text:
                    print(f"[{username}] Method 3 (evaluate): '{span_text}'")
            except:
                pass

        # Clean and validate
        if span_text:
            span_text = span_text.strip()
            print(f"[{username}] Final span_text: '{span_text}'")

            # Check if valid (not empty, not "0", not "1")
            if span_text and span_text not in ["0", "1", ""]:
                print(f"[{username}] ✓ Span text is VALID: '{span_text}'")
                return span_text
            else:
                print(f"[{username}] ✗ Span text is INVALID: '{span_text}'")
                return None
        else:
            print(f"[{username}] ✗ Span text is empty or None")
            return None

    except Exception as e:
        print(f"[{username}] ❌ Error getting span text: {e}")

        # Debug information
        try:
            element_count = page.locator(
                "xpath=//section[@id='examSection']/div/div[3]/div[4]/form/div/div[1]/div[8]/p/span"
            ).count()
            print(f"[{username}] Debug: Found {element_count} matching span elements")

            # Try to get parent paragraph text
            parent_text = page.locator(
                "xpath=//section[@id='examSection']/div/div[3]/div[4]/form/div/div[1]/div[8]/p"
            ).text_content()
            print(f"[{username}] Debug: Parent <p> text: '{parent_text}'")
        except:
            pass

        return None


def refresh_page(page, username):
    """Refresh the exam section"""
    print(f"[{username}] 🔄 Refreshing page...")
    try:
        page.click("xpath=//section[@id='examSection']/div/div[2]/div/div")
        page.click("xpath=//section[@id='examSection']/div/div[2]/div/div[2]/div")
        print(f"[{username}] ✓ Page refreshed")
    except Exception as e:
        print(f"[{username}] ⚠ Error during refresh: {e}")


def run_instance(username, password, module, upi):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(storage_state=None)
        page = context.new_page()

        # Do login
        login(page, username, password)

        try:
            while True:
                # Check if the option at index_number is enabled
                try:
                    select_element = page.locator(
                        "xpath=//*[@id='examSection']/div/div[3]/div[4]/form/div/div[1]/div[1]/div/select"
                    )
                    options = select_element.locator("option").all()

                    if len(options) > index_number:
                        option = options[index_number]
                        is_disabled = option.get_attribute("disabled")

                        if is_disabled is None:  # Option is enabled
                            print(f"[{username}] ✓ Option at index {index_number} is enabled")

                            # Keep retrying until option is selected
                            option_selected = False
                            retry_count = 0
                            max_retries = 5

                            while not option_selected and retry_count < max_retries:
                                try:
                                    print(f"[{username}] Attempting to select option (attempt {retry_count + 1})...")
                                    page.select_option(
                                        "xpath=//*[@id='examSection']/div/div[3]/div[4]/form/div/div[1]/div[1]/div/select",
                                        index=index_number,
                                    )
                                    option_selected = True
                                    print(f"[{username}] ✓ Option selected successfully!")

                                except Exception as e:
                                    retry_count += 1
                                    print(f"[{username}] ⚠ Selection failed (attempt {retry_count}): {e}")

                            if not option_selected:
                                print(f"[{username}] ✗ Failed to select option after {max_retries} attempts")
                                refresh_page(page, username)
                                continue

                            # Now check span text - CRITICAL VALIDATION
                            span_text = get_span_text(page, username)

                            if span_text:  # Only proceed if span text is valid
                                print(f"[{username}] ✅ SPAN TEXT IS VALID - Proceeding with booking...")

                                # Click the proceed button
                                page.click(
                                    "xpath=//section[@id='examSection']/div/div[3]/div[4]/form/div/div[2]/div[1]/button/span"
                                )
                                time.sleep(.5)

                                # Handle module selection
                                if module.lower().strip() == "full module":
                                    print(f"[{username}] Selecting FULL MODULE")
                                    # Click Payment Button for full module
                                    page.click(
                                        "xpath=//section[@id='examSection']/div/div[3]/div[4]/form/div/div[3]/div[4]/div[2]/button/span"
                                    )
                                else:
                                    print(f"[{username}] Selecting MODULAR: {module}")
                                    # Click modular option
                                    page.click(
                                        "//*[@id='examSection']/div/div[3]/div[4]/form/div/div[3]/div[3]/label[2]/span[1]"
                                    )

                                    # Select individual modules
                                    for mod in [m.strip() for m in module.split(",")]:
                                        xpath = module_xpaths.get(mod)
                                        if xpath:
                                            page.click(xpath)
                                            print(f"[{username}] ✅ Selected module: {mod}")
                                        else:
                                            print(f"[{username}] ⚠️ Unknown module: {mod}")

                                    time.sleep(1)
                                    # Click payment button for modular
                                    page.click(
                                        "xpath=//section[@id='examSection']/div/div[3]/div[4]/form/div/div[3]/div[4]/div[2]/button/span"
                                    )

                                time.sleep(3)

                                # Process UPI payment
                                print(f"[{username}] 💳 Processing payment...")
                                success = process_upi_payment(page, upi)

                                if success:
                                    print(f"\n[{username}] ✅ Payment process completed successfully!")
                                    print(f"[{username}] Waiting for payment confirmation...")
                                    time.sleep(1000)  # Keep session alive
                                else:
                                    print(f"\n[{username}] ⚠ Payment process incomplete - check manually")
                                    time.sleep(30)

                                break  # Exit the loop after successful attempt

                            else:
                                # Span text is invalid - refresh and try again
                                print(f"[{username}] ✗ SPAN TEXT IS INVALID - Refreshing...")
                                refresh_page(page, username)

                        else:
                            # Option is disabled
                            print(f"[{username}] ✗ Option at index {index_number} is disabled")
                            refresh_page(page, username)
                    else:
                        # Option index not found
                        print(f"[{username}] ✗ Option index {index_number} not found (only {len(options)} options)")
                        refresh_page(page, username)

                except Exception as e:
                    print(f"[{username}] ❌ Error in main loop: {e}")
                    import traceback
                    traceback.print_exc()
                    refresh_page(page, username)

        except KeyboardInterrupt:
            print(f"\n[{username}] 🛑 Stopped by user")
        except Exception as e:
            print(f"[{username}] ❌ FATAL EXCEPTION: {e}")
            import traceback
            traceback.print_exc()
        finally:
            browser.close()


def main():
    # Read Excel file
    df = pd.read_excel("accounts.xlsx")  # Must have columns: username, password, modules, upid

    processes = []
    for _, row in df.iterrows():
        p = Process(
            target=run_instance,
            args=(row["username"], row["password"], row["modules"], row["upid"])
        )
        p.start()
        processes.append(p)
        time.sleep(.5)  # Stagger the starts

    # Wait for all processes
    for p in processes:
        p.join()


if __name__ == "__main__":
    main()