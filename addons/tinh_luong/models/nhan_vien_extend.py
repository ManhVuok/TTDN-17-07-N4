# -*- coding: utf-8 -*-
from odoo import models, fields, api


class NhanVienTinhLuong(models.Model):
    """
    Mở rộng model nhan_vien để thêm thông tin liên kết với module tính lương
    """
    _inherit = 'nhan_vien'
    
    # Liên kết với hợp đồng lao động
    hop_dong_ids = fields.One2many(
        'hop_dong_lao_dong',
        inverse_name='nhan_vien_id',
        string="Danh sách hợp đồng"
    )
    
    hop_dong_hieu_luc_id = fields.Many2one(
        'hop_dong_lao_dong',
        string="Hợp đồng hiệu lực",
        compute="_compute_hop_dong_hieu_luc",
        store=False
    )
    
    luong_hien_tai = fields.Float(
        "Lương hiện tại",
        compute="_compute_hop_dong_hieu_luc",
        store=False
    )
    
    so_hop_dong = fields.Integer(
        "Số hợp đồng",
        compute="_compute_so_hop_dong"
    )
    
    @api.depends('hop_dong_ids')
    def _compute_hop_dong_hieu_luc(self):
        for record in self:
            hop_dong = self.env['hop_dong_lao_dong'].search([
                ('nhan_vien_id', '=', record.id),
                ('trang_thai', '=', 'hieu_luc')
            ], limit=1, order='ngay_hieu_luc desc')
            
            record.hop_dong_hieu_luc_id = hop_dong.id if hop_dong else False
            record.luong_hien_tai = hop_dong.luong_co_ban if hop_dong else 0
    
    @api.depends('hop_dong_ids')
    def _compute_so_hop_dong(self):
        for record in self:
            record.so_hop_dong = len(record.hop_dong_ids)
    
    def action_xem_hop_dong(self):
        """
        Mở danh sách hợp đồng của nhân viên
        """
        self.ensure_one()
        return {
            'name': f'Hợp đồng - {self.ho_va_ten}',
            'type': 'ir.actions.act_window',
            'res_model': 'hop_dong_lao_dong',
            'view_mode': 'tree,form',
            'domain': [('nhan_vien_id', '=', self.id)],
            'context': {
                'default_nhan_vien_id': self.id,
            }
        }
    
    def action_tao_hop_dong(self):
        """
        Tạo hợp đồng mới cho nhân viên
        """
        self.ensure_one()
        return {
            'name': 'Tạo hợp đồng mới',
            'type': 'ir.actions.act_window',
            'res_model': 'hop_dong_lao_dong',
            'view_mode': 'form',
            'context': {
                'default_nhan_vien_id': self.id,
            },
            'target': 'current',
        }
