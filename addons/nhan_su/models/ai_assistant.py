# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError
import requests
import json
import logging

_logger = logging.getLogger(__name__)


class AICauHinhAPI(models.Model):
    """Cấu hình API key cho AI Assistant"""
    _name = 'ai.cau_hinh_api'
    _description = 'Cấu hình API AI'
    _rec_name = 'ten'
    
    ten = fields.Char("Tên cấu hình", required=True, default="OpenRouter API")
    api_key = fields.Char("API Key", required=True)
    api_url = fields.Char(
        "API URL", 
        required=False, 
        default="https://openrouter.ai/api/v1/chat/completions"
    )
    model_name = fields.Char(
        "Model Name", 
        required=True, 
        default="gemini-1.5-flash"
    )
    active = fields.Boolean("Đang sử dụng", default=True)
    
    @api.model
    def get_active_config(self):
        """Lấy cấu hình đang active"""
        config = self.search([('active', '=', True)], limit=1)
        if not config:
            raise UserError("Chưa có cấu hình API AI. Vui lòng vào Cài đặt > AI Assistant để cấu hình.")
        return config


class AILichSuChat(models.Model):
    """Lưu lịch sử chat với AI"""
    _name = 'ai.lich_su_chat'
    _description = 'Lịch sử chat AI'
    _order = 'create_date desc'
    _rec_name = 'cau_hoi'
    
    user_id = fields.Many2one('res.users', string="Người dùng", default=lambda self: self.env.user)
    cau_hoi = fields.Text("Câu hỏi", required=True)
    tra_loi = fields.Text("Trả lời AI")
    context_data = fields.Text("Context Data", help="Dữ liệu context gửi cho AI")
    thoi_gian = fields.Datetime("Thời gian", default=fields.Datetime.now)
    thanh_cong = fields.Boolean("Thành công", default=True)
    loi = fields.Text("Lỗi nếu có")


class AIAssistant(models.TransientModel):
    """AI Assistant - Trợ lý thông minh cho dữ liệu nhân sự"""
    _name = 'ai.assistant'
    _description = 'AI Assistant'
    
    cau_hoi = fields.Text("Câu hỏi của bạn", required=True)
    tra_loi = fields.Html("Trả lời từ AI", readonly=True)
    loai_context = fields.Selection([
        ('nhan_vien', 'Thông tin nhân viên'),
        ('phong_ban', 'Thống kê phòng ban'),
        ('cham_cong', 'Dữ liệu chấm công'),
        ('luong', 'Thông tin lương'),
        ('noi_quy', 'Tra cứu nội quy công ty'),
        ('tong_hop', 'Tổng hợp tất cả'),
    ], string="Loại dữ liệu", default='tong_hop', required=True)
    
    # ==================== LẤY DỮ LIỆU CONTEXT ====================
    def _get_noi_quy_context(self):
        """Lấy thông tin nội quy công ty (Mức 3 - Trợ lý thông minh)"""
        return """
=== NỘI QUY CÔNG TY (TÓM TẮT) ===
1. Giờ làm việc: 
   - Sáng: 08:00 - 12:00
   - Chiều: 13:30 - 17:30
   - Làm việc từ Thứ 2 đến Thứ 6. Thứ 7 làm việc buổi sáng.
2. Quy định đi muộn/về sớm:
   - Đi muộn trên 15 phút mà không có đơn xin phép sẽ bị tính là đi muộn.
   - Đi muộn quá 3 lần/tháng sẽ bị nhắc nhở văn bản.
3. Chế độ nghỉ phép:
   - Mỗi năm có 12 ngày phép hưởng nguyên lương.
   - Nghỉ thai sản: Theo quy định nhà nước (6 tháng).
4. Quy định trang phục:
   - Lịch sự, gọn gàng. Thứ 2 và Thứ 6 mặc đồng phục công ty.
5. Khen thưởng/Kỷ luật:
   - Thưởng chuyên cần: 500.000 VNĐ nếu không đi muộn buổi nào trong tháng.
"""

    def _get_nhan_vien_context(self):
        """Lấy thông tin tổng hợp về nhân viên"""
        NhanVien = self.env['hr.employee']
        
        tong_nv = NhanVien.search_count([])
        nv_dang_lam = NhanVien.search_count([('trang_thai', '=', 'dang_lam')])
        nv_thu_viec = NhanVien.search_count([('trang_thai', '=', 'thu_viec')])
        nv_nghi_viec = NhanVien.search_count([('trang_thai', '=', 'nghi_viec')])
        nv_nam = NhanVien.search_count([('gender', '=', 'male')])
        nv_nu = NhanVien.search_count([('gender', '=', 'female')])
        
        # Tuổi trung bình
        nv_list = NhanVien.search([('trang_thai', '=', 'dang_lam')])
        tuoi_tb = sum(nv.tuoi for nv in nv_list) / len(nv_list) if nv_list else 0
        
        # Danh sách nhân viên
        ds_nhan_vien = []
        for nv in NhanVien.search([('trang_thai', '=', 'dang_lam')], limit=15):
            gender_map = {'male': 'Nam', 'female': 'Nữ', 'other': 'Khác'}
            ds_nhan_vien.append({
                'ma': nv.ma_dinh_danh,
                'ho_ten': nv.name,
                'phong_ban': nv.department_id.name if nv.department_id else 'Chưa phân bổ',
                'chuc_vu': nv.job_id.name if nv.job_id else 'Chưa có',
                'tuoi': nv.tuoi,
                'gioi_tinh': gender_map.get(nv.gender, nv.gender or 'Chưa có'),
                'email': nv.work_email,
                'sdt': nv.work_phone,
            })
        
        return f"""
=== THÔNG TIN NHÂN VIÊN ===
- Tổng số nhân viên: {tong_nv}
- Đang làm việc: {nv_dang_lam}
- Đang thử việc: {nv_thu_viec}
- Đã nghỉ việc: {nv_nghi_viec}
- Nam: {nv_nam}, Nữ: {nv_nu}
- Tuổi trung bình: {tuoi_tb:.1f}

=== DANH SÁCH NHÂN VIÊN ĐANG LÀM VIỆC ===
{json.dumps(ds_nhan_vien, ensure_ascii=False, indent=2)}
"""
    
    def _get_phong_ban_context(self):
        """Lấy thông tin phòng ban"""
        PhongBan = self.env['phong_ban']
        
        ds_phong_ban = []
        for pb in PhongBan.search([('active', '=', True)]):
            ds_phong_ban.append({
                'ma': pb.ma_phong_ban,
                'ten': pb.ten_phong_ban,
                'so_nhan_vien': pb.so_nhan_vien,
                'so_nv_dang_lam': pb.so_nhan_vien_dang_lam,
                'truong_phong': pb.truong_phong_id.name if pb.truong_phong_id else 'Chưa có',
            })
        
        return f"""
=== THỐNG KÊ PHÒNG BAN ===
Tổng số phòng ban: {len(ds_phong_ban)}

{json.dumps(ds_phong_ban, ensure_ascii=False, indent=2)}
"""
    
    def _get_cham_cong_context(self):
        """Lấy thống kê chấm công"""
        BangChamCong = self.env['bang_cham_cong']
        from datetime import date, timedelta
        
        today = date.today()
        thang_nay = today.replace(day=1)
        
        # Chấm công trong tháng
        cc_thang = BangChamCong.search([
            ('ngay_cham_cong', '>=', thang_nay),
            ('ngay_cham_cong', '<=', today),
        ])
        
        tong_cong = len(cc_thang)
        di_lam = len(cc_thang.filtered(lambda x: x.trang_thai == 'di_lam'))
        di_muon = len(cc_thang.filtered(lambda x: x.trang_thai in ['di_muon', 'di_muon_ve_som']))
        ve_som = len(cc_thang.filtered(lambda x: x.trang_thai in ['ve_som', 'di_muon_ve_som']))
        vang_mat = len(cc_thang.filtered(lambda x: x.trang_thai == 'vang_mat'))
        
        # Top nhân viên đi muộn
        top_di_muon = {}
        for cc in cc_thang.filtered(lambda x: x.phut_di_muon > 0):
            nv = cc.nhan_vien_id.name
            if nv not in top_di_muon:
                top_di_muon[nv] = 0
            top_di_muon[nv] += cc.phut_di_muon
        
        top_di_muon_list = sorted(top_di_muon.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return f"""
=== THỐNG KÊ CHẤM CÔNG THÁNG {today.month}/{today.year} ===
- Tổng số bản ghi: {tong_cong}
- Đi làm đúng giờ: {di_lam}
- Đi muộn: {di_muon}
- Về sớm: {ve_som}
- Vắng mặt: {vang_mat}

=== TOP 5 NHÂN VIÊN ĐI MUỘN NHIỀU NHẤT ===
{json.dumps(top_di_muon_list, ensure_ascii=False, indent=2)}
"""
    
    def _get_luong_context(self):
        """Lấy thông tin lương"""
        try:
            BangLuong = self.env['bang_luong']
            ChiTietLuong = self.env['chi_tiet_luong']
            
            # Bảng lương gần nhất
            bang_luong = BangLuong.search([], order='nam desc, thang desc', limit=1)
            
            if not bang_luong:
                return "Chưa có dữ liệu bảng lương."
            
            chi_tiet = ChiTietLuong.search([('bang_luong_id', '=', bang_luong.id)])
            
            tong_luong = sum(ct.luong_thuc_nhan for ct in chi_tiet)
            tong_thu_nhap = sum(ct.tong_thu_nhap for ct in chi_tiet)
            tong_bao_hiem = sum(ct.tong_bao_hiem for ct in chi_tiet)
            tong_thue = sum(ct.thue_tncn for ct in chi_tiet)
            
            # Thống kê theo phòng ban
            luong_theo_pb = {}
            for ct in chi_tiet:
                pb = ct.phong_ban_id.ten_phong_ban if ct.phong_ban_id else 'Chưa phân bổ'
                if pb not in luong_theo_pb:
                    luong_theo_pb[pb] = {'so_nv': 0, 'tong_luong': 0}
                luong_theo_pb[pb]['so_nv'] += 1
                luong_theo_pb[pb]['tong_luong'] += ct.luong_thuc_nhan
            
            return f"""
=== BẢNG LƯƠNG THÁNG {bang_luong.thang}/{bang_luong.nam} ===
- Trạng thái: {bang_luong.trang_thai}
- Số nhân viên: {len(chi_tiet)}
- Tổng thu nhập (Gross): {tong_thu_nhap:,.0f} VNĐ
- Tổng bảo hiểm: {tong_bao_hiem:,.0f} VNĐ
- Tổng thuế TNCN: {tong_thue:,.0f} VNĐ
- Tổng lương thực nhận (Net): {tong_luong:,.0f} VNĐ

=== THỐNG KÊ THEO PHÒNG BAN ===
{json.dumps(luong_theo_pb, ensure_ascii=False, indent=2)}
"""
        except Exception as e:
            return f"Không thể lấy dữ liệu lương: {str(e)}"
    
    def _get_all_context(self):
        """Lấy tất cả context"""
        return (
            self._get_nhan_vien_context() + "\n\n" +
            self._get_phong_ban_context() + "\n\n" +
            self._get_cham_cong_context() + "\n\n" +
            self._get_luong_context() + "\n\n" +
            self._get_noi_quy_context()
        )
    
    def _get_context_by_type(self):
        """Lấy context theo loại được chọn"""
        if self.loai_context == 'nhan_vien':
            return self._get_nhan_vien_context()
        elif self.loai_context == 'phong_ban':
            return self._get_phong_ban_context()
        elif self.loai_context == 'cham_cong':
            return self._get_cham_cong_context()
        elif self.loai_context == 'luong':
            return self._get_luong_context()
        elif self.loai_context == 'noi_quy':
            return self._get_noi_quy_context()
        else:
            return self._get_all_context()
    
    # ==================== GỌI API AI ====================
    def _call_ai_api(self, cau_hoi, context_data):
        """Gọi API OpenRouter"""
        config = self.env['ai.cau_hinh_api'].get_active_config()
        
        system_prompt = f"""Bạn là trợ lý AI thông minh cho hệ thống quản lý nhân sự. 
Nhiệm vụ của bạn là trả lời các câu hỏi dựa trên dữ liệu được cung cấp.

=== DỮ LIỆU HỆ THỐNG ===
{context_data}

=== HƯỚNG DẪN ===
1. Trả lời dựa trên dữ liệu thực tế được cung cấp ở trên
2. Nếu không có thông tin trong dữ liệu, hãy nói rõ là không có thông tin
3. Trả lời CỰC KỲ ngắn gọn, đi thẳng vào vấn đề. Ưu tiên tóm tắt.
4. Sử dụng tiếng Việt chuẩn, chuyên nghiệp.
5. Nếu dữ liệu được cung cấp bị giới hạn (tóm tắt), hãy trả lời dựa trên thông tin sẵn có tốt nhất.
6. ĐẶC BIỆT: Hãy đóng vai trò là một cố vấn nhân sự cấp cao, đưa ra các nhận xét và giải pháp cải thiện.
7. Format bằng Markdown đẹp, dễ đọc, ưu tiên dùng bảng nếu có số liệu.
"""
        
        api_key = (config.api_key or "").strip()
        if not api_key:
            raise UserError("API Key đang trống. Vui lòng kiểm tra lại cấu hình AI.")
            
        # Xác định xem đang dùng OpenRouter hay Gemini Native
        api_url = (config.api_url or "").strip()
        model_name = (config.model_name or "gemini-1.5-flash").strip()
        
        # TỰ ĐỘNG NHẬN DIỆN: Nếu Key bắt đầu bằng AIzaSy thì coi như dùng Gemini Native
        is_gemini_native = api_key.startswith("AIzaSy") or "googleapis.com" in api_url or not api_url
        
        if is_gemini_native:
            # Danh sách các model để thử theo thứ tự ưu tiên
            # Models được xác nhận hoạt động với Gemini v1beta API
            VALID_MODELS = [
                "gemini-2.0-flash",       # Mới, hiệu năng cao
                "gemini-1.5-flash",       # Ổn định, nhanh
                "gemini-1.5-flash-8b",    # Rất nhẹ, ít tốn quota
                "gemini-2.0-flash-lite",  # Bản lite của 2.0
                "gemini-1.5-pro",         # Mạnh mẽ nhất
                "gemini-2.0-pro-exp-02-05", # Bản Pro thực nghiệm
                "gemini-1.5-flash-001",   # Stable version 001
            ]
            # Ưu tiên model từ config nếu hợp lệ
            if model_name and model_name in VALID_MODELS:
                models_to_try = [model_name] + [m for m in VALID_MODELS if m != model_name]
            else:
                models_to_try = VALID_MODELS
            
            tried_models = []
            last_error = "N/A"
            for m in models_to_try:
                # Nếu một model đã bị lỗi quota ở v1beta thì không cần thử tiếp v1 của chính nó
                model_quota_exceeded = False
                
                for api_ver in ["v1beta", "v1"]:
                    if model_quota_exceeded:
                        break
                        
                    url = f"https://generativelanguage.googleapis.com/{api_ver}/models/{m}:generateContent"
                    params = {"key": api_key}
                    headers = {"Content-Type": "application/json"}
                    data = {
                        "contents": [{
                            "parts": [{
                                "text": f"{system_prompt}\n\nCâu hỏi: {cau_hoi}"
                            }]
                        }]
                    }
                    
                    try:
                        _logger.info(f"Đang thử model: {m} ({api_ver})")
                        response = requests.post(url, headers=headers, params=params, json=data, timeout=60)
                        
                        if response.status_code == 200:
                            result = response.json()
                            return result['candidates'][0]['content']['parts'][0]['text']
                            
                        elif response.status_code == 429:
                            _logger.warning(f"Model {m} ({api_ver}) hết quota.")
                            last_error = f"Model {m} hết quota (429)"
                            tried_models.append(f"{m} (429)")
                            model_quota_exceeded = True # Bỏ qua api_ver tiếp theo của model này
                            continue
                            
                        elif response.status_code == 404:
                            last_error = f"404 - {m} không tồn tại trong {api_ver}"
                            tried_models.append(f"{m}/{api_ver} (404)")
                            continue # Thử version khác
                            
                        else:
                            last_error = f"API Error ({m}/{api_ver}): {response.status_code} - {response.text[:200]}"
                            tried_models.append(f"{m} (Error {response.status_code})")
                    except Exception as e:
                        last_error = str(e)
                        _logger.error(f"Lỗi khi gọi {m}/{api_ver}: {last_error}")
                        tried_models.append(f"{m} (Exception)")
                        continue
            
            # Nếu chạy hết vòng lặp mà không được
            raise UserError(
                f"Tất cả các model AI đều không khả dụng hoặc hết quota.\n\n"
                f"Danh sách đã thử: {', '.join(tried_models)}\n"
                f"Lỗi cuối cùng: {last_error}\n\n"
                f"Giải pháp:\n"
                f"1. Kiểm tra lại API Key trong Cài đặt > AI Assistant\n"
                f"2. Truy cập aistudio.google.com/apikey để tạo Key mới nếu Key cũ bị khóa\n"
                f"3. Hoặc chuyển sang dùng OpenRouter API (có phí cực rẻ/miễn phí) để ổn định hơn."
            )

        else:
            # Cấu hình cho OpenRouter / OpenAI format
            url = api_url
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost:8069",
                "X-Title": "Odoo AI Assistant"
            }
            data = {
                "model": model_name,
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": cau_hoi}
                ],
                "temperature": 0.7,
                "max_tokens": 2000
            }

            # DEBUG: Print to terminal directly
            print("\n" + "="*50)
            print(f"DEBUG AI TYPE: OpenRouter")
            print(f"DEBUG URL: {url}")
            print(f"DEBUG API_URL_INPUT: '{api_url}'")
            print("="*50 + "\n")
            
            try:
                response = requests.post(
                    url,
                    headers=headers,
                    json=data,
                    timeout=60
                )
                
                if response.status_code == 200:
                    result = response.json()
                    return result['choices'][0]['message']['content']
                else:
                    error_msg = f"API Error: {response.status_code} - {response.text}"
                    _logger.error(error_msg)
                    raise UserError(error_msg)
            except Exception as e:
                raise UserError(f"Lỗi kết nối API: {str(e)}")
    
    # ==================== ACTION ====================
    def action_hoi_ai(self):
        """Gửi câu hỏi đến AI"""
        self.ensure_one()
        
        # Lấy context data
        context_data = self._get_context_by_type()
        
        # Gọi API
        try:
            tra_loi = self._call_ai_api(self.cau_hoi, context_data)
            
            # Lưu lịch sử
            self.env['ai.lich_su_chat'].create({
                'cau_hoi': self.cau_hoi,
                'tra_loi': tra_loi,
                'context_data': context_data[:3000],  # Giới hạn chặt chẽ hơn để tiết kiệm token
                'thanh_cong': True,
            })
            
            # Format HTML cho trả lời
            tra_loi_html = tra_loi.replace('\n', '<br/>')
            self.tra_loi = f"<div style='white-space: pre-wrap;'>{tra_loi_html}</div>"
            
        except Exception as e:
            # Lưu lỗi
            self.env['ai.lich_su_chat'].create({
                'cau_hoi': self.cau_hoi,
                'tra_loi': '',
                'context_data': context_data[:3000],
                'thanh_cong': False,
                'loi': str(e),
            })
            raise
        
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'ai.assistant',
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }
