# Discord Selenium 自動發訊腳本

這個資料夾包含一個使用 Selenium 操作瀏覽器的 Discord 自動化腳本。程式會登入 Discord、進入指定頻道，並依排程自動送出訊息。

## 檔案說明

- [selenium_discord_bot.py](selenium_discord_bot.py) - 主程式，負責登入、進入頻道與發送訊息
- [config.json](config.json) - 設定檔，存放 Discord 帳號、密碼、頻道網址與要送出的訊息

## 功能

- 使用真實 Chrome 瀏覽器登入 Discord
- 自動進入指定頻道
- 自動輸入並送出指定訊息
- 每輪會等待到下一個整點後，再額外加入 10 到 30 分鐘的隨機延遲

## 環境需求

- Python 3.10 以上
- Google Chrome
- Selenium 套件

如果你第一次執行時遇到 ChromeDriver 相關問題，通常是 Chrome 版本或瀏覽器驅動相容性問題。先確認本機已安裝可正常開啟的 Chrome。

## 安裝套件

建議先建立虛擬環境，再安裝 Selenium：

```bash
python -m venv .venv
.venv\Scripts\activate
pip install selenium
```

## 設定 `config.json`

請將 [config.json](config.json) 補成以下格式：

```json
{
  "discord_email": "你的Discord郵箱",
  "discord_password": "你的密碼",
  "channel_url": "https://discord.com/channels/...",
  "message_to_send": "/hourly",
  "send_interval_minutes": 60
}
```

欄位說明：

- `discord_email` - Discord 登入信箱
- `discord_password` - Discord 密碼
- `channel_url` - 目標頻道網址
- `message_to_send` - 要發送的訊息內容
- `send_interval_minutes` - 目前設定檔有保留這個欄位，但主程式排程是依整點與隨機延遲執行，尚未直接使用這個值

## 執行方式

在這個資料夾下執行：

```bash
python selenium_discord_bot.py
```

程式啟動後會：

1. 開啟 Chrome
2. 前往 Discord 登入頁
3. 使用 `config.json` 的帳密登入
4. 進入 `channel_url`
5. 進入自動發送循環

## 注意事項

- 第一次登入時，Discord 可能跳出驗證、通知或安全提示，需要手動處理
- 若頁面結構改版，Selenium 的選擇器可能需要調整
- 程式目前會持續執行，停止時可在終端機按 `Ctrl + C`
- 請確認你的使用方式符合 Discord 的服務條款與伺服器規範

## 常見問題

### 找不到 `config.json`

程式啟動時會檢查設定檔是否存在。如果沒有，請先建立 [config.json](config.json) 並填入必要資訊。

### 登入後無法進入頻道

- 確認 `channel_url` 是否正確
- 確認帳號有權限進入該頻道
- 若 Discord 要求額外驗證，請先完成驗證再重新執行

### 訊息沒有送出

- 檢查目標頻道的輸入框是否仍維持可操作狀態
- 確認 Discord 頁面沒有彈窗遮住輸入區
- 若元素選擇器失效，可能需要更新腳本中的定位方式