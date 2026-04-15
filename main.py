#!/usr/bin/env python3
"""Tinder Auto Like Bot - Auto-instalador"""
import subprocess
import sys
import os
from pathlib import Path

RUNNING_FROM_VENV = len(sys.argv) > 1 and sys.argv[1] == "RUNNING"

def check_and_install():
    venv_python = Path(".venv/bin/python3")
    if not venv_python.exists():
        print("[*] Creando virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", ".venv"], check=True)
    python = str(venv_python)
    print("[*] Instalando dependencias...")
    subprocess.run([python, "-m", "pip", "install", "playwright", "python-dotenv"], check=True)
    subprocess.run([python, "-m", "playwright", "install", "chromium"], check=True)
    print("[✓] Dependencias listas!")
    return python

def run_bot():
    from playwright.sync_api import sync_playwright
    import time
    import random
    import json
    
    PROFILE_PATH = Path(__file__).parent / "browser_profile"
    STATS_FILE = Path(__file__).parent / "stats.json"
    
    def load_stats():
        if STATS_FILE.exists():
            try:
                with open(STATS_FILE) as f:
                    return json.load(f)
            except:
                pass
        return {"total_swipes": 0, "total_matches": 0, "daily_likes": 0}
    
    def save_stats(stats):
        with open(STATS_FILE, 'w') as f:
            json.dump(stats, f, indent=2)
    
    def update_stats(key, value=1):
        stats = load_stats()
        stats[key] = stats.get(key, 0) + value
        save_stats(stats)
    
    def human_delay():
        """Delay balanceado - rápido pero humano"""
        r = random.random()
        if r < 0.5: 
            # 50% - rápido (1-4s) - típico de ver perfil rápido
            return random.uniform(1.0, 4.0)
        elif r < 0.8: 
            # 30% - normal (4-10s) - leer bio
            return random.uniform(4.0, 10.0)
        elif r < 0.95: 
            # 15% - lento (10-20s) - leer más
            return random.uniform(10.0, 20.0)
        else: 
            # 5% - pausa (20-35s) - "pensar"
            return random.uniform(20.0, 35.0)
    
    def break_duration():
        """Break entre ráfagas (10-25 min)"""
        return random.uniform(10 * 60, 25 * 60)
    
    stats = load_stats()
    print("=" * 50)
    print("  🤖 TINDER AUTO-LIKE BOT")
    print("  Anti-Ban Edition")
    print("=" * 50)
    print(f"  Total: {stats.get('total_swipes', 0)} swipes")
    print(f"  Matches: {stats.get('total_matches', 0)}")
    print("=" * 50)
    print()
    
    print("[*] Abriendo navegador...")
    print("[*] Login en Tinder manualmente (primera vez)")
    print("[*] Presiona Ctrl+C para detener")
    print()
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch_persistent_context(
                user_data_dir=str(PROFILE_PATH),
                headless=False,
                viewport={"width": 1280, "height": 720}
            )
            
            page = browser.pages[0] if browser.pages else browser.new_page()
            page.goto("https://tinder.com")
            
            print("[*] Esperando login...")
            logged_in = False
            wait = 0
            while not logged_in and wait < 300:
                try:
                    if page.locator('body').count() > 0 and 'tinder' in page.url.lower():
                        logged_in = True
                        print(f"[✓] Login detectado!")
                        break
                except:
                    pass
                wait += 1
                if wait % 15 == 0:
                    print(f"[*] Esperando... ({wait}s)")
                time.sleep(1)
            
            print("[*] 🤖 Bot activo! Swipeando humanamente...")
            swipe_count = 0
            burst_count = 0
            next_break = random.randint(25, 60)  # Break después de 25-60 likes
            likes_this_session = 0
            
            while True:
                try:
                    page.keyboard.press("ArrowRight")
                    swipe_count += 1
                    burst_count += 1
                    likes_this_session += 1
                    update_stats("total_swipes")
                    update_stats("daily_likes")
                    
                    if swipe_count % 10 == 0:
                        stats = load_stats()
                        print(f"[*] {swipe_count} swipes | {stats['daily_likes']} hoy | ráfaga: {burst_count}")
                    
                    delay = human_delay()
                    if delay >= 15:
                        print(f"[*] 🤔 Leyendo perfil... {delay:.0f}s")
                    time.sleep(delay)
                    
                    # Cerrar popups
                    try:
                        popups = page.locator('button:has-text("No Thanks"), button:has-text("Maybe Later"), [aria-label="Allow"]')
                        if popups.count() > 0:
                            popups.first.click()
                            time.sleep(0.3)
                    except:
                        pass
                    
                    # Break periódico
                    if burst_count >= next_break:
                        pause = break_duration()
                        print(f"[*] ☕ Break: {pause/60:.0f} min ({burst_count} likes | sesión: {likes_this_session})")
                        time.sleep(pause)
                        burst_count = 0
                        next_break = random.randint(25, 60)
                        page.goto("https://tinder.com")
                        time.sleep(2)
                        
                except Exception as e:
                    print(f"[*] Error: {e}")
                    time.sleep(1)
                    
    except KeyboardInterrupt:
        print(f"\n[*] Detenido - {swipe_count} swipes en sesión")
        print(f"[*] Total día: {stats.get('daily_likes', 0)}")

if __name__ == "__main__":
    if RUNNING_FROM_VENV:
        run_bot()
    else:
        python = check_and_install()
        os.execv(python, [python, sys.argv[0], "RUNNING"])
