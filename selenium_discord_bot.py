"""
Discord 瀏覽器自動化腳本（Selenium）

功能：使用真實瀏覽器自動發送訊息
特點：最難被偵測，因為使用真實瀏覽器行為
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
from datetime import datetime, timedelta
import sys
import json
import os
import random

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# ===== 讀取設定檔 =====
def load_config():
    """從 config.json 讀取設定"""
    config_file = "config.json"
    
    if not os.path.exists(config_file):
        print(f"❌ 找不到 {config_file}")
        print("請創建 config.json 檔案，格式如下：")
        print("""
{
  "discord_email": "你的Discord郵箱",
  "discord_password": "你的密碼",
  "channel_url": "https://discord.com/channels/...",
  "message_to_send": "/hourly",
  "send_interval_minutes": 60
}
        """)
        sys.exit(1)
    
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config
    except Exception as e:
        print(f"❌ 讀取設定檔失敗: {e}")
        sys.exit(1)

# 讀取設定
config = load_config()
DISCORD_EMAIL = config.get("discord_email")
DISCORD_PASSWORD = config.get("discord_password")
CHANNEL_URL = config.get("channel_url")
MESSAGE_TO_SEND = config.get("message_to_send")
SEND_INTERVAL_MINUTES = config.get("send_interval_minutes", 60)
# ==================

class DiscordBot:
    def __init__(self):
        # Chrome 選項
        chrome_options = Options()
        # chrome_options.add_argument("--headless")  # 無頭模式（不顯示窗口）
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-features=PasswordLeakDetection,PasswordCheck")
        chrome_options.add_argument("--password-store=basic")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
        chrome_options.add_argument("--log-level=3")
        chrome_prefs = {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.password_manager_leak_detection": False,
        }
        chrome_options.add_experimental_option("prefs", chrome_prefs)
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 15)
        
    def login(self):
        """登入 Discord"""
        print("🔐 正在登入 Discord...")
        self.driver.get("https://discord.com/login")
        
        try:
            # 等待郵箱輸入框出現
            email_input = self.wait.until(
                EC.presence_of_element_located((By.NAME, "email"))
            )
            email_input.send_keys(DISCORD_EMAIL)
            print("✅ 已輸入郵箱")
            
            # 輸入密碼
            password_input = self.driver.find_element(By.NAME, "password")
            password_input.send_keys(DISCORD_PASSWORD)
            print("✅ 已輸入密碼")
            
            # 點擊登入按鈕
            login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            login_button.click()
            print("✅ 已點擊登入按鈕")
            
            # 等待登入完成
            print("⏳ 等待登入完成...")
            time.sleep(6)
            
            # 關閉可能的彈窗
            try:
                close_buttons = self.driver.find_elements(
                    By.XPATH,
                    "//button[contains(text(), '確定')] | //button[contains(text(), 'OK')] | //button[contains(text(), '確認')]",
                )

                for btn in close_buttons:
                    if btn.is_displayed():
                        btn.click()
                        time.sleep(1)
                        break

                # 備援：若為瀏覽器層彈窗，嘗試按 ESC 關閉
                self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
                time.sleep(0.5)
            except:
                pass
            
            # 進入目標頻道並停留
            print("📍 進入目標頻道...")
            self.driver.get(CHANNEL_URL)
            time.sleep(3)
            
            # 檢查是否在頻道頁面
            if "discord.com/channels" in self.driver.current_url:
                print("✅ 已成功登入並進入頻道")
                print("📌 保持在此頻道，準備自動發送訊息")
                return True
            else:
                print("❌ 登入失敗，可能需要驗證")
                return False
                
        except Exception as e:
            print(f"❌ 登入錯誤: {e}")
            return False
    
    def send_message(self):
        """發送訊息"""
        try:
            print(f"\n📝 準備發送訊息...")
            
            # 不重新載入頁面，直接在當前頁面操作
            # 確保頁面已載入
            time.sleep(1)
            
            # 找到訊息輸入框
            message_box = self.wait.until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "div[role='textbox']")
                )
            )
            
            # 點擊訊息框確保聚焦
            message_box.click()
            time.sleep(0.5)
            
            # 輸入訊息
            message_box.send_keys(MESSAGE_TO_SEND)
            print(f"✅ 已輸入訊息: {MESSAGE_TO_SEND}")
            
            # 短暫等待
            time.sleep(1)
            
            # 按 Enter 發送（連按 3 次確保發送）
            message_box.send_keys(Keys.ENTER)
            time.sleep(0.2)
            message_box.send_keys(Keys.ENTER)
            time.sleep(0.5)
            message_box.send_keys(Keys.ENTER)
            time.sleep(1)
            message_box.send_keys(Keys.ENTER)
            print("✅ 已按 Enter 鍵（4次）")
            
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print(f"✅ [{current_time}] 訊息已發送！")
            
            # 短暫等待確認發送
            time.sleep(1)
            return True
            
        except Exception as e:
            print(f"❌ 發送失敗: {e}")
            print("嘗試重新載入頁面...")
            try:
                self.driver.get(CHANNEL_URL)
                time.sleep(3)
            except:
                pass
            import traceback
            traceback.print_exc()
            return False
    
    def auto_send_loop(self):
        """自動發送循環（每小時整點）"""
        print("=" * 50)
        print("🚀 Discord 瀏覽器自動化啟動")
        print("=" * 50)
        
        # 登入
        if not self.login():
            print("❌ 登入失敗，退出")
            self.close()
            return
        
        # 自動發送循環
        while True:
            try:
                # 計算下一個整點 + 隨機 10~30 分鐘
                now = datetime.now()
                next_hour = now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
                random_delay_min = random.randint(10, 30)
                next_time = next_hour + timedelta(minutes=random_delay_min)
                wait_seconds = (next_time - now).total_seconds()

                # # TEST（需要時取消註解）
                # now = datetime.now()
                # next_time = now + timedelta(seconds=10)
                # wait_seconds = (next_time - now).total_seconds()

                print(f"\n💤 等待 {wait_seconds:.0f} 秒")
                print(f"   隨機延遲: {random_delay_min} 分鐘")
                print(f"   下次發送: {next_time.strftime('%H:%M:%S')}")

                # # TEST 顯示（需要時取消註解）
                # print(f"\n💤 等待 {wait_seconds:.0f} 秒")
                # print(f"   下次發送: {next_time.strftime('%H:%M:%S')}")


                # 等待到整點
                time.sleep(wait_seconds)
                
                # 發送訊息
                self.send_message()
                
                # 發送後短暫等待
                time.sleep(3)
                
            except KeyboardInterrupt:
                print("\n\n🛑 已停止")
                break
            except Exception as e:
                print(f"❌ 循環錯誤: {e}")
                time.sleep(60)  # 發生錯誤時等待 1 分鐘後重試

    def close(self):
        """關閉瀏覽器"""
        self.driver.quit()
        print("✅ 瀏覽器已關閉")


if __name__ == '__main__':
    print("🌐 Discord 瀏覽器自動化")
    print("=" * 50)
    
    # 檢查設定
    if DISCORD_EMAIL == "你的Discord帳號郵箱" or not DISCORD_EMAIL:
        print("❌ 尚未設定帳號資訊")
        print("\n請編輯 config.json，設定以下項目:")
        print("  1. discord_email - 你的 Discord 登入郵箱")
        print("  2. discord_password - 你的 Discord 密碼")
        print("  3. channel_url - 頻道URL（已預設）")
        print("  4. message_to_send - 要發送的訊息")
        input("\n按 Enter 退出...")
        sys.exit()
    
    print("\n⚠️  警告:")
    print("  • 使用自動化違反 Discord 服務條款")
    print("  • 帳號可能被限制或封禁")
    print("  • 請自行承擔所有風險")
    print("\n開始啟動... (按 Ctrl+C 停止)")
    
    try:
        bot = DiscordBot()
        bot.auto_send_loop()
    except KeyboardInterrupt:
        print("\n⏹️  已中斷")
    except Exception as e:
        print(f"\n❌ 錯誤: {e}")
    finally:
        try:
            bot.close()
        except:
            pass
