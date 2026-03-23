# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date


class HrFamily(models.Model):
    """Quản lý thân nhân của nhân viên - Mức 1 Giai đoạn 2 (Gợi ý 1)"""
    _name = 'hr.family'
    _description = 'Thân nhân nhân viên'
    _order = 'employee_id, birth_date'

    employee_id = fields.Many2one(
        'hr.employee',
        string="Nhân viên",
        required=True,
        ondelete='cascade'
    )

    name = fields.Char("Họ và tên", required=True)

    relationship = fields.Selection([
        ('vo', 'Vợ'),
        ('chong', 'Chồng'),
        ('con', 'Con'),
        ('cha', 'Cha'),
        ('me', 'Mẹ'),
        ('anh', 'Anh/Em trai'),
        ('chi', 'Chị/Em gái'),
        ('khac', 'Khác'),
    ], string="Quan hệ", required=True)

    birth_date = fields.Date("Ngày sinh")

    age = fields.Integer(
        "Tuổi",
        compute="_compute_age",
        store=True
    )

    is_dependent = fields.Boolean(
        "Người phụ thuộc",
        default=False,
        help="Tích nếu người này được giảm trừ gia cảnh (con < 18 tuổi, cha/mẹ không có thu nhập...)"
    )

    ghi_chu = fields.Char("Ghi chú")

    # ==================== COMPUTE ====================
    @api.depends('birth_date')
    def _compute_age(self):
        today = date.today()
        for rec in self:
            if rec.birth_date:
                rec.age = today.year - rec.birth_date.year - (
                    (today.month, today.day) < (rec.birth_date.month, rec.birth_date.day)
                )
                # Tự động tick is_dependent nếu là con < 18 tuổi
                if rec.relationship == 'con' and rec.age < 18:
                    rec.is_dependent = True
            else:
                rec.age = 0

    # ==================== CONSTRAINTS ====================
    @api.constrains('birth_date')
    def _check_birth_date(self):
        for rec in self:
            if rec.birth_date and rec.birth_date > fields.Date.today():
                raise ValidationError("Ngày sinh của thân nhân không được lớn hơn ngày hiện tại!")
