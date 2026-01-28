from odoo import models, fields, api

class PhongBan(models.Model):
    _name = 'phong_ban'
    _description = 'Bảng chứa thông tin phòng ban'
    _rec_name = 'ten_phong_ban'
    _order = 'ten_phong_ban'

    ma_phong_ban = fields.Char("Mã phòng ban", required=True, copy=False)
    ten_phong_ban = fields.Char("Tên phòng ban", required=True)
    mo_ta = fields.Text("Mô tả")
    
    # Quản lý phòng ban cha - con
    parent_id = fields.Many2one(
        'phong_ban', 
        string="Phòng ban cha",
        ondelete='restrict'
    )
    child_ids = fields.One2many(
        'phong_ban',
        'parent_id',
        string="Phòng ban con"
    )
    
    # Trưởng phòng
    truong_phong_id = fields.Many2one(
        'nhan_vien',
        string="Trưởng phòng",
        domain="[('phong_ban_id', '=', id), ('trang_thai', '=', 'dang_lam')]"
    )
    
    # Danh sách nhân viên trong phòng
    nhan_vien_ids = fields.One2many(
        'nhan_vien',
        'phong_ban_id',
        string="Danh sách nhân viên"
    )
    
    # Số nhân viên - computed field
    so_nhan_vien = fields.Integer(
        "Số nhân viên",
        compute="_compute_so_nhan_vien",
        store=True
    )
    
    so_nhan_vien_dang_lam = fields.Integer(
        "NV đang làm việc",
        compute="_compute_so_nhan_vien",
        store=True
    )
    
    # Trạng thái hoạt động
    active = fields.Boolean("Hoạt động", default=True)
    
    # SQL Constraints
    _sql_constraints = [
        ('ma_phong_ban_unique', 'UNIQUE(ma_phong_ban)', 'Mã phòng ban phải là duy nhất!'),
    ]
    
    @api.depends('nhan_vien_ids', 'nhan_vien_ids.trang_thai')
    def _compute_so_nhan_vien(self):
        for record in self:
            nhan_vien = record.nhan_vien_ids
            record.so_nhan_vien = len(nhan_vien)
            record.so_nhan_vien_dang_lam = len(nhan_vien.filtered(
                lambda nv: nv.trang_thai == 'dang_lam'
            ))