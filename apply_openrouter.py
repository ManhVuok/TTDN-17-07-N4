import psycopg2

def update_openrouter_config():
    try:
        conn = psycopg2.connect(
            host="localhost",
            port=5431,
            user="odoo",
            password="odoo",
            database="odoo_vn"
        )
        cur = conn.cursor()
        
        # Cấu hình OpenRouter
        api_key = "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"
        api_url = "https://openrouter.ai/api/v1/chat/completions"
        model_name = "google/gemini-2.0-flash-001"
        
        sql = """
            UPDATE ai_cau_hinh_api 
            SET api_key = %s, 
                api_url = %s, 
                model_name = %s
            WHERE active = True;
        """
        
        cur.execute(sql, (api_key, api_url, model_name))
        
        if cur.rowcount == 0:
            print("No active config found, trying to update the first available record...")
            cur.execute("UPDATE ai_cau_hinh_api SET api_key = %s, api_url = %s, model_name = %s, active = True WHERE id = (SELECT id FROM ai_cau_hinh_api LIMIT 1);")
            
        conn.commit()
        print("Successfully updated Odoo to use OpenRouter!")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Error updating config: {e}")

if __name__ == "__main__":
    update_openrouter_config()
