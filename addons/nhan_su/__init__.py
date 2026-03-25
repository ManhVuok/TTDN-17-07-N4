# -*- coding: utf-8 -*-

from . import controllers
from . import models


def _post_init_hook(cr, registry):
    """Cài đặt ngôn ngữ Tiếng Việt khi cài module."""
    from odoo import api, SUPERUSER_ID
    env = api.Environment(cr, SUPERUSER_ID, {})
    # Kích hoạt ngôn ngữ Tiếng Việt
    lang_vn = env['res.lang'].search([('code', '=', 'vi_VN'), ('active', '=', False)])
    if lang_vn:
        lang_vn.write({'active': True})
    elif not env['res.lang'].search([('code', '=', 'vi_VN')]):
        # Nếu chưa có ngôn ngữ, cài từ wizard
        wizard = env['base.language.install'].create({'lang': 'vi_VN', 'overwrite': True})
        wizard.lang_install()
    # Đặt ngôn ngữ cho tất cả user
    env['res.users'].search([]).write({'lang': 'vi_VN'})