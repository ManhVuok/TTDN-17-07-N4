import requests
import sys

def test_telegram(token, chat_id):
    print(f"--- Đang kiểm tra Telegram Bot ---")
    print(f"Token: {token[:10]}...")
    print(f"Chat ID: {chat_id}")
    
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': "<b>[TEST]</b> Thông báo thử nghiệm từ script kiểm tra Odoo.",
        'parse_mode': 'HTML'
    }
    
    try:
        response = requests.post(url, json=payload, timeout=15)
        if response.status_code == 200:
            print("✅ Thành công! Bot đã gửi tin nhắn thành công.")
        else:
            print(f"❌ Thất bại! Lỗi từ Telegram: {response.status_code}")
            print(f"Chi tiết: {response.text}")
    except Exception as e:
        print(f"❌ Thất bại! Lỗi kết nối: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Sử dụng: python3 test_tele.py <TOKEN> <CHAT_ID>")
    else:
        test_telegram(sys.argv[1], sys.argv[2])
