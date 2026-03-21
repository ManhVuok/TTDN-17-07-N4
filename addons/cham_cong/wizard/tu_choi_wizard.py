# -*- coding: utf-8 -*-
from odoo import models, fields

class TuChoiWizard(models.TransientModel):
    _name = 'don_tu.tu_choi.wizard'
    _description = 'Wizard Nhập Lý Do Từ Chối'
    
    don_tu_id = fields.Many2one('don_tu', string="Đơn từ", required=True)
    ly_do_tu_choi = fields.Text("Lý do từ chối", required=True)
    
    def action_xac_nhan(self):
        self.ensure_one()
        self.don_tu_id.action_tu_choi_voi_ly_do(self.ly_do_tu_choi)
        return {'type': 'ir.actions.act_window_close'}
