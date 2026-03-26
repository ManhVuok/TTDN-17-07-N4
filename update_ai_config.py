import psycopg2

try:
    conn = psycopg2.connect(
        host="localhost",
        port=5431,
        user="odoo",
        password="odoo",
        database="odoo_vn"
    )
    cur = conn.cursor()
    
    # Cập nhật model name cho cấu hình đang active
    cur.execute("UPDATE ai_cau_hinh_api SET model_name = 'gemini-1.5-flash' WHERE active = True;")
    
    conn.commit()
    print("Database AI config updated to gemini-1.5-flash.")
    cur.close()
    conn.close()
except Exception as e:
    print(f"Error updating AI config: {e}")
