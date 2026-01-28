from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import ValidationError

class NhanVien(models.Model):
    _name = 'nhan_vien'
    _description = 'Bảng chứa thông tin nhân viên'
    _rec_name = 'ho_va_ten'
    _order = 'ten asc, tuoi desc'

    # ==================== THÔNG TIN CƠ BẢN ====================
    ma_dinh_danh = fields.Char("Mã nhân viên", required=True, copy=False)
    ho_ten_dem = fields.Char("Họ tên đệm", required=True)
    ten = fields.Char("Tên", required=True)
    ho_va_ten = fields.Char("Họ và tên", compute="_compute_ho_va_ten", store=True)
    ngay_sinh = fields.Date("Ngày sinh", required=True)
    tuoi = fields.Integer("Tuổi", compute="_compute_tinh_tuoi", store=True)
    gioi_tinh = fields.Selection([
        ("Nam", "Nam"),
        ("Nữ", "Nữ")
    ], string="Giới tính", required=True)
    
    anh = fields.Binary("Ảnh đại diện")
    
    # ==================== TRẠNG THÁI LÀM VIỆC ====================
    trang_thai = fields.Selection([
        ('dang_lam', 'Đang làm việc'),
        ('thu_viec', 'Đang thử việc'),
        ('nghi_thai_san', 'Nghỉ thai sản'),
        ('tam_nghi', 'Tạm nghỉ'),
        ('nghi_viec', 'Đã nghỉ việc'),
    ], string="Trạng thái", default='dang_lam', required=True)
    
    ngay_vao_lam = fields.Date("Ngày vào làm")
    ngay_nghi_viec = fields.Date("Ngày nghỉ việc")
    
    # ==================== THÔNG TIN CÁ NHÂN ====================
    # CMND/CCCD
    so_cmnd = fields.Char("Số CMND/CCCD")
    ngay_cap_cmnd = fields.Date("Ngày cấp")
    noi_cap_cmnd = fields.Char("Nơi cấp")
    
    # Địa chỉ
    que_quan = fields.Char("Quê quán", required=True)
    dia_chi_hien_tai = fields.Text("Địa chỉ hiện tại")
    
    # Tình trạng hôn nhân
    tinh_trang_hon_nhan = fields.Selection([
        ('doc_than', 'Độc thân'),
        ('da_ket_hon', 'Đã kết hôn'),
        ('ly_hon', 'Ly hôn'),
        ('goa', 'Góa'),
    ], string="Tình trạng hôn nhân", default='doc_than')
    
    # ==================== THÔNG TIN LIÊN HỆ ====================
    email = fields.Char("Email", required=True)
    so_dien_thoai = fields.Char("Số điện thoại", required=True)
    email_cong_ty = fields.Char("Email công ty")
    
    # ==================== NGƯỜI LIÊN HỆ KHẨN CẤP ====================
    nguoi_lien_he_khan_cap = fields.Char("Người liên hệ khẩn cấp")
    sdt_khan_cap = fields.Char("SĐT khẩn cấp")
    quan_he_khan_cap = fields.Char("Quan hệ")
    
    # ==================== THÔNG TIN NGÂN HÀNG ====================
    ten_ngan_hang = fields.Char("Tên ngân hàng")
    so_tai_khoan = fields.Char("Số tài khoản")
    chi_nhanh_ngan_hang = fields.Char("Chi nhánh")
    
    # ==================== THÔNG TIN TỔ CHỨC ====================
    phong_ban_id = fields.Many2one(
        "phong_ban", 
        string="Phòng ban", 
        compute="_compute_cong_tac", 
        store=True
    )
    chuc_vu_id = fields.Many2one(
        "chuc_vu", 
        string="Chức vụ", 
        compute="_compute_cong_tac", 
        store=True
    )
    
    # ==================== QUAN HỆ ====================
    lich_su_cong_tac_ids = fields.One2many(
        "lich_su_cong_tac", 
        inverse_name="nhan_vien_id", 
        string="Danh sách lịch sử công tác"
    )
    danh_sach_chung_chi_bang_cap_ids = fields.One2many(
        "danh_sach_chung_chi_bang_cap",
        inverse_name="nhan_vien_id",
        string="Danh sách chứng chỉ bằng cấp"
    )
    
    # ==================== SQL CONSTRAINTS ====================
    _sql_constraints = [
        ('ma_dinh_danh_unique', 'UNIQUE(ma_dinh_danh)', 'Mã nhân viên phải là duy nhất!'),
        ('email_unique', 'UNIQUE(email)', 'Email đã tồn tại trong hệ thống!'),
    ]
    
    # ==================== COMPUTED FIELDS ====================
    @api.depends("ngay_sinh")
    def _compute_tinh_tuoi(self): 
        for record in self:
            if record.ngay_sinh:
                year_now = datetime.now().year  
                record.tuoi = year_now - record.ngay_sinh.year
            else:
                record.tuoi = 0
    
    @api.depends('ho_ten_dem', 'ten')
    def _compute_ho_va_ten(self):
        for record in self:
            record.ho_va_ten = (record.ho_ten_dem or '') + ' ' + (record.ten or '')
    
    @api.depends("lich_su_cong_tac_ids")
    def _compute_cong_tac(self):
        for record in self:
            if record.lich_su_cong_tac_ids:
                lich_su = self.env['lich_su_cong_tac'].search([
                    ('nhan_vien_id', '=', record.id),
                    ('loai_chuc_vu', '=', "Chính"),
                    ('trang_thai', '=', "Đang giữ")
                ], limit=1)
                record.chuc_vu_id = lich_su.chuc_vu_id.id if lich_su else False
                record.phong_ban_id = lich_su.phong_ban_id.id if lich_su else False
            else:
                record.chuc_vu_id = False
                record.phong_ban_id = False
            
    # ==================== CONSTRAINTS ====================
    @api.constrains("tuoi")
    def _check_tuoi(self):
        for record in self:
            if record.tuoi and record.tuoi < 18:
                raise ValidationError("Tuổi không được nhỏ hơn 18")
    
    @api.constrains("so_cmnd")
    def _check_cmnd(self):
        for record in self:
            if record.so_cmnd:
                # CMND 9 số hoặc CCCD 12 số
                if len(record.so_cmnd) not in [9, 12]:
                    raise ValidationError("Số CMND phải có 9 số hoặc CCCD phải có 12 số!")
    
    # ==================== ONCHANGE ====================
    @api.onchange('trang_thai')
    def _onchange_trang_thai(self):
        if self.trang_thai == 'nghi_viec' and not self.ngay_nghi_viec:
            self.ngay_nghi_viec = fields.Date.today()
