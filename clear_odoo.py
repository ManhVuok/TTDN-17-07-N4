# Chạy lệnh: venv/bin/python odoo-bin.py shell -c odoo.conf -d odoo_vn < clear_odoo.py

print("--- ĐANG DỌN DẸP DỮ LIỆU NHÂN SỰ, CHẤM CÔNG, LƯƠNG ---")

# Xóa dữ liệu Chấm công
env['bang_cham_cong'].search([]).unlink()
env['dang_ky_ca_lam_theo_ngay'].search([]).unlink()
env['dang_ky_tang_ca'].search([]).unlink()
env['dot_dang_ky'].search([]).unlink()
env['don_tu'].search([]).unlink()

# Xóa dữ liệu Lương
env['chi_tiet_luong'].search([]).unlink()
env['bang_luong'].search([]).unlink()
env['hop_dong_lao_dong'].search([]).unlink()

# Xóa dữ liệu Nhân sự
env['lich_su_cong_tac'].search([]).unlink()
env['danh_sach_chung_chi_bang_cap'].search([]).unlink()
env['nhan_vien'].search([]).unlink()

env.cr.commit()
print("✅ HOÀN TẤT: Đã dọn sạch dữ liệu cũ. Sẵn sàng nạp 10 data mới.")
