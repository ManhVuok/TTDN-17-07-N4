import odoo
from odoo import api, SUPERUSER_ID
from odoo.tools.config import config as odoo_config
import os

# Load Odoo config
odoo_config.parse(['-c', 'odoo.conf'])

# Set up registry and cr
registry = odoo.registry('odoo_vn')
with registry.cursor() as cr:
    env = api.Environment(cr, SUPERUSER_ID, {})
    
    # Check Telegram Config
    configs = env['telegram.config'].search([])
    print(f"TOTAL CONFIGS: {len(configs)}")
    for conf in configs:
        print(f"- Name: {conf.ten}, Active: {conf.active}, Token: {conf.bot_token[:5]}..., ChatID: {conf.chat_id}")
        if conf.active:
            print(f"  Attempting test send for {conf.ten}...")
            result = conf.send_message('Test from Troubleshooting Script')
            print(f"  RESULT: {result}")
