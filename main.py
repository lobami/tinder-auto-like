from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import os
import time
import random
import sys

load_dotenv()

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")
BROWSER = os.getenv("BROWSER", "chrome")
DELAY = int(os.getenv("DELAY", 60))
SWIPE_DELAY_MIN = float(os.getenv("SWIPE_DELAY_MIN", 0.3))
SWIPE_DELAY_MAX = float(os.getenv("SWIPE_DELAY_MAX", 1.2))
BREAK_MIN = int(os.getenv("BREAK_MIN", 30))
BREAK_MAX = int(os.getenv("BREAK_MAX", 60))


def get_browser_context(browser_type, headless=False):
    if BROWSER == "brave":
        return browser_type.launch(channel="brave", headless=headless)
    return browser_type.launch(channel="chrome", headless=headless)


def login_via_facebook(driver):
    driver.click('[data-testid="loginBtn"]')
    time.sleep(2)

    driver.click('[data-testid="facebook"]')
    time.sleep(3)

    for handle in driver.context.handles:
        if "facebook" in handle.url:
            driver.switch_to_handle(handle)
            break

    driver.fill("#email", EMAIL)
    driver.fill("#pass", PASSWORD)
    driver.click("#loginbutton")
    time.sleep(3)

    driver.switch_to_handle(driver.context.handles[0])
    time.sleep(5)


def allow_location(driver):
    try:
        driver.click('[aria-label="Allow"]')
        time.sleep(2)
    except Exception:
        pass


def dismiss_popups(driver):
    try:
        driver.click('[data-testid="modalDismiss"]')
        time.sleep(1)
    except Exception:
        pass


def swipe_right(driver):
    driver.keyboard.press("ArrowRight")


def random_swipe_delay():
    return random.uniform(SWIPE_DELAY_MIN, SWIPE_DELAY_MAX)


def random_break_duration():
    return random.randint(BREAK_MIN, BREAK_MAX)


def format_time(seconds):
    if seconds >= 3600:
        return f"{seconds // 3600}h { (seconds % 3600) // 60}m"
    return f"{seconds // 60}m {seconds % 60}s"


def main():
    print(f"[*] Waiting {DELAY} seconds before starting...")
    time.sleep(DELAY)

    print("[*] Starting auto-like bot...")
    try:
        with sync_playwright() as p:
            browser = get_browser_context(p.chromium)
            context = browser.new_context(viewport={"width": 1280, "height": 720})
            driver = context.new_page()

            driver.goto("https://tinder.com")
            time.sleep(3)

            login_via_facebook(driver)
            allow_location(driver)
            dismiss_popups(driver)

            swipe_count = 0
            next_break = random.randint(50, 150)

            print("[*] Bot running. Press Ctrl+C to stop.")
            while True:
                try:
                    swipe_right(driver)
                    swipe_count += 1
                    delay = random_swipe_delay()
                    time.sleep(delay)

                    if swipe_count >= next_break:
                        break_duration = random_break_duration()
                        print(f"[*] Break time! Pausing {format_time(break_duration)} (swiped {swipe_count} profiles)")
                        time.sleep(break_duration)
                        swipe_count = 0
                        next_break = random.randint(50, 150)
                        print("[*] Resuming...")

                except Exception as e:
                    print(f"[*] Profile consumed or error: {e}")
                    break

            browser.close()
    except KeyboardInterrupt:
        print("\n[*] Bot stopped by user.")
        sys.exit(0)


if __name__ == "__main__":
    main()
