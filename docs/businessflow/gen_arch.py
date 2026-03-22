import base64
import requests

mermaid_code = '''
graph TB
    Client(("Máy khách / Người dùng"))

    subgraph Odoo_Server ["Máy chủ Odoo 15"]
        direction TB
        View["Giao diện Tương tác (XML/JS)"]
        Controller["Bộ Điều hướng (HTTP Controllers)"]
        Model["Tầng Xử lý & ORM (Python Models)"]

        View <--> Controller
        Controller <--> Model
        View <--> Model
    end

    subgraph Database ["Cơ sở dữ liệu"]
        DB[("PostgreSQL")]
    end

    subgraph External_APIs ["Tích hợp AI / API (Mức 3)"]
        Telegram["Telegram Bot API"]
        AI["Google Gemini LLM"]
    end

    Client <-->|HTTP/HTTPS| View
    Client <-->|HTTP/HTTPS| Controller
    Model <-->|SQL/ORM| DB

    Model -->|"Gửi JSON (Báo duyệt đơn)"| Telegram
    Model <-->|"Gọi REST API (Lấy nhận xét)"| AI

    classDef server fill:#f2e6ff,stroke:#8e44ad,stroke-width:2px;
    classDef db fill:#e3f2fd,stroke:#1976d2,stroke-width:2px;
    classDef api fill:#e8f5e9,stroke:#388e3c,stroke-width:2px;
    classDef user fill:#fff3e0,stroke:#f57c00,stroke-width:2px;

    class Odoo_Server server
    class Database,DB db
    class External_APIs,Telegram,AI api
    class Client user
'''
encoded_str = base64.b64encode(mermaid_code.encode('utf-8')).decode('utf-8')
url = 'https://mermaid.ink/img/' + encoded_str + '?bgColor=FFFFFF'

try:
    response = requests.get(url)
    if response.status_code == 200:
        with open('System_Architecture_ChamCong_TinhLuong.png', 'wb') as f:
            f.write(response.content)
        print('DONE!')
    else:
        print('Error', response.status_code, response.text)
except Exception as e:
    print('Failed', e)
