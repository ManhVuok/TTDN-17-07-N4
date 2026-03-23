from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from datetime import date
import calendar
import logging

_logger = logging.getLogger(__name__)


class BangLuong(models.Model):
    """
    Bảng lương theo tháng.
    Quản lý quy trình tính lương cho toàn bộ nhân viên trong tháng.
    """
    _name = 'bang_luong'
    _description = 'Bảng lương tháng'
    _rec_name = 'ten_bang_luong'
    _order = 'nam desc, thang desc'

    # Thông tin cơ bản
    ma_bang_luong = fields.Char("Mã bảng lương", required=True, copy=False)
    ten_bang_luong = fields.Char(
        "Tên bảng lương",
        compute="_compute_ten_bang_luong",
        store=True
    )
    
    # Kỳ lương
    thang = fields.Selection(
        [(str(i), f'Tháng {i}') for i in range(1, 13)],
        string="Tháng",
        required=True
    )
    nam = fields.Char("Năm", required=True, default=lambda self: str(date.today().year))
    
    # Thời gian tính lương
    ngay_bat_dau = fields.Date(
        "Từ ngày",
        compute="_compute_thoi_gian",
        store=True
    )
    ngay_ket_thuc = fields.Date(
        "Đến ngày",
        compute="_compute_thoi_gian",
        store=True
    )
    
    # Cấu hình lương áp dụng
    cau_hinh_luong_id = fields.Many2one(
        'cau_hinh_luong',
        string="Cấu hình lương",
        required=True,
        ondelete='cascade',
        default=lambda self: self.env['cau_hinh_luong'].search([('active', '=', True)], limit=1).id
    )
    
    # Chi tiết lương từng nhân viên
    chi_tiet_luong_ids = fields.One2many(
        'chi_tiet_luong',
        inverse_name='bang_luong_id',
        string="Chi tiết lương"
    )
    
    # Thống kê
    tong_nhan_vien = fields.Integer(
        "Tổng số nhân viên",
        compute="_compute_thong_ke",
        store=True
    )
    tong_luong_gross = fields.Float(
        "Tổng lương Gross",
        compute="_compute_thong_ke",
        store=True
    )
    tong_luong_net = fields.Float(
        "Tổng lương Net",
        compute="_compute_thong_ke",
        store=True
    )
    tong_bao_hiem = fields.Float(
        "Tổng BH người LĐ đóng",
        compute="_compute_thong_ke",
        store=True
    )
    
    # Trạng thái
    trang_thai = fields.Selection([
        ('nhap', 'Nháp'),
        ('da_tinh', 'Đã tính lương'),
        ('cho_duyet', 'Chờ duyệt'),
        ('da_duyet', 'Đã duyệt'),
        ('da_tra', 'Đã trả lương'),
        ('huy', 'Đã hủy'),
    ], string="Trạng thái", default='nhap', required=True)
    
    # Người phê duyệt
    nguoi_duyet_id = fields.Many2one('res.users', string="Người duyệt")
    ngay_duyet = fields.Datetime("Ngày duyệt")
    
    # Ghi chú
    ghi_chu = fields.Text("Ghi chú")
    
    @api.depends('thang', 'nam')
    def _compute_ten_bang_luong(self):
        for record in self:
            if record.thang and record.nam:
                record.ten_bang_luong = f"Bảng lương tháng {record.thang}/{record.nam}"
            else:
                record.ten_bang_luong = "Bảng lương mới"
    
    @api.depends('thang', 'nam')
    def _compute_thoi_gian(self):
        for record in self:
            if record.thang and record.nam:
                thang = int(record.thang)
                nam = int(record.nam)
                record.ngay_bat_dau = date(nam, thang, 1)
                record.ngay_ket_thuc = date(nam, thang, calendar.monthrange(nam, thang)[1])
            else:
                record.ngay_bat_dau = False
                record.ngay_ket_thuc = False
    
    @api.depends('chi_tiet_luong_ids', 'chi_tiet_luong_ids.luong_thuc_nhan',
                 'chi_tiet_luong_ids.tong_thu_nhap', 'chi_tiet_luong_ids.tong_bao_hiem')
    def _compute_thong_ke(self):
        for record in self:
            record.tong_nhan_vien = len(record.chi_tiet_luong_ids)
            record.tong_luong_gross = sum(record.chi_tiet_luong_ids.mapped('tong_thu_nhap'))
            record.tong_luong_net = sum(record.chi_tiet_luong_ids.mapped('luong_thuc_nhan'))
            record.tong_bao_hiem = sum(record.chi_tiet_luong_ids.mapped('tong_bao_hiem'))
    
    def action_tao_chi_tiet(self):
        """
        Tạo chi tiết lương cho tất cả nhân viên có hợp đồng hiệu lực
        """
        self.ensure_one()
        
        if self.trang_thai != 'nhap':
            raise UserError("Chỉ có thể tạo chi tiết khi bảng lương ở trạng thái Nháp!")
        
        # Xóa chi tiết cũ nếu có
        self.chi_tiet_luong_ids.unlink()
        
        # Lấy tất cả nhân viên có hợp đồng hiệu lực
        hop_dong_model = self.env['hop_dong_lao_dong']
        nhan_vien_model = self.env['hr.employee']
        
        # Lấy tất cả nhân viên
        all_nhan_vien = nhan_vien_model.search([])
        
        chi_tiet_vals = []
        for nhan_vien in all_nhan_vien:
            # Kiểm tra có hợp đồng hiệu lực không
            hop_dong = hop_dong_model.search([
                ('nhan_vien_id', '=', nhan_vien.id),
                ('trang_thai', '=', 'hieu_luc')
            ], limit=1, order='ngay_hieu_luc desc')
            
            if hop_dong:
                chi_tiet_vals.append({
                    'bang_luong_id': self.id,
                    'nhan_vien_id': nhan_vien.id,
                    'hop_dong_id': hop_dong.id,
                })
        
        if chi_tiet_vals:
            self.env['chi_tiet_luong'].create(chi_tiet_vals)
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Thành công',
                'message': f'Đã tạo chi tiết lương cho {len(chi_tiet_vals)} nhân viên',
                'type': 'success',
            }
        }
    
    def action_tinh_luong(self):
        """
        Tính lương cho tất cả nhân viên trong bảng lương
        """
        self.ensure_one()
        
        if self.trang_thai not in ['nhap', 'da_tinh']:
            raise UserError("Không thể tính lương ở trạng thái hiện tại!")
        
        if not self.chi_tiet_luong_ids:
            raise UserError("Chưa có chi tiết lương! Vui lòng tạo chi tiết trước.")
        
        # Tính lương cho từng nhân viên
        for chi_tiet in self.chi_tiet_luong_ids:
            chi_tiet.action_tinh_luong()
        
        self.trang_thai = 'da_tinh'
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Thành công',
                'message': 'Đã tính lương cho tất cả nhân viên!',
                'type': 'success',
            }
        }
    
    def action_gui_duyet(self):
        """Gửi duyệt bảng lương"""
        self.ensure_one()
        if self.trang_thai != 'da_tinh':
            raise UserError("Chỉ có thể gửi duyệt sau khi đã tính lương!")
        self.trang_thai = 'cho_duyet'
    
    def action_duyet(self):
        """Duyệt bảng lương"""
        self.ensure_one()
        if self.trang_thai != 'cho_duyet':
            raise UserError("Chỉ có thể duyệt khi ở trạng thái Chờ duyệt!")
        self.write({
            'trang_thai': 'da_duyet',
            'nguoi_duyet_id': self.env.user.id,
            'ngay_duyet': fields.Datetime.now(),
        })
        # Gửi thông báo Telegram
        self._send_telegram_notification()

    def _send_telegram_notification(self):
        """Tính toán nội dung và gửi thông báo qua Telegram"""
        self.ensure_one()
        config = self.env['telegram.config'].get_active_config()
        _logger.info(f"--- Bắt đầu gửi thông báo Telegram cho bảng lương {self.ma_bang_luong} ---")
        if not config:
            _logger.warning("Không tìm thấy cấu hình Telegram Bot nào đang hoạt động.")
            return
        
        _logger.info(f"Đang sử dụng cấu hình Telegram: {config.ten} (Chat ID: {config.chat_id})")

        message = f"<b>📢 THÔNG BÁO DUYỆT LƯƠNG</b>\n"
        message += f"--------------------------------\n"
        message += f"🗓 <b>Kỳ lương:</b> Tháng {self.thang}/{self.nam}\n"
        message += f"👤 <b>Số nhân viên:</b> {self.tong_nhan_vien}\n"
        message += f"💰 <b>Tổng lương Net:</b> {self.tong_luong_net:,.0f} VNĐ\n"
        message += f"✅ <b>Người duyệt:</b> {self.env.user.name}\n"
        message += f"--------------------------------\n"
        message += f"<i>Hệ thống Quản trị Odoo ERP</i>"

        _logger.info(f"Nội dung thông báo: {message}")
        config.send_message(message)
    
    def action_tra_luong(self):
        """Xác nhận đã trả lương"""
        self.ensure_one()
        if self.trang_thai != 'da_duyet':
            raise UserError("Chỉ có thể xác nhận trả lương sau khi đã duyệt!")
        self.trang_thai = 'da_tra'

    def action_ai_send_payslip(self):
        """Dùng AI để sinh nhận xét lương và gửi Email thực tế qua hệ thống Odoo"""
        self.ensure_one()
        if self.trang_thai not in ['da_duyet', 'da_tra']:
            raise UserError("Phải duyệt bảng lương trước khi gửi Payslip!")
            
        AIHelper = self.env['ai.assistant']
        count = 0
        
        for chi_tiet in self.chi_tiet_luong_ids:
            count += 1
            # Để demo nhanh (tránh load 30s), chỉ gọi AI thật cho 2 người đầu tiên. Những người sau dùng mẫu có sẵn.
            if count <= 2:
                prompt = f"Viết 1 nhận xét ngắn (3-4 câu) gửi cho {chi_tiet.nhan_vien_id.name}.\nLương tháng {self.thang}/{self.nam}.\nĐi làm: {chi_tiet.so_cong_thuc_te} ngày. Vắng mặt: {chi_tiet.so_ngay_vang} ngày. Đi muộn: {chi_tiet.tong_phut_di_muon} phút.\nYêu cầu: Nhận xét khách quan, nhẹ nhàng khuyên bảo nếu đi muộn, khen ngợi nếu chăm chỉ. Đóng vai: Chuyên gia nhân sự gửi theo dạng văn bản Email (bắt đầu bằng tên người nhận)."
                try:
                    ai_doc = AIHelper.create({'cau_hoi': prompt, 'loai_context': 'tong_hop'})
                    nhan_xet = ai_doc._call_ai_api(prompt, "Bạn là Trưởng phòng Nhân sự chuyên nghiệp.")
                except Exception as e:
                    nhan_xet = f"Không thể lấy đánh giá AI: {str(e)}"
            else:
                nhan_xet = f"Kính gửi {chi_tiet.nhan_vien_id.name},\n\nPhòng nhân sự gửi anh/chị thông tin lương tháng {self.thang}/{self.nam}. Trong tháng anh/chị có {chi_tiet.so_cong_thuc_te} ngày công. Cảm ơn sự đóng góp của anh/chị!\n\nTrân trọng,\nPhòng Nhân sự"

            chi_tiet.ai_nhan_xet = nhan_xet

            # 2. Tạo PDF phiếu lương bằng ReportLab (không cần wkhtmltopdf)
            try:
                import io
                import base64
                from reportlab.lib.pagesizes import A4
                from reportlab.lib import colors
                from reportlab.lib.units import mm
                from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
                from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
                from reportlab.pdfbase import pdfmetrics
                from reportlab.pdfbase.ttfonts import TTFont
                from reportlab.lib.enums import TA_CENTER, TA_LEFT

                buf = io.BytesIO()
                doc = SimpleDocTemplate(buf, pagesize=A4,
                                        rightMargin=15*mm, leftMargin=15*mm,
                                        topMargin=15*mm, bottomMargin=15*mm)

                # Đăng ký font Arial hỗ trợ tiếng Việt (Unicode)
                import os as _os
                font_paths = [
                    r'C:\Windows\Fonts\arial.ttf',
                    r'C:\Windows\Fonts\Arial.ttf',
                    '/usr/share/fonts/truetype/msttcorefonts/Arial.ttf',
                    '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf',
                ]
                font_bold_paths = [
                    r'C:\Windows\Fonts\arialbd.ttf',
                    r'C:\Windows\Fonts\ArialBD.ttf',
                    '/usr/share/fonts/truetype/msttcorefonts/Arial_Bold.ttf',
                    '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf',
                ]
                vn_font = 'Helvetica'
                vn_font_bold = 'Helvetica-Bold'
                for fp in font_paths:
                    if _os.path.exists(fp):
                        pdfmetrics.registerFont(TTFont('ArialVN', fp))
                        vn_font = 'ArialVN'
                        break
                for fp in font_bold_paths:
                    if _os.path.exists(fp):
                        pdfmetrics.registerFont(TTFont('ArialVN-Bold', fp))
                        vn_font_bold = 'ArialVN-Bold'
                        break

                styles = getSampleStyleSheet()
                title_style = ParagraphStyle('title', parent=styles['Heading1'],
                                             fontName=vn_font_bold,
                                             alignment=TA_CENTER, fontSize=16, spaceAfter=6)
                subtitle_style = ParagraphStyle('subtitle', parent=styles['Normal'],
                                                fontName=vn_font,
                                                alignment=TA_CENTER, fontSize=12, spaceAfter=12)
                normal = ParagraphStyle('normal_vn', parent=styles['Normal'],
                                        fontName=vn_font, fontSize=10)

                nv = chi_tiet.nhan_vien_id
                content = []

                # Tiêu đề
                content.append(Paragraph("PHIẾU LƯƠNG", title_style))
                content.append(Paragraph(f"Kỳ lương: Tháng {self.thang}/{self.nam}", subtitle_style))
                content.append(Spacer(1, 6*mm))

                # Thông tin nhân viên
                emp_data = [
                    ['Mã nhân viên:', nv.ma_dinh_danh or '', 'Họ và tên:', nv.name or ''],
                    ['Phòng ban:', chi_tiet.phong_ban_id.ten_phong_ban if chi_tiet.phong_ban_id else '', 'Chức vụ:', chi_tiet.chuc_vu_id.ten_chuc_vu if chi_tiet.chuc_vu_id else ''],
                    ['Số ngày công CĐ:', str(chi_tiet.so_cong_chuan), 'Ngày công TT:', str(chi_tiet.so_cong_thuc_te)],
                ]
                emp_table = Table(emp_data, colWidths=[40*mm, 50*mm, 40*mm, 50*mm])
                emp_table.setStyle(TableStyle([
                    ('BACKGROUND', (0,0), (-1,-1), colors.whitesmoke),
                    ('FONTSIZE', (0,0), (-1,-1), 10),
                    ('FONTNAME', (0,0), (-1,-1), vn_font),
                    ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
                    ('FONTNAME', (0,0), (0,-1), vn_font_bold),
                    ('FONTNAME', (2,0), (2,-1), vn_font_bold),
                    ('PADDING', (0,0), (-1,-1), 4),
                ]))
                content.append(emp_table)
                content.append(Spacer(1, 6*mm))

                # Chi tiết lương
                luong_data = [
                    ['Khoản mục', 'Số tiền (VNĐ)'],
                    ['Lương cơ bản', f"{chi_tiet.luong_co_ban:,.0f}"],
                    ['Lương theo công', f"{chi_tiet.luong_theo_cong:,.0f}"],
                    ['Tổng phụ cấp', f"{chi_tiet.tong_phu_cap:,.0f}"],
                    ['TỔNG THU NHẬP (GROSS)', f"{chi_tiet.tong_thu_nhap:,.0f}"],
                    ['BHXH (8%)', f"- {chi_tiet.tien_bhxh:,.0f}"],
                    ['BHYT (1.5%)', f"- {chi_tiet.tien_bhyt:,.0f}"],
                    ['BHTN (1%)', f"- {chi_tiet.tien_bhtn:,.0f}"],
                    ['Phạt đi muộn/về sớm', f"- {(chi_tiet.tien_phat_di_muon + chi_tiet.tien_phat_ve_som):,.0f}"],
                    ['Thuế TNCN', f"- {chi_tiet.thue_tncn:,.0f}"],
                    ['LƯƠNG THỰC NHẬN (NET)', f"{chi_tiet.luong_thuc_nhan:,.0f}"],
                ]
                luong_table = Table(luong_data, colWidths=[120*mm, 60*mm])
                luong_table.setStyle(TableStyle([
                    ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#0066cc')),
                    ('TEXTCOLOR', (0,0), (-1,0), colors.white),
                    ('FONTNAME', (0,0), (-1,-1), vn_font),
                    ('FONTNAME', (0,0), (-1,0), vn_font_bold),
                    ('ALIGN', (1,0), (1,-1), 'RIGHT'),
                    ('FONTSIZE', (0,0), (-1,-1), 10),
                    ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
                    ('BACKGROUND', (0,4), (-1,4), colors.HexColor('#d4edda')),
                    ('FONTNAME', (0,4), (-1,4), vn_font_bold),
                    ('BACKGROUND', (0,-1), (-1,-1), colors.HexColor('#0066cc')),
                    ('TEXTCOLOR', (0,-1), (-1,-1), colors.white),
                    ('FONTNAME', (0,-1), (-1,-1), vn_font_bold),
                    ('FONTSIZE', (0,-1), (-1,-1), 12),
                    ('PADDING', (0,0), (-1,-1), 5),
                ]))
                content.append(luong_table)
                content.append(Spacer(1, 8*mm))

                # Nhận xét
                if chi_tiet.ai_nhan_xet:
                    content.append(Paragraph("<b>Nhận xét từ phòng nhân sự:</b>", normal))
                    for line in chi_tiet.ai_nhan_xet.split('\n')[:8]:  # max 8 dòng
                        content.append(Paragraph(line or '&nbsp;', normal))

                doc.build(content)
                pdf_content = buf.getvalue()
                pdf_filename = f'PhieuLuong_{nv.name}_{self.thang}_{self.nam}.pdf'
            except Exception as e:
                pdf_content = None
                pdf_filename = None

            # 3. Lệnh tạo Email và đính kèm PDF
            nhan_vien = chi_tiet.nhan_vien_id
            email_target = getattr(nhan_vien, 'email_cong_ty', False) or getattr(nhan_vien, 'email', False) or 'thuyet1230@gmail.com'

            mail_values = {
                'subject': f'Phiếu lương và Nhận xét tháng {self.thang}/{self.nam}',
                'body_html': f'<pre>{chi_tiet.ai_nhan_xet}</pre>',
                'email_to': email_target,
            }

            if pdf_content and pdf_filename:
                import base64
                mail_values['attachment_ids'] = [(0, 0, {
                    'name': pdf_filename,
                    'datas': base64.b64encode(pdf_content),
                    'mimetype': 'application/pdf',
                })]

            mail = self.env['mail.mail'].sudo().create(mail_values)
            mail.send()
        
        self.trang_thai = 'da_tra'
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Gửi Email thành công!',
                'message': f'Đã sinh {len(self.chi_tiet_luong_ids)} nhận xét và GỬI TRỰC TIẾP tới email nhân viên.',
                'type': 'success',
            }
        }
    
    def action_huy(self):
        """Hủy bảng lương"""
        self.ensure_one()
        if self.trang_thai == 'da_tra':
            raise UserError("Không thể hủy bảng lương đã trả!")
        self.trang_thai = 'huy'
    
    def action_reset(self):
        """Đặt lại về trạng thái nháp"""
        self.ensure_one()
        if self.trang_thai == 'da_tra':
            raise UserError("Không thể reset bảng lương đã trả!")
        self.trang_thai = 'nhap'

    @api.model
    def _cron_generate_monthly_payroll(self):
        """
        Phương thức cho Scheduled Action: Tự động tạo bảng lương nháp vào ngày đầu tháng.
        """
        today = date.today()
        thang = str(today.month)
        nam = str(today.year)
        
        # Kiểm tra xem đã có bảng lương cho tháng này chưa
        existing = self.search([('thang', '=', thang), ('nam', '=', nam)], limit=1)
        if existing:
            _logger.info(f"Bảng lương tháng {thang}/{nam} đã tồn tại, bỏ qua tự động tạo.")
            return
            
        # Tạo bảng lương mới
        ma_bang_luong = f"BL{nam}{thang.zfill(2)}"
        vals = {
            'ma_bang_luong': ma_bang_luong,
            'thang': thang,
            'nam': nam,
            'trang_thai': 'nhap',
            'ghi_chu': f"Bảng lương được tạo tự động bởi hệ thống vào ngày {today.strftime('%d/%m/%Y')}"
        }
        
        try:
            new_payroll = self.create(vals)
            # Tự động tạo chi tiết nhân viên
            new_payroll.action_tao_chi_tiet()
            _logger.info(f"Đã tự động tạo bảng lương: {ma_bang_luong}")
        except Exception as e:
            _logger.error(f"Lỗi khi tự động tạo bảng lương: {str(e)}")
    
    _sql_constraints = [
        ('ma_bang_luong_unique', 'UNIQUE(ma_bang_luong)', 'Mã bảng lương phải là duy nhất!'),
        ('thang_nam_unique', 'UNIQUE(thang, nam)', 'Đã tồn tại bảng lương cho tháng này!')
    ]
