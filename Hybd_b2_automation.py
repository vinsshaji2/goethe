# -*- coding: utf-8 -*-
import time
from time import sleep

import pandas as pd
from multiprocessing import Process
from playwright.sync_api import sync_playwright

full_module = False
index_number = 0

# Map module names to their XPaths
module_xpaths = {
    "Lesen": "//section[@id='examSection]/div/div[3]/div[4]/form/div/div[3]/div[4]/div[1]/div/label[1]/span[1]",
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
    # page.click("#loginBtn")
    # time.sleep(1)

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
        # Strategy 1: Find button with specific attributes (most reliable)
        # This button has data-testid="collect-pay-button" and data-payment-category="upi"
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

        # Strategy 2: Find by text pattern - any button with "Pay" followed by currency/amount
        if not pay_button:
            print("  Searching buttons by text pattern...")
            all_buttons = frame.locator("button[type='submit']").all()

            for btn in all_buttons:
                try:
                    btn_text = btn.inner_text()
                    print(f"    Found button: '{btn_text}'")

                    # Match "Pay ₹XXXX" or "Pay Rs XXXX" or just "Pay" with numbers
                    if ("Pay" in btn_text and (
                            "₹" in btn_text or "Rs" in btn_text or any(char.isdigit() for char in btn_text))):
                        # Exclude QR-related buttons
                        if "QR" not in btn_text and "Show" not in btn_text:
                            pay_button = btn
                            print(f"    ✓ Matched Pay button: '{btn_text}'")
                            break
                except:
                    continue

        # Strategy 3: Get all pay-button name buttons and pick the right one
        if not pay_button:
            print("  Trying fallback method...")
            try:
                all_pay_buttons = frame.locator("button[name='pay-button']").all()
                for btn in all_pay_buttons:
                    text = btn.inner_text()
                    # Exclude QR buttons
                    if "QR" not in text and "Show" not in text and "Scan" not in text:
                        pay_button = btn
                        print(f"    ✓ Fallback found: '{text}'")
                        break
            except:
                pass

        # Click the button if found
        if pay_button:
            # Check if disabled
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
                for i, btn in enumerate(all_btns[:10]):  # First 10 buttons
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


def run_instance(username, password, module, upi):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # headless=True for silent mode
        context = browser.new_context(storage_state=None)  # fresh session
        page = context.new_page()

        # Do login
        login(page, username, password)
        try:
            while True:

                # ################full module###################
                # span_text = page.text_content(
                #     "xpath=//section[@id='examSection']/div/div[3]/div[4]/form/div/div[1]/div[8]/p/span"
                # )
                ######modular wise#################

                # Check if the option at index_number is enabled
                try:
                    select_element = page.locator(
                        "xpath=//*[@id='examSection']/div/div[3]/div[4]/form/div/div[1]/div[1]/div/select")
                    options = select_element.locator("option").all()

                    if len(options) > index_number:
                        option = options[index_number]
                        is_disabled = option.get_attribute("disabled")

                        if is_disabled is None:  # Option is enabled
                            # Keep retrying until option is found
                            option_selected = False
                            retry_count = 0
                            while not option_selected:
                                try:
                                    print(f"[{username}] Attempting to select option (attempt {retry_count + 1})...")
                                    page.select_option(
                                        "xpath=//*[@id='examSection']/div/div[3]/div[4]/form/div/div[1]/div[1]/div/select",
                                        index=index_number,
                                    )
                                    option_selected = True
                                    print(f"[{username}] ✓ Option selected successfully!")
                                    span_text = page.text_content(
                                        "xpath=//section[@id='examSection']/div/div[3]/div[4]/form/div/div[1]/div[8]/p/span"
                                    )
                                    print(f"[{username}] span_text:", span_text)
                                    if span_text and span_text.strip() not in ["0", "1"]:
                                        print(f"[{username}] Span has content:", span_text)
                                        page.click(
                                            "xpath=//section[@id='examSection']/div/div[3]/div[4]/form/div/div[2]/div[1]/button/span")
                                        if module.lower().strip() == "full module":
                                            # Click Payment Button
                                            page.click(
                                                "xpath=//section[@id='examSection']/div/div[3]/div[4]/form/div/div[3]/div[4]/div[2]/button/span"
                                            )
                                        else:
                                            page.click(
                                                "//*[@id='examSection']/div/div[3]/div[4]/form/div/div[3]/div[3]/label[2]/span[1]")
                                            # Split your variable (comma-separated values)
                                            for mod in [m.strip() for m in module.split(",")]:
                                                xpath = module_xpaths.get(mod)
                                                if xpath:
                                                    page.click(xpath)
                                                    print(f"[{username}] ✅ Selected module: {mod}")
                                                else:
                                                    print(f"[{username}] ⚠️ Unknown module: {mod}")
                                            page.click(
                                                "xpath=//section[@id='examSection']/div/div[3]/div[4]/form/div/div[3]/div[4]/div[2]/button/span"
                                            )
                                        success = process_upi_payment(page, upi)

                                        if success:
                                            print("\n✅ Payment process completed successfully!")
                                            print("Waiting 60 seconds to complete payment...")
                                        else:
                                            print("\n⚠ Payment process incomplete - check manually")
                                            print("Waiting 30 seconds for manual intervention...")

                                        time.sleep(1000)  # keep session alive
                                        break
                                    else:
                                        print(f"[{username}] Span is empty, refreshing...")
                                        page.click("xpath=//section[@id='examSection']/div/div[2]/div/div")
                                        page.click("xpath=//section[@id='examSection']/div/div[2]/div/div[2]/div")
                                except Exception as e:
                                    retry_count += 1
                                    print(
                                        f"[{username}] ⚠ Option not found yet (attempt {retry_count}), retrying in 2 seconds...")
                        else:
                            print(f"[{username}] Option is disabled, refreshing...")
                            page.click("xpath=//section[@id='examSection']/div/div[2]/div/div")
                            page.click("xpath=//section[@id='examSection']/div/div[2]/div/div[2]/div")
                    else:
                        print(f"[{username}] Option index not found, refreshing...")
                        page.click("xpath=//section[@id='examSection']/div/div[2]/div/div")
                        page.click("xpath=//section[@id='examSection']/div/div[2]/div/div[2]/div")

                except Exception as e:
                    print(f"[{username}] Error checking option: {e}, refreshing...")
                    page.click("xpath=//section[@id='examSection']/div/div[2]/div/div")
                    page.click("xpath=//section[@id='examSection']/div/div[2]/div/div[2]/div")

        except Exception as e:
            print("EXCEPTION OCCURED:", e)


def main():
    # Read Excel file
    df = pd.read_excel("accounts.xlsx")  # Must have columns: username, password, modules

    processes = []
    for _, row in df.iterrows():
        p = Process(target=run_instance, args=(row["username"], row["password"], row["modules"], row["upid"]))
        p.start()
        processes.append(p)

    # Wait for all processes
    for p in processes:
        p.join()


if __name__ == "__main__":
    main()