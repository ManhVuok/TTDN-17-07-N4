from odoo import models, fields, api
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError, UserError

class DonTu(models.Model):
    _name = 'don_tu'
    _description = 'Đơn từ'
    _rec_name = 'ten_don'
    _order = 'ngay_lam_don desc, id desc'

    # ==================== THÔNG TIN CƠ BẢN ====================
    ten_don = fields.Char(
        "Tiêu đề đơn",
        compute="_compute_ten_don",
        store=True
    )
    
    nhan_vien_id = fields.Many2one(
        'hr.employee', 
        string="Nhân viên", 
        required=True,
        domain="[('trang_thai', '=', 'dang_lam')]"
    )
    
    # Thông tin từ nhân viên
    phong_ban_id = fields.Many2one(
        related='nhan_vien_id.department_id',
        string="Phòng ban",
        store=True,
        readonly=True
    )
    
    ngay_lam_don = fields.Date(
        "Ngày làm đơn", 
        required=True, 
        default=fields.Date.today,
        readonly=True
    )
    
    ngay_ap_dung = fields.Date(
        "Ngày áp dụng", 
        required=True
    )
    
    ngay_ket_thuc = fields.Date(
        "Ngày kết thúc",
        help="Để trống nếu chỉ xin 1 ngày"
    )
    
    # ==================== LOẠI ĐƠN ====================
    loai_don = fields.Selection([
        ('nghi', 'Đơn xin nghỉ'),
        ('nghi_phep', 'Đơn nghỉ phép năm'),
        ('nghi_khong_luong', 'Đơn nghỉ không lương'),
        ('di_muon', 'Đơn xin đi muộn'),
        ('ve_som', 'Đơn xin về sớm'),
        ('cong_tac', 'Đơn xin đi công tác'),
        ('lam_them', 'Đơn xin làm thêm giờ'),
    ], string="Loại đơn", required=True, default='nghi')
    
    # Thời gian xin đi muộn/về sớm (phút)
    thoi_gian_xin = fields.Float(
        "Thời gian xin (phút)",
        help="Áp dụng cho đơn đi muộn/về sớm"
    )
    
    # Lý do
    ly_do = fields.Text("Lý do")
    
    # ==================== TRẠNG THÁI ====================
    trang_thai_duyet = fields.Selection([
        ('nhap', 'Nháp'),
        ('cho_duyet', 'Chờ duyệt'),
        ('da_duyet', 'Đã duyệt'),
        ('tu_choi', 'Từ chối'),
        ('huy', 'Đã hủy'),
    ], string="Trạng thái", default='nhap', required=True)
    
    # ==================== THÔNG TIN PHÊ DUYỆT ====================
    nguoi_duyet_id = fields.Many2one(
        'res.users',
        string="Người duyệt",
        readonly=True
    )
    ngay_duyet = fields.Datetime(
        "Ngày duyệt",
        readonly=True
    )
    ly_do_tu_choi = fields.Text("Lý do từ chối", readonly=True)
    
    # ==================== GHI CHÚ ====================
    ghi_chu = fields.Text("Ghi chú")
    
    # ==================== COMPUTED ====================
    @api.depends('nhan_vien_id', 'loai_don', 'ngay_ap_dung')
    def _compute_ten_don(self):
        loai_don_dict = dict(self._fields['loai_don'].selection)
        for record in self:
            if record.nhan_vien_id and record.loai_don and record.ngay_ap_dung:
                loai = loai_don_dict.get(record.loai_don, '')
                record.ten_don = f"{loai} - {record.nhan_vien_id.name} - {record.ngay_ap_dung}"
            else:
                record.ten_don = "Đơn mới"
    
    # ==================== WORKFLOW ACTIONS ====================
    def _send_telegram_notification(self, title, detail):
        """Tính toán nội dung và gửi thông báo qua Telegram"""
        try:
            config = self.env['telegram.config'].sudo().get_active_config()
            if not config:
                return
            message = f"<b>{title}</b>\n"
            message += f"--------------------------------\n"
            message += f"👤 <b>Nhân viên:</b> {self.nhan_vien_id.name}\n"
            message += f"{detail}\n"
            message += f"--------------------------------\n"
            message += f"<i>Odoo HR & Chấm công</i>"
            config.send_message(message)
        except Exception:
            pass

    def action_gui_duyet(self):
        """Gửi đơn để duyệt"""
        for record in self:
            if record.trang_thai_duyet != 'nhap':
                raise UserError("Chỉ có thể gửi duyệt đơn ở trạng thái nháp!")
            record.trang_thai_duyet = 'cho_duyet'
            
            # Thông báo Telegram
            loai_don_dict = dict(self._fields['loai_don'].selection)
            loai = loai_don_dict.get(record.loai_don, '')
            detail = f"📝 <b>Loại đơn:</b> {loai}\n"
            detail += f"🗓 <b>Ngày áp dụng:</b> {record.ngay_ap_dung}\n"
            if record.ly_do:
                detail += f"💬 <b>Lý do:</b> {record.ly_do}"
            record._send_telegram_notification("🔔 CÓ YÊU CẦU ĐƠN TỪ MỚI CẦN DUYỆT", detail)
    
    def action_duyet(self):
        """Phê duyệt đơn"""
        for record in self:
            if record.trang_thai_duyet != 'cho_duyet':
                raise UserError("Chỉ có thể duyệt đơn đang chờ duyệt!")
            record.write({
                'trang_thai_duyet': 'da_duyet',
                'nguoi_duyet_id': self.env.user.id,
                'ngay_duyet': fields.Datetime.now(),
            })
            
            # Tự động cập nhật Bảng chấm công
            if record.loai_don in ['nghi', 'nghi_phep', 'nghi_khong_luong']:
                start_date = record.ngay_ap_dung
                end_date = record.ngay_ket_thuc or record.ngay_ap_dung
                current_date = start_date
                while current_date <= end_date:
                    bcc = self.env['bang_cham_cong'].search([
                        ('nhan_vien_id', '=', record.nhan_vien_id.id),
                        ('ngay_cham_cong', '=', current_date)
                    ], limit=1)
                    if bcc:
                        bcc.write({'don_tu_id': record.id})
                    else:
                        self.env['bang_cham_cong'].create({
                            'nhan_vien_id': record.nhan_vien_id.id,
                            'ngay_cham_cong': current_date,
                            'don_tu_id': record.id,
                        })
                    current_date += timedelta(days=1)
            
            # Thông báo Telegram
            loai_don_dict = dict(self._fields['loai_don'].selection)
            loai = loai_don_dict.get(record.loai_don, '')
            detail = f"📝 <b>Loại đơn:</b> {loai}\n🗓 <b>Ngày áp dụng:</b> {record.ngay_ap_dung}\n✅ <b>Trạng thái:</b> Đã được duyệt"
            record._send_telegram_notification("✅ ĐƠN TỪ ĐÃ ĐƯỢC PHÊ DUYỆT", detail)
    
    def action_tu_choi(self):
        """Từ chối đơn - mở wizard nhập lý do"""
        return {
            'name': 'Từ chối đơn',
            'type': 'ir.actions.act_window',
            'res_model': 'don_tu.tu_choi.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_don_tu_id': self.id},
        }
    
    def action_tu_choi_voi_ly_do(self, ly_do):
        """Từ chối đơn với lý do"""
        for record in self:
            if record.trang_thai_duyet != 'cho_duyet':
                raise UserError("Chỉ có thể từ chối đơn đang chờ duyệt!")
            record.write({
                'trang_thai_duyet': 'tu_choi',
                'nguoi_duyet_id': self.env.user.id,
                'ngay_duyet': fields.Datetime.now(),
                'ly_do_tu_choi': ly_do,
            })
            
            # Thông báo Telegram
            loai_don_dict = dict(self._fields['loai_don'].selection)
            loai = loai_don_dict.get(record.loai_don, '')
            detail = f"📝 <b>Loại đơn:</b> {loai}\n🗓 <b>Ngày áp dụng:</b> {record.ngay_ap_dung}\n❌ <b>Từ chối bởi:</b> {self.env.user.name}\n💬 <b>Lý do:</b> {ly_do}"
            record._send_telegram_notification("❌ ĐƠN TỪ ĐÃ BỊ TỪ CHỐI", detail)
    
    def action_huy(self):
        """Hủy đơn"""
        for record in self:
            if record.trang_thai_duyet in ['da_duyet']:
                raise UserError("Không thể hủy đơn đã được duyệt!")
            record.trang_thai_duyet = 'huy'
    
    def action_reset(self):
        """Đặt lại về nháp"""
        for record in self:
            if record.trang_thai_duyet == 'da_duyet':
                raise UserError("Không thể đặt lại đơn đã được duyệt!")
            record.write({
                'trang_thai_duyet': 'nhap',
                'nguoi_duyet_id': False,
                'ngay_duyet': False,
                'ly_do_tu_choi': False,
            })
    
    # ==================== CONSTRAINTS ====================
    @api.constrains('ngay_ap_dung', 'ngay_ket_thuc')
    def _check_ngay(self):
        for record in self:
            if record.ngay_ket_thuc and record.ngay_ap_dung:
                if record.ngay_ket_thuc < record.ngay_ap_dung:
                    raise ValidationError("Ngày kết thúc phải sau hoặc bằng ngày áp dụng!")
    
    @api.constrains('thoi_gian_xin')
    def _check_thoi_gian(self):
        for record in self:
            if record.loai_don in ['di_muon', 've_som']:
                if not record.thoi_gian_xin or record.thoi_gian_xin <= 0:
                    raise ValidationError("Vui lòng nhập thời gian xin (phút) cho đơn đi muộn/về sớm!")