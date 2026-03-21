# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class CauHinhLuong(models.Model):
    """
    Cấu hình các thông số tính lương chung cho công ty.
    Bao gồm: tỷ lệ bảo hiểm, số công chuẩn, mức phạt đi muộn/về sớm...
    """
    _name = 'cau_hinh_luong'
    _description = 'Cấu hình tính lương'
    _rec_name = 'ten_cau_hinh'

    ten_cau_hinh = fields.Char("Tên cấu hình", required=True, default="Cấu hình mặc định")
    
    # Thông tin đơn vị tiền tệ
    don_vi_tien = fields.Char("Đơn vị tiền tệ", default="VNĐ")
    
    # Số công chuẩn trong tháng
    so_cong_chuan = fields.Float(
        "Số công chuẩn/tháng", 
        default=24.0,
        help="Số ngày công làm việc tiêu chuẩn trong 1 tháng"
    )
    
    # Tỷ lệ bảo hiểm xã hội (phần người lao động đóng)
    ty_le_bhxh = fields.Float(
        "Tỷ lệ BHXH (%)", 
        default=8.0,
        help="Tỷ lệ bảo hiểm xã hội người lao động đóng (mặc định 8%)"
    )
    ty_le_bhyt = fields.Float(
        "Tỷ lệ BHYT (%)", 
        default=1.5,
        help="Tỷ lệ bảo hiểm y tế người lao động đóng (mặc định 1.5%)"
    )
    ty_le_bhtn = fields.Float(
        "Tỷ lệ BHTN (%)", 
        default=1.0,
        help="Tỷ lệ bảo hiểm thất nghiệp người lao động đóng (mặc định 1%)"
    )
    
    # Mức khấu trừ đi muộn/về sớm
    muc_phat_di_muon = fields.Float(
        "Mức phạt đi muộn (VNĐ/phút)",
        default=5000.0,
        help="Số tiền khấu trừ cho mỗi phút đi muộn"
    )
    muc_phat_ve_som = fields.Float(
        "Mức phạt về sớm (VNĐ/phút)",
        default=5000.0,
        help="Số tiền khấu trừ cho mỗi phút về sớm"
    )
    muc_phat_vang_mat = fields.Float(
        "Mức phạt vắng mặt không phép (VNĐ/ngày)",
        default=200000.0,
        help="Số tiền khấu trừ cho mỗi ngày vắng mặt không phép"
    )
    
    # Ngưỡng miễn trừ
    nguong_mien_phat_di_muon = fields.Float(
        "Ngưỡng miễn phạt đi muộn (phút)",
        default=5.0,
        help="Số phút đi muộn được miễn phạt"
    )
    nguong_mien_phat_ve_som = fields.Float(
        "Ngưỡng miễn phạt về sớm (phút)",
        default=5.0,
        help="Số phút về sớm được miễn phạt"
    )
    
    # Thuế TNCN
    muc_giam_tru_ban_than = fields.Float(
        "Mức giảm trừ bản thân",
        default=11000000.0,
        help="Mức giảm trừ gia cảnh bản thân (11 triệu VNĐ)"
    )
    muc_giam_tru_nguoi_phu_thuoc = fields.Float(
        "Mức giảm trừ người phụ thuộc",
        default=4400000.0,
        help="Mức giảm trừ cho mỗi người phụ thuộc (4.4 triệu VNĐ)"
    )
    
    # Trạng thái
    active = fields.Boolean("Đang sử dụng", default=True)
    
    # Ghi chú
    ghi_chu = fields.Text("Ghi chú")
    
    @api.constrains('ty_le_bhxh', 'ty_le_bhyt', 'ty_le_bhtn')
    def _check_ty_le_bao_hiem(self):
        for record in self:
            if record.ty_le_bhxh < 0 or record.ty_le_bhxh > 100:
                raise ValidationError("Tỷ lệ BHXH phải từ 0 đến 100%")
            if record.ty_le_bhyt < 0 or record.ty_le_bhyt > 100:
                raise ValidationError("Tỷ lệ BHYT phải từ 0 đến 100%")
            if record.ty_le_bhtn < 0 or record.ty_le_bhtn > 100:
                raise ValidationError("Tỷ lệ BHTN phải từ 0 đến 100%")
    
    @api.constrains('so_cong_chuan')
    def _check_so_cong_chuan(self):
        for record in self:
            if record.so_cong_chuan <= 0 or record.so_cong_chuan > 31:
                raise ValidationError("Số công chuẩn phải lớn hơn 0 và không quá 31 ngày")


class CauHinhThue(models.Model):
    """
    Bảng thuế thu nhập cá nhân theo bậc
    """
    _name = 'cau_hinh_thue'
    _description = 'Cấu hình thuế TNCN theo bậc'
    _order = 'muc_tu asc'
    
    ten_bac = fields.Char("Tên bậc thuế", required=True)
    muc_tu = fields.Float("Từ (VNĐ)", required=True)
    muc_den = fields.Float("Đến (VNĐ)", required=True)
    ty_le_thue = fields.Float("Tỷ lệ thuế (%)", required=True)
    
    @api.constrains('muc_tu', 'muc_den', 'ty_le_thue')
    def _check_muc_thue(self):
        for record in self:
            if record.muc_tu < 0:
                raise ValidationError("Mức từ phải >= 0")
            if record.muc_den <= record.muc_tu:
                raise ValidationError("Mức đến phải lớn hơn mức từ")
            if record.ty_le_thue < 0 or record.ty_le_thue > 100:
                raise ValidationError("Tỷ lệ thuế phải từ 0 đến 100%")
