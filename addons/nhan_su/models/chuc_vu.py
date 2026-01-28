from odoo import models, fields, api

class ChucVu(models.Model):
    _name = 'chuc_vu'
    _description = 'Bảng chứa thông tin chức vụ'
    _rec_name = 'ten_chuc_vu'
    _order = 'cap_bac desc, ten_chuc_vu'

    ma_chuc_vu = fields.Char("Mã chức vụ", required=True)
    ten_chuc_vu = fields.Char("Tên chức vụ", required=True)
    
    # Thông tin bổ sung cho module tính lương
    cap_bac = fields.Integer(
        "Cấp bậc",
        default=1,
        help="Cấp bậc chức vụ (số càng lớn = cấp càng cao)"
    )
    luong_co_ban_de_xuat = fields.Float(
        "Lương cơ bản đề xuất",
        help="Mức lương cơ bản đề xuất cho chức vụ này (VNĐ/tháng)"
    )
    phu_cap_chuc_vu = fields.Float(
        "Phụ cấp chức vụ",
        default=0,
        help="Mức phụ cấp theo chức vụ (VNĐ/tháng)"
    )
    mo_ta = fields.Text("Mô tả công việc")
    
    _sql_constraints = [
        ('ma_chuc_vu_unique', 'UNIQUE(ma_chuc_vu)', 'Mã chức vụ phải là duy nhất!')
    ]