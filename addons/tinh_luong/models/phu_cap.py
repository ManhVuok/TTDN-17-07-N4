# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class PhuCap(models.Model):
    """
    Quản lý các loại phụ cấp cho nhân viên.
    Có thể áp dụng theo chức vụ, phòng ban hoặc cá nhân.
    """
    _name = 'phu_cap'
    _description = 'Phụ cấp'
    _rec_name = 'ten_phu_cap'
    _order = 'loai_phu_cap, ten_phu_cap'

    # Thông tin cơ bản
    ma_phu_cap = fields.Char("Mã phụ cấp", required=True)
    ten_phu_cap = fields.Char("Tên phụ cấp", required=True)
    
    # Loại phụ cấp
    loai_phu_cap = fields.Selection([
        ('co_dinh', 'Cố định'),
        ('theo_chuc_vu', 'Theo chức vụ'),
        ('theo_phong_ban', 'Theo phòng ban'),
        ('theo_tham_nien', 'Theo thâm niên'),
        ('khac', 'Khác'),
    ], string="Loại phụ cấp", required=True, default='co_dinh')
    
    # Số tiền phụ cấp
    so_tien = fields.Float("Số tiền (VNĐ)", required=True)
    
    # Điều kiện áp dụng (tuỳ chọn)
    chuc_vu_ids = fields.Many2many(
        'chuc_vu',
        string="Áp dụng cho chức vụ",
        help="Để trống nếu áp dụng cho tất cả"
    )
    phong_ban_ids = fields.Many2many(
        'phong_ban',
        string="Áp dụng cho phòng ban",
        help="Để trống nếu áp dụng cho tất cả"
    )
    
    # Tính chất
    tinh_thue = fields.Boolean(
        "Tính thuế TNCN",
        default=True,
        help="Phụ cấp này có tính vào thu nhập chịu thuế TNCN không?"
    )
    tinh_bao_hiem = fields.Boolean(
        "Tính bảo hiểm",
        default=False,
        help="Phụ cấp này có tính vào thu nhập đóng bảo hiểm không?"
    )
    
    # Trạng thái
    active = fields.Boolean("Đang sử dụng", default=True)
    
    # Mô tả
    mo_ta = fields.Text("Mô tả")
    
    @api.constrains('so_tien')
    def _check_so_tien(self):
        for record in self:
            if record.so_tien < 0:
                raise ValidationError("Số tiền phụ cấp phải >= 0!")
    
    _sql_constraints = [
        ('ma_phu_cap_unique', 'UNIQUE(ma_phu_cap)', 'Mã phụ cấp phải là duy nhất!')
    ]


class LoaiKhauTru(models.Model):
    """
    Các loại khấu trừ khác (ngoài bảo hiểm và đi muộn/về sớm)
    """
    _name = 'loai_khau_tru'
    _description = 'Loại khấu trừ'
    _rec_name = 'ten_khau_tru'

    ma_khau_tru = fields.Char("Mã khấu trừ", required=True)
    ten_khau_tru = fields.Char("Tên khấu trừ", required=True)
    
    loai = fields.Selection([
        ('co_dinh', 'Cố định hàng tháng'),
        ('phan_tram', 'Phần trăm lương'),
        ('thu_cong', 'Nhập thủ công'),
    ], string="Loại khấu trừ", required=True, default='co_dinh')
    
    gia_tri = fields.Float("Giá trị", help="Số tiền cố định hoặc % lương")
    
    mo_ta = fields.Text("Mô tả")
    active = fields.Boolean("Đang sử dụng", default=True)
    
    _sql_constraints = [
        ('ma_khau_tru_unique', 'UNIQUE(ma_khau_tru)', 'Mã khấu trừ phải là duy nhất!')
    ]
