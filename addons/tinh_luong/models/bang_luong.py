# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError
from datetime import date
import calendar


class BangLuong(models.Model):
    """
    Bảng lương theo tháng.
    Quản lý quy trình tính lương cho toàn bộ nhân viên trong tháng.
    """
    _name = 'bang_luong'
    _description = 'Bảng lương tháng'
    _rec_name = 'ten_bang_luong'
    _order = 'nam desc, thang desc'

    # Thông tin cơ bản
    ma_bang_luong = fields.Char("Mã bảng lương", required=True, copy=False)
    ten_bang_luong = fields.Char(
        "Tên bảng lương",
        compute="_compute_ten_bang_luong",
        store=True
    )
    
    # Kỳ lương
    thang = fields.Selection(
        [(str(i), f'Tháng {i}') for i in range(1, 13)],
        string="Tháng",
        required=True
    )
    nam = fields.Char("Năm", required=True, default=lambda self: str(date.today().year))
    
    # Thời gian tính lương
    ngay_bat_dau = fields.Date(
        "Từ ngày",
        compute="_compute_thoi_gian",
        store=True
    )
    ngay_ket_thuc = fields.Date(
        "Đến ngày",
        compute="_compute_thoi_gian",
        store=True
    )
    
    # Cấu hình lương áp dụng
    cau_hinh_luong_id = fields.Many2one(
        'cau_hinh_luong',
        string="Cấu hình lương",
        required=True,
        default=lambda self: self.env['cau_hinh_luong'].search([('active', '=', True)], limit=1).id
    )
    
    # Chi tiết lương từng nhân viên
    chi_tiet_luong_ids = fields.One2many(
        'chi_tiet_luong',
        inverse_name='bang_luong_id',
        string="Chi tiết lương"
    )
    
    # Thống kê
    tong_nhan_vien = fields.Integer(
        "Tổng số nhân viên",
        compute="_compute_thong_ke",
        store=True
    )
    tong_luong_gross = fields.Float(
        "Tổng lương Gross",
        compute="_compute_thong_ke",
        store=True
    )
    tong_luong_net = fields.Float(
        "Tổng lương Net",
        compute="_compute_thong_ke",
        store=True
    )
    tong_bao_hiem = fields.Float(
        "Tổng BH người LĐ đóng",
        compute="_compute_thong_ke",
        store=True
    )
    
    # Trạng thái
    trang_thai = fields.Selection([
        ('nhap', 'Nháp'),
        ('da_tinh', 'Đã tính lương'),
        ('cho_duyet', 'Chờ duyệt'),
        ('da_duyet', 'Đã duyệt'),
        ('da_tra', 'Đã trả lương'),
        ('huy', 'Đã hủy'),
    ], string="Trạng thái", default='nhap', required=True)
    
    # Người phê duyệt
    nguoi_duyet_id = fields.Many2one('res.users', string="Người duyệt")
    ngay_duyet = fields.Datetime("Ngày duyệt")
    
    # Ghi chú
    ghi_chu = fields.Text("Ghi chú")
    
    @api.depends('thang', 'nam')
    def _compute_ten_bang_luong(self):
        for record in self:
            if record.thang and record.nam:
                record.ten_bang_luong = f"Bảng lương tháng {record.thang}/{record.nam}"
            else:
                record.ten_bang_luong = "Bảng lương mới"
    
    @api.depends('thang', 'nam')
    def _compute_thoi_gian(self):
        for record in self:
            if record.thang and record.nam:
                thang = int(record.thang)
                nam = int(record.nam)
                record.ngay_bat_dau = date(nam, thang, 1)
                record.ngay_ket_thuc = date(nam, thang, calendar.monthrange(nam, thang)[1])
            else:
                record.ngay_bat_dau = False
                record.ngay_ket_thuc = False
    
    @api.depends('chi_tiet_luong_ids', 'chi_tiet_luong_ids.luong_thuc_nhan',
                 'chi_tiet_luong_ids.tong_thu_nhap', 'chi_tiet_luong_ids.tong_bao_hiem')
    def _compute_thong_ke(self):
        for record in self:
            record.tong_nhan_vien = len(record.chi_tiet_luong_ids)
            record.tong_luong_gross = sum(record.chi_tiet_luong_ids.mapped('tong_thu_nhap'))
            record.tong_luong_net = sum(record.chi_tiet_luong_ids.mapped('luong_thuc_nhan'))
            record.tong_bao_hiem = sum(record.chi_tiet_luong_ids.mapped('tong_bao_hiem'))
    
    def action_tao_chi_tiet(self):
        """
        Tạo chi tiết lương cho tất cả nhân viên có hợp đồng hiệu lực
        """
        self.ensure_one()
        
        if self.trang_thai != 'nhap':
            raise UserError("Chỉ có thể tạo chi tiết khi bảng lương ở trạng thái Nháp!")
        
        # Xóa chi tiết cũ nếu có
        self.chi_tiet_luong_ids.unlink()
        
        # Lấy tất cả nhân viên có hợp đồng hiệu lực
        hop_dong_model = self.env['hop_dong_lao_dong']
        nhan_vien_model = self.env['nhan_vien']
        
        # Lấy tất cả nhân viên
        all_nhan_vien = nhan_vien_model.search([])
        
        chi_tiet_vals = []
        for nhan_vien in all_nhan_vien:
            # Kiểm tra có hợp đồng hiệu lực không
            hop_dong = hop_dong_model.search([
                ('nhan_vien_id', '=', nhan_vien.id),
                ('trang_thai', '=', 'hieu_luc')
            ], limit=1, order='ngay_hieu_luc desc')
            
            if hop_dong:
                chi_tiet_vals.append({
                    'bang_luong_id': self.id,
                    'nhan_vien_id': nhan_vien.id,
                    'hop_dong_id': hop_dong.id,
                })
        
        if chi_tiet_vals:
            self.env['chi_tiet_luong'].create(chi_tiet_vals)
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Thành công',
                'message': f'Đã tạo chi tiết lương cho {len(chi_tiet_vals)} nhân viên',
                'type': 'success',
            }
        }
    
    def action_tinh_luong(self):
        """
        Tính lương cho tất cả nhân viên trong bảng lương
        """
        self.ensure_one()
        
        if self.trang_thai not in ['nhap', 'da_tinh']:
            raise UserError("Không thể tính lương ở trạng thái hiện tại!")
        
        if not self.chi_tiet_luong_ids:
            raise UserError("Chưa có chi tiết lương! Vui lòng tạo chi tiết trước.")
        
        # Tính lương cho từng nhân viên
        for chi_tiet in self.chi_tiet_luong_ids:
            chi_tiet.action_tinh_luong()
        
        self.trang_thai = 'da_tinh'
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Thành công',
                'message': 'Đã tính lương cho tất cả nhân viên!',
                'type': 'success',
            }
        }
    
    def action_gui_duyet(self):
        """Gửi duyệt bảng lương"""
        self.ensure_one()
        if self.trang_thai != 'da_tinh':
            raise UserError("Chỉ có thể gửi duyệt sau khi đã tính lương!")
        self.trang_thai = 'cho_duyet'
    
    def action_duyet(self):
        """Duyệt bảng lương"""
        self.ensure_one()
        if self.trang_thai != 'cho_duyet':
            raise UserError("Chỉ có thể duyệt khi ở trạng thái Chờ duyệt!")
        self.write({
            'trang_thai': 'da_duyet',
            'nguoi_duyet_id': self.env.user.id,
            'ngay_duyet': fields.Datetime.now(),
        })
    
    def action_tra_luong(self):
        """Xác nhận đã trả lương"""
        self.ensure_one()
        if self.trang_thai != 'da_duyet':
            raise UserError("Chỉ có thể xác nhận trả lương sau khi đã duyệt!")
        self.trang_thai = 'da_tra'
    
    def action_huy(self):
        """Hủy bảng lương"""
        self.ensure_one()
        if self.trang_thai == 'da_tra':
            raise UserError("Không thể hủy bảng lương đã trả!")
        self.trang_thai = 'huy'
    
    def action_reset(self):
        """Đặt lại về trạng thái nháp"""
        self.ensure_one()
        if self.trang_thai == 'da_tra':
            raise UserError("Không thể reset bảng lương đã trả!")
        self.trang_thai = 'nhap'
    
    _sql_constraints = [
        ('ma_bang_luong_unique', 'UNIQUE(ma_bang_luong)', 'Mã bảng lương phải là duy nhất!'),
        ('thang_nam_unique', 'UNIQUE(thang, nam)', 'Đã tồn tại bảng lương cho tháng này!')
    ]
