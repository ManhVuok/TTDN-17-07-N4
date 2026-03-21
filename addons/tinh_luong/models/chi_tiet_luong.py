# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError
from datetime import date


class ChiTietLuong(models.Model):
    """
    Chi tiết lương của từng nhân viên trong bảng lương.
    Tự động tính toán dựa trên:
    - Hợp đồng lao động (lương cơ bản, phụ cấp)
    - Dữ liệu chấm công thực tế (số công, đi muộn, về sớm)
    - Cấu hình lương (bảo hiểm, mức phạt)
    """
    _name = 'chi_tiet_luong'
    _description = 'Chi tiết lương nhân viên'
    _rec_name = 'nhan_vien_id'
    _order = 'nhan_vien_id'

    # Liên kết bảng lương
    bang_luong_id = fields.Many2one(
        'bang_luong',
        string="Bảng lương",
        required=True,
        ondelete='cascade'
    )
    
    # Thông tin kỳ lương (từ bảng lương)
    thang = fields.Selection(related='bang_luong_id.thang', store=True)
    nam = fields.Char(related='bang_luong_id.nam', store=True)
    ngay_bat_dau = fields.Date(related='bang_luong_id.ngay_bat_dau', store=True)
    ngay_ket_thuc = fields.Date(related='bang_luong_id.ngay_ket_thuc', store=True)
    cau_hinh_luong_id = fields.Many2one(related='bang_luong_id.cau_hinh_luong_id', store=True)
    
    # Thông tin nhân viên
    nhan_vien_id = fields.Many2one(
        'nhan_vien',
        string="Nhân viên",
        required=True
    )
    phong_ban_id = fields.Many2one(
        related='nhan_vien_id.phong_ban_id',
        string="Phòng ban",
        store=True
    )
    chuc_vu_id = fields.Many2one(
        related='nhan_vien_id.chuc_vu_id',
        string="Chức vụ",
        store=True
    )
    
    # Hợp đồng áp dụng
    hop_dong_id = fields.Many2one(
        'hop_dong_lao_dong',
        string="Hợp đồng",
        required=True
    )
    
    # === THÔNG TIN TỪ HỢP ĐỒNG ===
    luong_co_ban = fields.Float(
        "Lương cơ bản",
        compute="_compute_tu_hop_dong",
        store=True
    )
    luong_dong_bao_hiem = fields.Float(
        "Lương đóng BH",
        compute="_compute_tu_hop_dong",
        store=True
    )
    so_nguoi_phu_thuoc = fields.Integer(
        "Số người phụ thuộc",
        compute="_compute_tu_hop_dong",
        store=True
    )
    
    # === THÔNG TIN CHẤM CÔNG (TỰ ĐỘNG TÍNH TỪ MODULE CHAM_CONG) ===
    so_cong_chuan = fields.Float(
        "Số công chuẩn",
        compute="_compute_tu_cau_hinh",
        store=True
    )
    so_cong_thuc_te = fields.Float(
        "Số công thực tế",
        compute="_compute_cham_cong",
        store=True,
        help="Tự động tính từ dữ liệu chấm công"
    )
    so_ngay_vang = fields.Float(
        "Số ngày vắng",
        compute="_compute_cham_cong",
        store=True
    )
    so_ngay_vang_co_phep = fields.Float(
        "Số ngày vắng có phép",
        compute="_compute_cham_cong",
        store=True
    )
    so_ngay_vang_khong_phep = fields.Float(
        "Số ngày vắng không phép",
        compute="_compute_cham_cong",
        store=True
    )
    tong_phut_di_muon = fields.Float(
        "Tổng phút đi muộn",
        compute="_compute_cham_cong",
        store=True
    )
    tong_phut_ve_som = fields.Float(
        "Tổng phút về sớm",
        compute="_compute_cham_cong",
        store=True
    )
    
    # === CÁC KHOẢN THU NHẬP ===
    luong_theo_cong = fields.Float(
        "Lương theo công",
        compute="_compute_luong_theo_cong",
        store=True,
        help="= (Lương cơ bản / Số công chuẩn) × Số công thực tế"
    )
    
    # === LÀM THÊM GIỜ (OT) ===
    so_gio_lam_them_ngay_thuong = fields.Float(
        "Giờ OT ngày thường",
        default=0.0,
        help="Số giờ làm thêm ngày thường (hệ số 150%)"
    )
    so_gio_lam_them_cuoi_tuan = fields.Float(
        "Giờ OT cuối tuần",
        default=0.0,
        help="Số giờ làm thêm cuối tuần (hệ số 200%)"
    )
    so_gio_lam_them_ngay_le = fields.Float(
        "Giờ OT ngày lễ",
        default=0.0,
        help="Số giờ làm thêm ngày lễ (hệ số 300%)"
    )
    tien_lam_them_gio = fields.Float(
        "Tiền làm thêm giờ",
        compute="_compute_tien_ot",
        store=True,
        help="Tổng tiền OT = Lương giờ × Số giờ × Hệ số"
    )
    
    tong_phu_cap = fields.Float(
        "Tổng phụ cấp",
        compute="_compute_phu_cap",
        store=True
    )
    thu_nhap_khac = fields.Float(
        "Thu nhập khác",
        default=0.0,
        help="Thưởng, trợ cấp đặc biệt..."
    )
    tong_thu_nhap = fields.Float(
        "Tổng thu nhập (Gross)",
        compute="_compute_tong_thu_nhap",
        store=True
    )
    
    # === CÁC KHOẢN KHẤU TRỪ ===
    # Bảo hiểm
    tien_bhxh = fields.Float(
        "BHXH (8%)",
        compute="_compute_bao_hiem",
        store=True
    )
    tien_bhyt = fields.Float(
        "BHYT (1.5%)",
        compute="_compute_bao_hiem",
        store=True
    )
    tien_bhtn = fields.Float(
        "BHTN (1%)",
        compute="_compute_bao_hiem",
        store=True
    )
    tong_bao_hiem = fields.Float(
        "Tổng BH người LĐ đóng",
        compute="_compute_bao_hiem",
        store=True
    )
    
    # Khấu trừ vi phạm
    tien_phat_di_muon = fields.Float(
        "Tiền phạt đi muộn",
        compute="_compute_tien_phat",
        store=True
    )
    tien_phat_ve_som = fields.Float(
        "Tiền phạt về sớm",
        compute="_compute_tien_phat",
        store=True
    )
    tien_phat_vang_mat = fields.Float(
        "Tiền phạt vắng mặt",
        compute="_compute_tien_phat",
        store=True
    )
    tong_tien_phat = fields.Float(
        "Tổng tiền phạt",
        compute="_compute_tien_phat",
        store=True
    )
    
    # Thuế TNCN
    thu_nhap_chiu_thue = fields.Float(
        "Thu nhập chịu thuế",
        compute="_compute_thue_tncn",
        store=True
    )
    giam_tru_gia_canh = fields.Float(
        "Giảm trừ gia cảnh",
        compute="_compute_thue_tncn",
        store=True
    )
    thu_nhap_tinh_thue = fields.Float(
        "Thu nhập tính thuế",
        compute="_compute_thue_tncn",
        store=True
    )
    thue_tncn = fields.Float(
        "Thuế TNCN",
        compute="_compute_thue_tncn",
        store=True
    )
    
    # Khấu trừ khác
    khau_tru_khac = fields.Float(
        "Khấu trừ khác",
        default=0.0
    )
    
    tong_khau_tru = fields.Float(
        "Tổng khấu trừ",
        compute="_compute_tong_khau_tru",
        store=True
    )
    
    # LƯƠNG THỰC NHẬN ===
    luong_thuc_nhan = fields.Float(
        "Lương thực nhận (Net)",
        compute="_compute_luong_thuc_nhan",
        store=True
    )
    
    # Ghi chú & AI
    ghi_chu = fields.Text("Ghi chú")
    ai_nhan_xet = fields.Text("AI Nhận xét Email", help="Nội dung đánh giá sinh tự động bởi AI")
    
    # === COMPUTED METHODS ===
    
    @api.depends('hop_dong_id', 'hop_dong_id.luong_co_ban', 
                 'hop_dong_id.luong_dong_bao_hiem', 'hop_dong_id.so_nguoi_phu_thuoc')
    def _compute_tu_hop_dong(self):
        for record in self:
            if record.hop_dong_id:
                record.luong_co_ban = record.hop_dong_id.luong_co_ban
                record.luong_dong_bao_hiem = record.hop_dong_id.luong_dong_bao_hiem or record.hop_dong_id.luong_co_ban
                record.so_nguoi_phu_thuoc = record.hop_dong_id.so_nguoi_phu_thuoc
            else:
                record.luong_co_ban = 0
                record.luong_dong_bao_hiem = 0
                record.so_nguoi_phu_thuoc = 0
    
    @api.depends('cau_hinh_luong_id', 'cau_hinh_luong_id.so_cong_chuan')
    def _compute_tu_cau_hinh(self):
        for record in self:
            if record.cau_hinh_luong_id:
                record.so_cong_chuan = record.cau_hinh_luong_id.so_cong_chuan
            else:
                record.so_cong_chuan = 24.0  # Mặc định
    
    @api.depends('nhan_vien_id', 'ngay_bat_dau', 'ngay_ket_thuc')
    def _compute_cham_cong(self):
        """
        Tự động tính số công từ dữ liệu chấm công (module cham_cong)
        """
        bang_cham_cong = self.env['bang_cham_cong']
        
        for record in self:
            if not record.nhan_vien_id or not record.ngay_bat_dau or not record.ngay_ket_thuc:
                record.so_cong_thuc_te = 0
                record.so_ngay_vang = 0
                record.so_ngay_vang_co_phep = 0
                record.so_ngay_vang_khong_phep = 0
                record.tong_phut_di_muon = 0
                record.tong_phut_ve_som = 0
                continue
            
            # Tìm tất cả bản ghi chấm công trong kỳ
            cham_cong_records = bang_cham_cong.search([
                ('nhan_vien_id', '=', record.nhan_vien_id.id),
                ('ngay_cham_cong', '>=', record.ngay_bat_dau),
                ('ngay_cham_cong', '<=', record.ngay_ket_thuc),
            ])
            
            so_cong = 0
            so_vang = 0
            so_vang_co_phep = 0
            so_vang_ko_phep = 0
            tong_di_muon = 0
            tong_ve_som = 0
            
            for cc in cham_cong_records:
                # Tính số công dựa trên ca làm
                if cc.ca_lam == 'Cả ngày':
                    cong_ngay = 1.0
                elif cc.ca_lam in ['Sáng', 'Chiều']:
                    cong_ngay = 0.5
                else:
                    cong_ngay = 0
                
                if cc.trang_thai == 'di_lam':
                    so_cong += cong_ngay
                elif cc.trang_thai in ['di_muon', 've_som', 'di_muon_ve_som']:
                    so_cong += cong_ngay  # Vẫn tính công nhưng sẽ bị phạt
                elif cc.trang_thai == 'vang_mat':
                    so_vang += cong_ngay
                    so_vang_ko_phep += cong_ngay
                elif cc.trang_thai == 'vang_mat_co_phep':
                    so_vang += cong_ngay
                    so_vang_co_phep += cong_ngay
                
                # Tổng phút đi muộn/về sớm (đã trừ đơn từ)
                tong_di_muon += cc.phut_di_muon or 0
                tong_ve_som += cc.phut_ve_som or 0
            
            record.so_cong_thuc_te = so_cong
            record.so_ngay_vang = so_vang
            record.so_ngay_vang_co_phep = so_vang_co_phep
            record.so_ngay_vang_khong_phep = so_vang_ko_phep
            record.tong_phut_di_muon = tong_di_muon
            record.tong_phut_ve_som = tong_ve_som
    
    @api.depends('luong_co_ban', 'so_cong_chuan', 'so_cong_thuc_te')
    def _compute_luong_theo_cong(self):
        for record in self:
            if record.so_cong_chuan > 0:
                luong_ngay = record.luong_co_ban / record.so_cong_chuan
                record.luong_theo_cong = luong_ngay * record.so_cong_thuc_te
            else:
                record.luong_theo_cong = 0
    
    @api.depends('hop_dong_id', 'hop_dong_id.tong_phu_cap')
    def _compute_phu_cap(self):
        for record in self:
            if record.hop_dong_id:
                record.tong_phu_cap = record.hop_dong_id.tong_phu_cap
            else:
                record.tong_phu_cap = 0
    
    @api.depends('luong_co_ban', 'so_cong_chuan', 
                 'so_gio_lam_them_ngay_thuong', 'so_gio_lam_them_cuoi_tuan', 'so_gio_lam_them_ngay_le')
    def _compute_tien_ot(self):
        """
        Tính tiền làm thêm giờ (OT)
        - Ngày thường: 150% lương giờ
        - Cuối tuần : 200% lương giờ  
        - Ngày lễ   : 300% lương giờ
        """
        for record in self:
            if record.so_cong_chuan > 0 and record.luong_co_ban > 0:
                # Lương giờ = Lương ngày / 8 giờ
                luong_gio = (record.luong_co_ban / record.so_cong_chuan) / 8
                
                ot_ngay_thuong = record.so_gio_lam_them_ngay_thuong * luong_gio * 1.5
                ot_cuoi_tuan = record.so_gio_lam_them_cuoi_tuan * luong_gio * 2.0
                ot_ngay_le = record.so_gio_lam_them_ngay_le * luong_gio * 3.0
                
                record.tien_lam_them_gio = ot_ngay_thuong + ot_cuoi_tuan + ot_ngay_le
            else:
                record.tien_lam_them_gio = 0
    
    @api.depends('luong_theo_cong', 'tong_phu_cap', 'thu_nhap_khac', 'tien_lam_them_gio')
    def _compute_tong_thu_nhap(self):
        for record in self:
            record.tong_thu_nhap = (
                record.luong_theo_cong + 
                record.tong_phu_cap + 
                record.thu_nhap_khac + 
                record.tien_lam_them_gio
            )
    
    @api.depends('luong_dong_bao_hiem', 'cau_hinh_luong_id',
                 'cau_hinh_luong_id.ty_le_bhxh', 'cau_hinh_luong_id.ty_le_bhyt',
                 'cau_hinh_luong_id.ty_le_bhtn')
    def _compute_bao_hiem(self):
        for record in self:
            luong_bh = record.luong_dong_bao_hiem or record.luong_co_ban
            
            if record.cau_hinh_luong_id:
                record.tien_bhxh = luong_bh * record.cau_hinh_luong_id.ty_le_bhxh / 100
                record.tien_bhyt = luong_bh * record.cau_hinh_luong_id.ty_le_bhyt / 100
                record.tien_bhtn = luong_bh * record.cau_hinh_luong_id.ty_le_bhtn / 100
            else:
                # Mặc định
                record.tien_bhxh = luong_bh * 0.08
                record.tien_bhyt = luong_bh * 0.015
                record.tien_bhtn = luong_bh * 0.01
            
            record.tong_bao_hiem = record.tien_bhxh + record.tien_bhyt + record.tien_bhtn
    
    @api.depends('tong_phut_di_muon', 'tong_phut_ve_som', 'so_ngay_vang_khong_phep',
                 'cau_hinh_luong_id', 'cau_hinh_luong_id.muc_phat_di_muon',
                 'cau_hinh_luong_id.muc_phat_ve_som', 'cau_hinh_luong_id.muc_phat_vang_mat',
                 'cau_hinh_luong_id.nguong_mien_phat_di_muon', 'cau_hinh_luong_id.nguong_mien_phat_ve_som')
    def _compute_tien_phat(self):
        for record in self:
            if record.cau_hinh_luong_id:
                cfg = record.cau_hinh_luong_id
                
                # Tính phút đi muộn sau khi trừ ngưỡng miễn
                phut_di_muon_tinh = max(0, record.tong_phut_di_muon - cfg.nguong_mien_phat_di_muon)
                phut_ve_som_tinh = max(0, record.tong_phut_ve_som - cfg.nguong_mien_phat_ve_som)
                
                record.tien_phat_di_muon = phut_di_muon_tinh * cfg.muc_phat_di_muon
                record.tien_phat_ve_som = phut_ve_som_tinh * cfg.muc_phat_ve_som
                record.tien_phat_vang_mat = record.so_ngay_vang_khong_phep * cfg.muc_phat_vang_mat
            else:
                record.tien_phat_di_muon = 0
                record.tien_phat_ve_som = 0
                record.tien_phat_vang_mat = 0
            
            record.tong_tien_phat = record.tien_phat_di_muon + record.tien_phat_ve_som + record.tien_phat_vang_mat
    
    @api.depends('tong_thu_nhap', 'tong_bao_hiem', 'so_nguoi_phu_thuoc',
                 'cau_hinh_luong_id', 'cau_hinh_luong_id.muc_giam_tru_ban_than',
                 'cau_hinh_luong_id.muc_giam_tru_nguoi_phu_thuoc')
    def _compute_thue_tncn(self):
        for record in self:
            # Thu nhập chịu thuế = Tổng thu nhập - Các khoản được miễn thuế (như BHXH, BHYT, BHTN)
            record.thu_nhap_chiu_thue = record.tong_thu_nhap - record.tong_bao_hiem
            
            # Giảm trừ gia cảnh
            if record.cau_hinh_luong_id:
                cfg = record.cau_hinh_luong_id
                record.giam_tru_gia_canh = cfg.muc_giam_tru_ban_than + (record.so_nguoi_phu_thuoc * cfg.muc_giam_tru_nguoi_phu_thuoc)
            else:
                record.giam_tru_gia_canh = 11000000 + (record.so_nguoi_phu_thuoc * 4400000)
            
            # Thu nhập tính thuế
            record.thu_nhap_tinh_thue = max(0, record.thu_nhap_chiu_thue - record.giam_tru_gia_canh)
            
            # Tính thuế TNCN theo biểu thuế lũy tiến
            record.thue_tncn = record._tinh_thue_luy_tien(record.thu_nhap_tinh_thue)
    
    def _tinh_thue_luy_tien(self, thu_nhap):
        """
        Tính thuế TNCN theo biểu thuế lũy tiến từng phần
        Biểu thuế áp dụng cho người VN:
        - Đến 5 triệu: 5%
        - Trên 5 - 10 triệu: 10%
        - Trên 10 - 18 triệu: 15%
        - Trên 18 - 32 triệu: 20%
        - Trên 32 - 52 triệu: 25%
        - Trên 52 - 80 triệu: 30%
        - Trên 80 triệu: 35%
        """
        if thu_nhap <= 0:
            return 0
        
        bac_thue = [
            (5000000, 0.05),
            (5000000, 0.10),   # 5-10 triệu
            (8000000, 0.15),   # 10-18 triệu
            (14000000, 0.20),  # 18-32 triệu
            (20000000, 0.25),  # 32-52 triệu
            (28000000, 0.30),  # 52-80 triệu
            (float('inf'), 0.35)  # Trên 80 triệu
        ]
        
        thue = 0
        con_lai = thu_nhap
        
        for muc, ty_le in bac_thue:
            if con_lai <= 0:
                break
            tinh_thue = min(con_lai, muc)
            thue += tinh_thue * ty_le
            con_lai -= muc
        
        return thue
    
    @api.depends('tong_bao_hiem', 'tong_tien_phat', 'thue_tncn', 'khau_tru_khac')
    def _compute_tong_khau_tru(self):
        for record in self:
            record.tong_khau_tru = (record.tong_bao_hiem + record.tong_tien_phat + 
                                    record.thue_tncn + record.khau_tru_khac)
    
    @api.depends('tong_thu_nhap', 'tong_khau_tru')
    def _compute_luong_thuc_nhan(self):
        for record in self:
            record.luong_thuc_nhan = record.tong_thu_nhap - record.tong_khau_tru
    
    def action_tinh_luong(self):
        """
        Tính lại lương cho nhân viên này
        """
        for record in self:
            # Trigger recompute cho tất cả các field computed
            record._compute_tu_hop_dong()
            record._compute_tu_cau_hinh()
            record._compute_cham_cong()
            record._compute_luong_theo_cong()
            record._compute_phu_cap()
            record._compute_tong_thu_nhap()
            record._compute_bao_hiem()
            record._compute_tien_phat()
            record._compute_thue_tncn()
            record._compute_tong_khau_tru()
            record._compute_luong_thuc_nhan()
    
    _sql_constraints = [
        ('nhan_vien_bang_luong_unique', 
         'UNIQUE(nhan_vien_id, bang_luong_id)', 
         'Mỗi nhân viên chỉ có một bản ghi lương trong mỗi bảng lương!')
    ]
    
    def action_xem_cham_cong(self):
        """
        Mở view chấm công của nhân viên trong kỳ lương này
        """
        self.ensure_one()
        return {
            'name': f'Chấm công - {self.nhan_vien_id.ho_va_ten}',
            'type': 'ir.actions.act_window',
            'res_model': 'bang_cham_cong',
            'view_mode': 'tree,form,calendar',
            'domain': [
                ('nhan_vien_id', '=', self.nhan_vien_id.id),
                ('ngay_cham_cong', '>=', self.ngay_bat_dau),
                ('ngay_cham_cong', '<=', self.ngay_ket_thuc),
            ],
            'context': {
                'default_nhan_vien_id': self.nhan_vien_id.id,
            }
        }
