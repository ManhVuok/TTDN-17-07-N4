import requests
import sys
import json

def test_gemini_native(api_key):
    print("--- KIỂM TRA GOOGLE GEMINI NATIVE API ---")
    # Sử dụng endpoint NATIVE của Google (không qua OpenAI proxy)
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    headers = {
        "Content-Type": "application/json",
    }
    
    data = {
        "contents": [{
            "parts": [{"text": "Xin chào, hãy trả lời ngắn gọn: OK"}]
        }]
    }
    
    print(f"URL: {url}")
    try:
        response = requests.post(url, headers=headers, json=data, timeout=30)
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            print("✅ THÀNH CÔNG! AI phản hồi:")
            print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        else:
            print("❌ THẤT BẠI!")
            print(f"Lỗi: {response.text}")
    except Exception as e:
        print(f"❌ LỖI KẾT NỐI: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Sử dụng: python3 test_gemini_native.py <API_KEY>")
    else:
        test_gemini_native(sys.argv[1])
