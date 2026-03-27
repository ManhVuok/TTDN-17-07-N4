
import odoo
from odoo import api, SUPERUSER_ID

conf_file = 'odoo.conf'
db_name = 'ttdn_final2'

# Odoo environment setup
config = odoo.tools.config
config.parse_config(['-c', conf_file])
registry = odoo.registry(db_name)

with registry.cursor() as cr:
    env = api.Environment(cr, SUPERUSER_ID, {})
    
    # Target values
    target_key = "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"
    target_url = "https://openrouter.ai/api/v1/chat/completions"
    target_model = "google/gemini-2.0-flash-lite-preview-02-05:free"
    
    # Update existing or create new
    config_model = env['ai.cau_hinh_api']
    existing = config_model.search([('active', '=', True)], limit=1)
    
    if existing:
        existing.write({
            'api_key': target_key,
            'api_url': target_url,
            'model_name': target_model,
        })
        print(f"Updated existing AI config: {existing.ten}")
    else:
        new_config = config_model.create({
            'ten': 'OpenRouter Demo AI',
            'api_key': target_key,
            'api_url': target_url,
            'model_name': target_model,
            'active': True
        })
        print(f"Created new AI config: {new_config.ten}")
    
    cr.commit()
print("AI configuration updated successfully!")
