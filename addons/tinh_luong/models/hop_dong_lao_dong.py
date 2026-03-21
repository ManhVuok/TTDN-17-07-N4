# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date


class HopDongLaoDong(models.Model):
    """
    Quản lý hợp đồng lao động của nhân viên.
    Liên kết với hồ sơ nhân viên từ module nhan_su.
    """
    _name = 'hop_dong_lao_dong'
    _description = 'Hợp đồng lao động'
    _rec_name = 'ma_hop_dong'
    _order = 'ngay_ky desc'

    # Thông tin cơ bản
    ma_hop_dong = fields.Char("Mã hợp đồng", required=True, copy=False)
    
    # Liên kết với nhân viên từ module nhan_su
    nhan_vien_id = fields.Many2one(
        'nhan_vien', 
        string="Nhân viên", 
        required=True,
        ondelete='cascade'
    )
    
    # Thông tin từ nhân viên (để hiển thị)
    phong_ban_id = fields.Many2one(
        related='nhan_vien_id.phong_ban_id',
        string="Phòng ban",
        store=True,
        readonly=True
    )
    chuc_vu_id = fields.Many2one(
        related='nhan_vien_id.chuc_vu_id',
        string="Chức vụ",
        store=True,
        readonly=True
    )
    
    # Loại hợp đồng
    loai_hop_dong = fields.Selection([
        ('thu_viec', 'Thử việc'),
        ('co_thoi_han', 'Có thời hạn'),
        ('khong_thoi_han', 'Không thời hạn'),
        ('thoi_vu', 'Thời vụ'),
    ], string="Loại hợp đồng", required=True, default='co_thoi_han')
    
    # Thời gian hợp đồng
    ngay_ky = fields.Date("Ngày ký hợp đồng", required=True, default=fields.Date.today)
    ngay_hieu_luc = fields.Date("Ngày hiệu lực", required=True)
    ngay_het_han = fields.Date("Ngày hết hạn")
    
    # Mức lương
    luong_co_ban = fields.Float(
        "Lương cơ bản", 
        required=True,
        help="Mức lương cơ bản theo hợp đồng (VNĐ/tháng)"
    )
    luong_dong_bao_hiem = fields.Float(
        "Lương đóng bảo hiểm",
        help="Mức lương làm căn cứ đóng bảo hiểm (nếu khác lương cơ bản)"
    )
    
    # Trạng thái
    trang_thai = fields.Selection([
        ('moi', 'Mới tạo'),
        ('hieu_luc', 'Đang hiệu lực'),
        ('tam_dung', 'Tạm dừng'),
        ('het_han', 'Hết hạn'),
        ('cham_dut', 'Chấm dứt'),
    ], string="Trạng thái", compute="_compute_trang_thai", store=True)
    
    ngay_cham_dut = fields.Date("Ngày chấm dứt")
    
    # Thông tin bổ sung
    so_nguoi_phu_thuoc = fields.Integer(
        "Số người phụ thuộc",
        default=0,
        help="Số người phụ thuộc để tính giảm trừ gia cảnh"
    )
    
    # Phụ cấp
    phu_cap_ids = fields.Many2many(
        'phu_cap',
        string="Các khoản phụ cấp",
        help="Các khoản phụ cấp áp dụng cho hợp đồng này"
    )
    
    tong_phu_cap = fields.Float(
        "Tổng phụ cấp",
        compute="_compute_tong_phu_cap",
        store=True
    )
    
    # Ghi chú
    ghi_chu = fields.Text("Ghi chú")
    
    # File đính kèm
    file_hop_dong = fields.Binary("File hợp đồng")
    file_hop_dong_name = fields.Char("Tên file")
    
    @api.depends('ngay_hieu_luc', 'ngay_het_han', 'ngay_cham_dut')
    def _compute_trang_thai(self):
        today = date.today()
        for record in self:
            if record.ngay_cham_dut:
                record.trang_thai = 'cham_dut'
            elif not record.ngay_hieu_luc:
                record.trang_thai = 'moi'
            elif record.ngay_hieu_luc > today:
                record.trang_thai = 'moi'
            elif record.ngay_het_han and record.ngay_het_han < today:
                record.trang_thai = 'het_han'
            else:
                record.trang_thai = 'hieu_luc'
    
    @api.depends('phu_cap_ids', 'phu_cap_ids.so_tien')
    def _compute_tong_phu_cap(self):
        for record in self:
            record.tong_phu_cap = sum(record.phu_cap_ids.mapped('so_tien'))
    
    @api.constrains('ngay_hieu_luc', 'ngay_het_han')
    def _check_ngay_hop_dong(self):
        for record in self:
            if record.ngay_het_han and record.ngay_hieu_luc:
                if record.ngay_het_han < record.ngay_hieu_luc:
                    raise ValidationError("Ngày hết hạn phải sau ngày hiệu lực!")
    
    @api.constrains('luong_co_ban')
    def _check_luong_co_ban(self):
        for record in self:
            if record.luong_co_ban <= 0:
                raise ValidationError("Lương cơ bản phải lớn hơn 0!")
    
    @api.onchange('luong_co_ban')
    def _onchange_luong_co_ban(self):
        """Mặc định lương đóng bảo hiểm bằng lương cơ bản"""
        for record in self:
            if not record.luong_dong_bao_hiem:
                record.luong_dong_bao_hiem = record.luong_co_ban
    
    def get_hop_dong_hieu_luc(self, nhan_vien_id, ngay=None):
        """
        Lấy hợp đồng đang hiệu lực của nhân viên tại thời điểm chỉ định
        """
        if not ngay:
            ngay = date.today()
        
        hop_dong = self.search([
            ('nhan_vien_id', '=', nhan_vien_id),
            ('ngay_hieu_luc', '<=', ngay),
            '|',
            ('ngay_het_han', '=', False),
            ('ngay_het_han', '>=', ngay)
        ], limit=1, order='ngay_hieu_luc desc')
        
        return hop_dong
    
    _sql_constraints = [
        ('ma_hop_dong_unique', 'UNIQUE(ma_hop_dong)', 'Mã hợp đồng phải là duy nhất!')
    ]
