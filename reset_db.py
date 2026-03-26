import psycopg2
import sys

def reset_database(clear_assets=False):
    try:
        conn = psycopg2.connect(
            host="localhost",
            port=5431,
            user="odoo",
            password="odoo",
            database="postgres"
        )
        conn.autocommit = True
        cur = conn.cursor()
        
        if clear_assets:
            # Connect to 'odoo_vn' instead
            conn_vn = psycopg2.connect(
                host="localhost",
                port=5431,
                user="odoo",
                password="odoo",
                database="odoo_vn"
            )
            conn_vn.autocommit = True
            cur_vn = conn_vn.cursor()
            print("Clearing Odoo assets to force re-compilation...")
            cur_vn.execute("DELETE FROM ir_attachment WHERE url LIKE '/web/content/%';")
            cur_vn.close()
            conn_vn.close()
        else:
            # Terminate active connections to 'odoo_vn'
            cur.execute("""
                SELECT pg_terminate_backend(pg_stat_activity.pid)
                FROM pg_stat_activity
                WHERE pg_stat_activity.datname = 'odoo_vn'
                  AND pid <> pg_backend_pid();
            """)
            
            # Drop and recreate
            print("Dropping database odoo_vn...")
            cur.execute("DROP DATABASE IF EXISTS odoo_vn;")
            print("Creating database odoo_vn...")
            cur.execute("CREATE DATABASE odoo_vn OWNER odoo;")
        
        cur.close()
        conn.close()
        print("Database operation successful.")
        return True
    except Exception as e:
        print(f"Error during database operation: {e}")
        return False

if __name__ == "__main__":
    clear_assets = "--clear-assets" in sys.argv
    reset_database(clear_assets=clear_assets)
