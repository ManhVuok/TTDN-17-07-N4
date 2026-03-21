import requests
import sys
import json

def list_models(api_key):
    print("--- LIỆT KÊ CÁC MODEL AI CÓ SẴN ---")
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    
    try:
        response = requests.get(url, timeout=30)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            models = response.json().get('models', [])
            print(f"Tìm thấy {len(models)} models:")
            for m in models:
                print(f"- {m['name']} ({m['displayName']})")
            print("\nLời khuyên: Bạn hãy chọn một tên model bắt đầu bằng 'models/' ở trên (bỏ chữ models/ đi) để điền vào Odoo nhé.")
        else:
            print("❌ THẤT BẠI!")
            print(f"Lỗi: {response.text}")
    except Exception as e:
        print(f"❌ LỖI KẾT NỐI: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Sử dụng: python3 list_models.py <API_KEY>")
    else:
        list_models(sys.argv[1])
