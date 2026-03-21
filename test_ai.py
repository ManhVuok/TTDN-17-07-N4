import requests
import sys
import json

def test_ai(api_key, provider="google"):
    print(f"--- KIỂM TRA {provider.upper()} API ---")
    
    if provider == "google":
        url = "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions"
        model = "gemini-1.5-flash"
    else:
        url = "https://openrouter.ai/api/v1/chat/completions"
        model = "google/gemini-2.0-flash-lite-preview-02-05:free"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    
    if provider == "openrouter":
        headers["HTTP-Referer"] = "http://localhost:8069"
        headers["X-Title"] = "Odoo Testing Script"
    
    data = {
        "model": model,
        "messages": [
            {"role": "user", "content": "Xin chào, hãy trả lời ngắn gọn: OK"}
        ]
    }
    
    print(f"URL: {url}")
    print(f"Model: {model}")
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
        print("Sử dụng: python3 test_ai.py <API_KEY> [google|openrouter]")
    else:
        provider = sys.argv[2] if len(sys.argv) > 2 else "google"
        test_ai(sys.argv[1], provider)
