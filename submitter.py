import os
import time
import pyperclip
from playwright.sync_api import sync_playwright

DIR = "LeetCode-Solutions/C++"
DELAY = 15

def clean(code):
    return code.split("int main()")[0].strip() if "int main()" in code else code.strip()

def run():
    with sync_playwright() as p:
        try:
            b = p.chromium.connect_over_cdp("http://localhost:9222")
        except:
            return

        page = b.contexts[0].pages[0] if b.contexts[0].pages else b.contexts[0].new_page()
        files = [f for f in os.listdir(DIR) if f.endswith('.cpp')]

        for f in files:
            slug = f[:-4]
            try:
                with open(os.path.join(DIR, f), 'r', encoding='utf-8') as fp:
                    code = clean(fp.read())
                
                page.goto(f"https://leetcode.com/problems/{slug}/", wait_until="domcontentloaded")
                
                try:
                    page.wait_for_selector('.monaco-editor', timeout=10000)
                except:
                    print(f"[{slug}] SKIP")
                    continue

                pyperclip.copy(code)
                
                page.locator('.monaco-editor:visible').first.click(force=True, timeout=3000)
                time.sleep(0.3)
                page.keyboard.press("Meta+A")
                time.sleep(0.1)
                page.keyboard.press("Backspace")
                time.sleep(0.3)
                
                page.keyboard.down("Meta")
                page.keyboard.press("v")
                page.keyboard.up("Meta")
                time.sleep(0.8)
                
                try:
                    page.locator('[data-e2e-locator="console-submit-button"]').click(force=True, timeout=3000)
                except:
                    page.get_by_role("button", name="Submit").click(force=True, timeout=3000)
                
                page.wait_for_selector('[data-e2e-locator="submission-result"]', timeout=15000)
                res = page.locator('[data-e2e-locator="submission-result"]').inner_text().strip()
                
                if "Accepted" in res:
                    print(f"[{slug}] AC")
                    time.sleep(DELAY)
                else:
                    print(f"[{slug}] {res}")
                    time.sleep(2) 
                    
            except:
                print(f"[{slug}] ERR")

if __name__ == "__main__":
    run()
