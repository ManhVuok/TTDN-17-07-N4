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
    
    # 1. Deactivate duplicate custom menus
    target_names = ('Quản lý nhân sự', 'Chấm công', 'Tính lương', 'Quản lý Nhân sự', 'Tính Lương')
    cur.execute("UPDATE ir_ui_menu SET active = False WHERE name IN %s;", (target_names,))
    
    # 2. Hide standard HR menus that might conflict
    cur.execute("UPDATE ir_ui_menu SET active = False WHERE name IN ('Employees', 'Attendances', 'Recruitment', 'Time Off');")
    
    # 3. Clear old model data to force reload
    cur.execute("DELETE FROM ir_model_data WHERE module IN ('nhan_su', 'cham_cong', 'tinh_luong');")

    # 4. Critical: Delete all custom views that don't have an external ID from these modules
    # This prevents the "Invalid view" errors when Odoo tries to load the clean XML
    cur.execute("""
        DELETE FROM ir_ui_view 
        WHERE (model LIKE 'nhan_%%' OR model LIKE 'cham_%%' OR model LIKE 'don_tu%%')
        AND id NOT IN (SELECT res_id FROM ir_model_data WHERE model = 'ir.ui.view');
    """)
    
    conn.commit()
    print("Database cleanup successful.")
    cur.close()
    conn.close()
except Exception as e:
    print(f"Error during database cleanup: {e}")
