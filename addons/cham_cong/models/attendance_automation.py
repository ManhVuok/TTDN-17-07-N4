# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import date
import logging

_logger = logging.getLogger(__name__)


class AttendanceAutomation(models.Model):
    _name = 'attendance.automation'
    _description = 'Tự động hóa chấm công'

    @api.model
    def _cron_daily_attendance_summary(self):
        """
        Gửi báo cáo tóm tắt chấm công hàng ngày qua Telegram (Mức 2 & 3)
        """
        today = date.today()
        config = self.env['telegram.config'].get_active_config()
        if not config:
            _logger.warning("Telegram Bot chưa được cấu hình. Bỏ qua gửi báo cáo ngày.")
            return

        # Lấy dữ liệu chấm công hôm nay
        attendances = self.env['bang_cham_cong'].search([
            ('ngay_cham_cong', '=', today)
        ])

        total = len(attendances)
        latecomers = attendances.filtered(lambda x: x.phut_di_muon > 0)
        absentees = attendances.filtered(lambda x: x.trang_thai == 'vang_mat')
        on_time = attendances.filtered(lambda x: x.trang_thai == 'di_lam' and x.phut_di_muon == 0)

        message = f"<b>📊 BÁO CÁO CHẤM CÔNG NGÀY {today.strftime('%d/%m/%Y')}</b>\n"
        message += f"--------------------------------\n"
        message += f"👥 <b>Tổng số nhân viên:</b> {total}\n"
        message += f"✅ <b>Đúng giờ:</b> {len(on_time)}\n"
        message += f"⌛ <b>Đi muộn:</b> {len(latecomers)}\n"
        message += f"❌ <b>Vắng mặt:</b> {len(absentees)}\n"
        
        if latecomers:
            message += f"--------------------------------\n"
            message += f"<b>Danh sách đi muộn:</b>\n"
            for lc in latecomers[:10]: # Giới hạn 10 người đầu tiên
                message += f"- {lc.nhan_vien_id.ho_va_ten} ({lc.phut_di_muon} phút)\n"
            if len(latecomers) > 10:
                message += f"... và {len(latecomers)-10} người khác.\n"

        message += f"--------------------------------\n"
        message += f"<i>Hệ thống Quản trị Odoo ERP</i>"

        config.send_message(message)
        _logger.info(f"Đã gửi báo cáo chấm công ngày {today}")
