from odoo import models, fields, api
import requests
import logging

_logger = logging.getLogger(__name__)

class TelegramConfig(models.Model):
    """Cấu hình Telegram Bot để gửi thông báo"""
    _name = 'telegram.config'
    _description = 'Cấu hình Telegram Bot'
    _rec_name = 'ten'

    ten = fields.Char("Tên cấu hình", required=True, default="Odoo HR Telegram Bot")
    bot_token = fields.Char("Bot Token", required=True, help="Token từ @BotFather")
    chat_id = fields.Char(
        "Chat ID", 
        required=True, 
        help="ID của channel hoặc group nhận thông báo. Ví dụ: -100xxxxxxxxxx"
    )
    active = fields.Boolean("Đang sử dụng", default=True)

    @api.model
    def get_active_config(self):
        """Lấy cấu hình đang active"""
        config = self.search([('active', '=', True)], limit=1)
        return config

    def send_message(self, message):
        """Gửi tin nhắn qua Telegram API"""
        if not self.bot_token or not self.chat_id:
            _logger.warning("Telegram Bot không được cấu hình đầy đủ. Bỏ qua gửi tin nhắn.")
            return False

        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        payload = {
            'chat_id': self.chat_id,
            'text': message,
            'parse_mode': 'HTML'
        }

        try:
            _logger.info(f"Đang gửi tin nhắn Telegram tới {self.chat_id}...")
            response = requests.post(url, json=payload, timeout=10)
            if response.status_code == 200:
                _logger.info("Đã gửi thông báo Telegram thành công.")
                return True
            else:
                _logger.error(f"Lỗi gửi Telegram: {response.status_code} - {response.text}")
                return False
        except Exception as e:
            _logger.error(f"Lỗi kết nối Telegram API: {str(e)}")
            return False
