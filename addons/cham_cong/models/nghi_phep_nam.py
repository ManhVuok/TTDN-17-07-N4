# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError
from datetime import date

class NghiPhepNam(models.Model):
    """
    Quản lý số ngày nghỉ phép của nhân viên theo năm.
    Mỗi nhân viên có một bản ghi cho mỗi năm.
    """
    _name = 'nghi_phep_nam'
    _description = 'Nghỉ phép năm'
    _rec_name = 'display_name'
    _order = 'nam desc, nhan_vien_id'
    
    # ==================== THÔNG TIN CƠ BẢN ====================
    nhan_vien_id = fields.Many2one(
        'hr.employee',
        string="Nhân viên",
        required=True,
        ondelete='cascade',
        domain="[('trang_thai', '=', 'dang_lam')]"
    )
    
    phong_ban_id = fields.Many2one(
        related='nhan_vien_id.department_id',
        string="Phòng ban",
        store=True,
        readonly=True
    )
    
    nam = fields.Integer(
        "Năm",
        required=True,
        default=lambda self: date.today().year
    )
    
    display_name = fields.Char(
        "Tên hiển thị",
        compute="_compute_display_name",
        store=True
    )
    
    # ==================== SỐ NGÀY PHÉP ====================
    so_ngay_phep_nam = fields.Float(
        "Số ngày phép năm",
        default=12.0,
        help="Số ngày phép được hưởng trong năm (mặc định 12 ngày)"
    )
    
    so_ngay_phep_them = fields.Float(
        "Phép thâm niên",
        default=0.0,
        help="Số ngày phép thêm theo thâm niên"
    )
    
    so_ngay_phep_chuyen = fields.Float(
        "Phép năm trước chuyển sang",
        default=0.0,
        help="Số ngày phép từ năm trước chưa sử dụng (tối đa 5 ngày)"
    )
    
    tong_ngay_phep = fields.Float(
        "Tổng ngày phép",
        compute="_compute_tong_ngay_phep",
        store=True
    )
    
    # ==================== SỬ DỤNG ====================
    so_ngay_da_nghi = fields.Float(
        "Số ngày đã nghỉ",
        compute="_compute_ngay_da_nghi",
        store=True,
        help="Số ngày đã nghỉ phép (từ đơn được duyệt)"
    )
    
    so_ngay_cho_duyet = fields.Float(
        "Số ngày chờ duyệt",
        compute="_compute_ngay_da_nghi",
        store=True,
        help="Số ngày đang chờ duyệt"
    )
    
    so_ngay_con_lai = fields.Float(
        "Số ngày còn lại",
        compute="_compute_ngay_con_lai",
        store=True
    )
    
    # ==================== GHI CHÚ ====================
    ghi_chu = fields.Text("Ghi chú")
    
    # ==================== SQL CONSTRAINTS ====================
    _sql_constraints = [
        ('unique_nhan_vien_nam', 'UNIQUE(nhan_vien_id, nam)', 
         'Mỗi nhân viên chỉ có một bản ghi nghỉ phép cho mỗi năm!'),
    ]
    
    # ==================== COMPUTE METHODS ====================
    @api.depends('nhan_vien_id', 'nam')
    def _compute_display_name(self):
        for record in self:
            if record.nhan_vien_id and record.nam:
                record.display_name = f"{record.nhan_vien_id.name} - {record.nam}"
            else:
                record.display_name = "Nghỉ phép mới"
    
    @api.depends('so_ngay_phep_nam', 'so_ngay_phep_them', 'so_ngay_phep_chuyen')
    def _compute_tong_ngay_phep(self):
        for record in self:
            record.tong_ngay_phep = (
                record.so_ngay_phep_nam + 
                record.so_ngay_phep_them + 
                record.so_ngay_phep_chuyen
            )
    
    @api.depends('nhan_vien_id', 'nam')
    def _compute_ngay_da_nghi(self):
        """Tính số ngày đã nghỉ từ các đơn nghỉ phép được duyệt"""
        for record in self:
            if not record.nhan_vien_id or not record.nam:
                record.so_ngay_da_nghi = 0
                record.so_ngay_cho_duyet = 0
                continue
            
            # Đơn nghỉ phép năm đã duyệt trong năm
            don_da_duyet = self.env['don_tu'].search([
                ('nhan_vien_id', '=', record.nhan_vien_id.id),
                ('loai_don', '=', 'nghi_phep'),
                ('trang_thai_duyet', '=', 'da_duyet'),
                ('ngay_ap_dung', '>=', f'{record.nam}-01-01'),
                ('ngay_ap_dung', '<=', f'{record.nam}-12-31'),
            ])
            
            # Đơn nghỉ phép năm đang chờ duyệt
            don_cho_duyet = self.env['don_tu'].search([
                ('nhan_vien_id', '=', record.nhan_vien_id.id),
                ('loai_don', '=', 'nghi_phep'),
                ('trang_thai_duyet', '=', 'cho_duyet'),
                ('ngay_ap_dung', '>=', f'{record.nam}-01-01'),
                ('ngay_ap_dung', '<=', f'{record.nam}-12-31'),
            ])
            
            # Tính số ngày
            so_ngay_da_nghi = 0
            for don in don_da_duyet:
                if don.ngay_ket_thuc:
                    so_ngay = (don.ngay_ket_thuc - don.ngay_ap_dung).days + 1
                else:
                    so_ngay = 1
                so_ngay_da_nghi += so_ngay
            
            so_ngay_cho_duyet = 0
            for don in don_cho_duyet:
                if don.ngay_ket_thuc:
                    so_ngay = (don.ngay_ket_thuc - don.ngay_ap_dung).days + 1
                else:
                    so_ngay = 1
                so_ngay_cho_duyet += so_ngay
            
            record.so_ngay_da_nghi = so_ngay_da_nghi
            record.so_ngay_cho_duyet = so_ngay_cho_duyet
    
    @api.depends('tong_ngay_phep', 'so_ngay_da_nghi', 'so_ngay_cho_duyet')
    def _compute_ngay_con_lai(self):
        for record in self:
            record.so_ngay_con_lai = record.tong_ngay_phep - record.so_ngay_da_nghi
    
    # ==================== ACTIONS ====================
    def action_cap_nhat_phep(self):
        """Cập nhật lại số ngày phép đã sử dụng"""
        for record in self:
            record._compute_ngay_da_nghi()
        return True
    
    def action_xem_don_nghi(self):
        """Xem danh sách đơn nghỉ phép của nhân viên trong năm"""
        self.ensure_one()
        return {
            'name': f'Đơn nghỉ phép - {self.nhan_vien_id.name} - {self.nam}',
            'type': 'ir.actions.act_window',
            'res_model': 'don_tu',
            'view_mode': 'tree,form',
            'domain': [
                ('nhan_vien_id', '=', self.nhan_vien_id.id),
                ('loai_don', '=', 'nghi_phep'),
                ('ngay_ap_dung', '>=', f'{self.nam}-01-01'),
                ('ngay_ap_dung', '<=', f'{self.nam}-12-31'),
            ],
            'context': {
                'default_nhan_vien_id': self.nhan_vien_id.id,
                'default_loai_don': 'nghi_phep',
            },
        }
    
    @api.model
    def tao_phep_nam_cho_tat_ca(self, nam=None):
        """Tạo bản ghi nghỉ phép năm cho tất cả nhân viên đang làm việc"""
        if not nam:
            nam = date.today().year
        
        nhan_vien_list = self.env['hr.employee'].search([
            ('trang_thai', '=', 'dang_lam')
        ])
        
        created = 0
        for nv in nhan_vien_list:
            existing = self.search([
                ('nhan_vien_id', '=', nv.id),
                ('nam', '=', nam)
            ], limit=1)
            
            if not existing:
                self.create({
                    'nhan_vien_id': nv.id,
                    'nam': nam,
                    'so_ngay_phep_nam': 12.0,
                })
                created += 1
        
        return created
    
    @api.constrains('so_ngay_phep_chuyen')
    def _check_phep_chuyen(self):
        for record in self:
            if record.so_ngay_phep_chuyen > 5:
                raise ValidationError("Số ngày phép chuyển từ năm trước không được quá 5 ngày!")
