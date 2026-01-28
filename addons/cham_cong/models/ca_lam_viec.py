# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta


class CaLamViec(models.Model):
    """
    Định nghĩa các ca làm việc trong công ty.
    VD: Ca sáng, Ca chiều, Ca đêm, Ca hành chính, etc.
    """
    _name = 'ca_lam_viec'
    _description = 'Ca làm việc'
    _order = 'gio_bat_dau'
    
    # ==================== THÔNG TIN CƠ BẢN ====================
    ma_ca = fields.Char("Mã ca", required=True)
    ten_ca = fields.Char("Tên ca", required=True)
    mo_ta = fields.Text("Mô tả")
    
    # ==================== THỜI GIAN ====================
    gio_bat_dau = fields.Float(
        "Giờ bắt đầu", 
        required=True,
        help="Giờ bắt đầu ca (VD: 8.0 = 8:00, 8.5 = 8:30)"
    )
    gio_ket_thuc = fields.Float(
        "Giờ kết thúc", 
        required=True,
        help="Giờ kết thúc ca (VD: 17.0 = 17:00)"
    )
    
    gio_nghi_bat_dau = fields.Float(
        "Giờ nghỉ trưa (bắt đầu)",
        default=12.0
    )
    gio_nghi_ket_thuc = fields.Float(
        "Giờ nghỉ trưa (kết thúc)",
        default=13.0
    )
    
    # ==================== COMPUTED ====================
    so_gio_lam = fields.Float(
        "Số giờ làm",
        compute="_compute_so_gio_lam",
        store=True
    )
    
    thoi_gian_hien_thi = fields.Char(
        "Thời gian",
        compute="_compute_thoi_gian_hien_thi"
    )
    
    # ==================== CẤU HÌNH ====================
    loai_ca = fields.Selection([
        ('hanh_chinh', 'Ca hành chính'),
        ('sang', 'Ca sáng'),
        ('chieu', 'Ca chiều'),
        ('dem', 'Ca đêm'),
        ('lien_tuc', 'Ca liên tục'),
    ], string="Loại ca", default='hanh_chinh', required=True)
    
    la_ca_dem = fields.Boolean(
        "Là ca đêm",
        default=False,
        help="Ca đêm được tính hệ số lương cao hơn"
    )
    
    he_so_luong = fields.Float(
        "Hệ số lương",
        default=1.0,
        help="Hệ số nhân với lương giờ (VD: ca đêm = 1.3)"
    )
    
    active = fields.Boolean("Đang sử dụng", default=True)
    
    # ==================== SQL CONSTRAINTS ====================
    _sql_constraints = [
        ('unique_ma_ca', 'UNIQUE(ma_ca)', 'Mã ca làm việc phải là duy nhất!'),
    ]
    
    # ==================== COMPUTE METHODS ====================
    @api.depends('gio_bat_dau', 'gio_ket_thuc', 'gio_nghi_bat_dau', 'gio_nghi_ket_thuc')
    def _compute_so_gio_lam(self):
        for record in self:
            tong_gio = record.gio_ket_thuc - record.gio_bat_dau
            # Trừ giờ nghỉ trưa nếu có
            if record.gio_nghi_bat_dau and record.gio_nghi_ket_thuc:
                gio_nghi = record.gio_nghi_ket_thuc - record.gio_nghi_bat_dau
                if gio_nghi > 0:
                    tong_gio -= gio_nghi
            record.so_gio_lam = max(0, tong_gio)
    
    @api.depends('gio_bat_dau', 'gio_ket_thuc')
    def _compute_thoi_gian_hien_thi(self):
        for record in self:
            def format_gio(gio):
                h = int(gio)
                m = int((gio - h) * 60)
                return f"{h:02d}:{m:02d}"
            
            record.thoi_gian_hien_thi = f"{format_gio(record.gio_bat_dau)} - {format_gio(record.gio_ket_thuc)}"
    
    def name_get(self):
        result = []
        for record in self:
            name = f"[{record.ma_ca}] {record.ten_ca} ({record.thoi_gian_hien_thi})"
            result.append((record.id, name))
        return result
    
    @api.constrains('gio_bat_dau', 'gio_ket_thuc')
    def _check_gio(self):
        for record in self:
            if record.gio_bat_dau >= record.gio_ket_thuc and not record.la_ca_dem:
                raise ValidationError("Giờ kết thúc phải sau giờ bắt đầu!")
            if record.gio_bat_dau < 0 or record.gio_bat_dau > 24:
                raise ValidationError("Giờ bắt đầu không hợp lệ!")
            if record.gio_ket_thuc < 0 or record.gio_ket_thuc > 24:
                raise ValidationError("Giờ kết thúc không hợp lệ!")


class DangKyTangCa(models.Model):
    """
    Đăng ký làm thêm giờ (tăng ca/overtime).
    Nhân viên hoặc quản lý đăng ký cho nhân viên làm thêm giờ.
    """
    _name = 'dang_ky_tang_ca'
    _description = 'Đăng ký tăng ca'
    _order = 'ngay_tang_ca desc, id desc'
    _rec_name = 'ten_hien_thi'
    
    # ==================== THÔNG TIN CƠ BẢN ====================
    ten_hien_thi = fields.Char(
        "Tên hiển thị",
        compute="_compute_ten_hien_thi",
        store=True
    )
    
    nhan_vien_id = fields.Many2one(
        'nhan_vien',
        string="Nhân viên",
        required=True,
        domain="[('trang_thai', '=', 'dang_lam')]"
    )
    
    phong_ban_id = fields.Many2one(
        related='nhan_vien_id.phong_ban_id',
        string="Phòng ban",
        store=True,
        readonly=True
    )
    
    # ==================== THỜI GIAN TĂNG CA ====================
    ngay_tang_ca = fields.Date(
        "Ngày tăng ca",
        required=True,
        default=fields.Date.today
    )
    
    loai_ngay = fields.Selection([
        ('ngay_thuong', 'Ngày thường'),
        ('cuoi_tuan', 'Cuối tuần (T7, CN)'),
        ('ngay_le', 'Ngày lễ'),
    ], string="Loại ngày", default='ngay_thuong', required=True)
    
    ca_lam_viec_id = fields.Many2one(
        'ca_lam_viec',
        string="Ca làm chính",
        help="Ca làm việc chính trong ngày (nếu có)"
    )
    
    gio_bat_dau = fields.Float(
        "Giờ bắt đầu tăng ca",
        required=True,
        default=17.5,
        help="VD: 17.5 = 17:30"
    )
    
    gio_ket_thuc = fields.Float(
        "Giờ kết thúc tăng ca",
        required=True,
        default=20.0,
        help="VD: 20.0 = 20:00"
    )
    
    so_gio_tang_ca = fields.Float(
        "Số giờ tăng ca",
        compute="_compute_so_gio_tang_ca",
        store=True
    )
    
    # ==================== HỆ SỐ LƯƠNG ====================
    he_so_tang_ca = fields.Float(
        "Hệ số tăng ca",
        compute="_compute_he_so_tang_ca",
        store=True,
        help="Hệ số nhân với lương giờ"
    )
    
    # ==================== TRẠNG THÁI ====================
    trang_thai = fields.Selection([
        ('nhap', 'Nháp'),
        ('cho_duyet', 'Chờ duyệt'),
        ('da_duyet', 'Đã duyệt'),
        ('hoan_thanh', 'Hoàn thành'),
        ('tu_choi', 'Từ chối'),
        ('huy', 'Đã hủy'),
    ], string="Trạng thái", default='nhap', required=True)
    
    # ==================== THÔNG TIN PHÊ DUYỆT ====================
    nguoi_duyet_id = fields.Many2one(
        'res.users',
        string="Người duyệt",
        readonly=True
    )
    ngay_duyet = fields.Datetime("Ngày duyệt", readonly=True)
    ly_do_tu_choi = fields.Text("Lý do từ chối")
    
    # ==================== LÝ DO & GHI CHÚ ====================
    ly_do_tang_ca = fields.Text("Lý do tăng ca")
    cong_viec_thuc_hien = fields.Text("Công việc thực hiện")
    ghi_chu = fields.Text("Ghi chú")
    
    # ==================== GIỜ THỰC TẾ (SAU KHI HOÀN THÀNH) ====================
    gio_bat_dau_thuc_te = fields.Float("Giờ bắt đầu thực tế")
    gio_ket_thuc_thuc_te = fields.Float("Giờ kết thúc thực tế")
    so_gio_thuc_te = fields.Float(
        "Số giờ thực tế",
        compute="_compute_so_gio_thuc_te",
        store=True
    )
    
    # ==================== SQL CONSTRAINTS ====================
    _sql_constraints = [
        ('unique_nv_ngay', 'UNIQUE(nhan_vien_id, ngay_tang_ca, gio_bat_dau)', 
         'Nhân viên đã có đăng ký tăng ca vào thời điểm này!'),
    ]
    
    # ==================== COMPUTE METHODS ====================
    @api.depends('nhan_vien_id', 'ngay_tang_ca')
    def _compute_ten_hien_thi(self):
        for record in self:
            if record.nhan_vien_id and record.ngay_tang_ca:
                record.ten_hien_thi = f"{record.nhan_vien_id.ho_va_ten} - {record.ngay_tang_ca}"
            else:
                record.ten_hien_thi = "Đăng ký tăng ca mới"
    
    @api.depends('gio_bat_dau', 'gio_ket_thuc')
    def _compute_so_gio_tang_ca(self):
        for record in self:
            if record.gio_ket_thuc > record.gio_bat_dau:
                record.so_gio_tang_ca = record.gio_ket_thuc - record.gio_bat_dau
            else:
                record.so_gio_tang_ca = 0
    
    @api.depends('gio_bat_dau_thuc_te', 'gio_ket_thuc_thuc_te')
    def _compute_so_gio_thuc_te(self):
        for record in self:
            if record.gio_ket_thuc_thuc_te > record.gio_bat_dau_thuc_te:
                record.so_gio_thuc_te = record.gio_ket_thuc_thuc_te - record.gio_bat_dau_thuc_te
            else:
                record.so_gio_thuc_te = 0
    
    @api.depends('loai_ngay')
    def _compute_he_so_tang_ca(self):
        """
        Tính hệ số tăng ca theo quy định:
        - Ngày thường: 150%
        - Cuối tuần: 200%
        - Ngày lễ: 300%
        """
        for record in self:
            if record.loai_ngay == 'ngay_thuong':
                record.he_so_tang_ca = 1.5
            elif record.loai_ngay == 'cuoi_tuan':
                record.he_so_tang_ca = 2.0
            elif record.loai_ngay == 'ngay_le':
                record.he_so_tang_ca = 3.0
            else:
                record.he_so_tang_ca = 1.5
    
    @api.onchange('ngay_tang_ca')
    def _onchange_ngay_tang_ca(self):
        """Tự động detect loại ngày"""
        if self.ngay_tang_ca:
            weekday = self.ngay_tang_ca.weekday()
            if weekday >= 5:  # Thứ 7 (5) hoặc CN (6)
                self.loai_ngay = 'cuoi_tuan'
            else:
                self.loai_ngay = 'ngay_thuong'
    
    # ==================== ACTIONS ====================
    def action_gui_duyet(self):
        """Gửi đăng ký để duyệt"""
        for record in self:
            if record.trang_thai != 'nhap':
                raise ValidationError("Chỉ có thể gửi duyệt đăng ký ở trạng thái Nháp!")
            record.trang_thai = 'cho_duyet'
    
    def action_duyet(self):
        """Phê duyệt đăng ký tăng ca"""
        for record in self:
            if record.trang_thai != 'cho_duyet':
                raise ValidationError("Chỉ có thể duyệt đăng ký đang chờ duyệt!")
            record.write({
                'trang_thai': 'da_duyet',
                'nguoi_duyet_id': self.env.user.id,
                'ngay_duyet': fields.Datetime.now(),
            })
    
    def action_tu_choi(self):
        """Từ chối đăng ký"""
        for record in self:
            if record.trang_thai != 'cho_duyet':
                raise ValidationError("Chỉ có thể từ chối đăng ký đang chờ duyệt!")
            record.write({
                'trang_thai': 'tu_choi',
                'nguoi_duyet_id': self.env.user.id,
                'ngay_duyet': fields.Datetime.now(),
            })
    
    def action_hoan_thanh(self):
        """Xác nhận hoàn thành tăng ca"""
        for record in self:
            if record.trang_thai != 'da_duyet':
                raise ValidationError("Chỉ có thể hoàn thành đăng ký đã được duyệt!")
            # Nếu chưa nhập giờ thực tế, lấy giờ đăng ký
            if not record.gio_bat_dau_thuc_te:
                record.gio_bat_dau_thuc_te = record.gio_bat_dau
            if not record.gio_ket_thuc_thuc_te:
                record.gio_ket_thuc_thuc_te = record.gio_ket_thuc
            record.trang_thai = 'hoan_thanh'
    
    def action_huy(self):
        """Hủy đăng ký"""
        for record in self:
            if record.trang_thai in ['hoan_thanh']:
                raise ValidationError("Không thể hủy đăng ký đã hoàn thành!")
            record.trang_thai = 'huy'
    
    def action_reset(self):
        """Đặt lại về nháp"""
        for record in self:
            if record.trang_thai == 'hoan_thanh':
                raise ValidationError("Không thể reset đăng ký đã hoàn thành!")
            record.write({
                'trang_thai': 'nhap',
                'nguoi_duyet_id': False,
                'ngay_duyet': False,
                'ly_do_tu_choi': False,
            })
    
    @api.constrains('gio_bat_dau', 'gio_ket_thuc')
    def _check_gio_tang_ca(self):
        for record in self:
            if record.gio_bat_dau >= record.gio_ket_thuc:
                raise ValidationError("Giờ kết thúc phải sau giờ bắt đầu!")
            if record.so_gio_tang_ca > 4:
                raise ValidationError("Số giờ tăng ca trong một lần không được quá 4 giờ!")
