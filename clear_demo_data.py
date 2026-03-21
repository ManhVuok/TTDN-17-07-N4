import psycopg2
import sys

def clear_data(db_name):
    print(f"--- ĐANG XÓA DỮ LIỆU CŨ TRONG DATABASE: {db_name} ---")
    try:
        conn = psycopg2.connect(dbname=db_name, user='odoo', password='odoo', host='localhost')
        cur = conn.cursor()
        
        # Xóa theo thứ tự ngược lại của ràng buộc (Foreign Key)
        tables = [
            'chi_tiet_luong',
            'bang_luong',
            'hop_dong_lao_dong',
            'lich_su_cong_tac',
            'danh_sach_chung_chi_bang_cap',
            'nhan_vien'
        ]
        
        for table in tables:
            print(f"Đang xóa bảng: {table}...")
            cur.execute(f"DELETE FROM {table};")
        
        conn.commit()
        cur.close()
        conn.close()
        print("✅ THÀNH CÔNG! Đã dọn dẹp dữ liệu cũ.")
    except Exception as e:
        print(f"❌ THẤT BẠI: {str(e)}")

if __name__ == "__main__":
    db = sys.argv[1] if len(sys.argv) > 1 else "odoo_vn"
    clear_data(db)
