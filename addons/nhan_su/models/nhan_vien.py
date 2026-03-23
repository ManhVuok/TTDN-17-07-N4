from odoo import models, fields, api
from datetime import datetime
from odoo.exceptions import ValidationError

class NhanVien(models.Model):
    _inherit = 'hr.employee'
    _description = 'Bảng chứa thông tin nhân viên'

    # ==================== THÔNG TIN CƠ BẢN ====================
    ma_dinh_danh = fields.Char("Mã nhân viên", required=True, copy=False)
    ho_ten_dem = fields.Char("Họ tên đệm", required=True)
    ten = fields.Char("Tên", required=True)
    
    name = fields.Char(string="Họ và tên", compute="_compute_name", store=True, readonly=False)

    @api.depends('ho_ten_dem', 'ten')
    def _compute_name(self):
        for record in self:
            if record.ho_ten_dem or record.ten:
                record.name = ((record.ho_ten_dem or '') + ' ' + (record.ten or '')).strip()

    ngay_sinh = fields.Date("Ngày sinh", required=True)
    tuoi = fields.Integer("Tuổi", compute="_compute_tinh_tuoi", store=True)

    # hr.employee có sẵn 'gender' (gioi_tinh), 'image_1920' (anh) nên ta không định nghĩa lại.
    
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
    # Thay vì dùng email, so_dien_thoai riêng, ta dùng work_email, work_phone của hr.employee
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
    # hr.employee đã có department_id, job_id, ta sẽ dùng hàm compute để map từ lich_su_cong_tac
    # và ta sẽ ghi đè method compute nếu cần, nhưng tốt nhất update logic vào department_id/job_id.
    
    @api.depends("lich_su_cong_tac_ids")
    def _compute_cong_tac(self):
        for record in self:
            if record.lich_su_cong_tac_ids:
                lich_su = self.env['lich_su_cong_tac'].search([
                    ('nhan_vien_id', '=', record.id),
                    ('loai_chuc_vu', '=', "Chính"),
                    ('trang_thai', '=', "Đang giữ")
                ], limit=1)
                record.job_id = lich_su.chuc_vu_id.id if lich_su else False
                record.department_id = lich_su.phong_ban_id.id if lich_su else False
            else:
                record.job_id = False
                record.department_id = False

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

    # ==================== THÂN NHÂN ====================
    family_ids = fields.One2many(
        'hr.family',
        'employee_id',
        string="Danh sách thân nhân"
    )
    so_nguoi_phu_thuoc = fields.Integer(
        "Số người phụ thuộc",
        compute="_compute_so_nguoi_phu_thuoc",
        store=True,
        help="Dùng để tính giảm trừ gia cảnh khi tính thuế TNCN"
    )

    @api.depends('family_ids', 'family_ids.is_dependent')
    def _compute_so_nguoi_phu_thuoc(self):
        for rec in self:
            rec.so_nguoi_phu_thuoc = len(rec.family_ids.filtered(lambda f: f.is_dependent))

    # Ghi đè field 'children' chuẩn Odoo để tự tính từ danh sách thân nhân
    children = fields.Integer(
        string="Số lượng con",
        compute="_compute_children",
    )

    @api.depends('family_ids', 'family_ids.relationship')
    def _compute_children(self):
        for rec in self:
            rec.children = len(rec.family_ids.filtered(lambda f: f.relationship == 'con'))


    
    # ==================== SQL CONSTRAINTS ====================
    _sql_constraints = [
        ('ma_dinh_danh_unique', 'UNIQUE(ma_dinh_danh)', 'Mã nhân viên phải là duy nhất!'),
        # Loại bỏ email_unique tạm thời nếu work_email không yêu cầu unique
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
            
    # ==================== CONSTRAINTS ====================
    @api.constrains('ngay_sinh')
    def _check_ngay_sinh(self):
        """Kiểm tra ngày sinh hợp lệ theo yêu cầu Mức 1 - Giai đoạn 1"""
        for rec in self:
            if rec.ngay_sinh and rec.ngay_sinh > fields.Date.today():
                raise ValidationError("Ngày sinh không được lớn hơn ngày hiện tại!")

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
