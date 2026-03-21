# -*- coding: utf-8 -*-
{
    'name': "Tính Lương",
    'summary': """
        Module tính lương tự động dựa trên hồ sơ nhân sự và dữ liệu chấm công thực tế.
        Tự động tính bảo hiểm xã hội, y tế, thất nghiệp.""",
    'description': """
        Module Tính Lương - Kết hợp với Nhân Sự và Chấm Công
        =====================================================
        
        Tính năng chính:
        - Quản lý hợp đồng lao động và mức lương
        - Thiết lập phụ cấp theo chức vụ, phòng ban
        - Tự động tính công dựa trên dữ liệu chấm công
        - Tính các khoản bảo hiểm (BHXH, BHYT, BHTN)
        - Khấu trừ đi muộn, về sớm
        - Tính thuế TNCN theo biểu lũy tiến
        - Tạo bảng lương theo tháng
        - Xuất phiếu lương PDF
        - Dashboard thống kê lương
    """,
    'author': "Business Internship Team",
    'website': "http://www.yourcompany.com",
    'category': 'Human Resources',
    'version': '1.0',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'nhan_su',
        'cham_cong'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/cau_hinh_luong.xml',
        'views/hop_dong_lao_dong.xml',
        'views/phu_cap.xml',
        'views/bang_luong.xml',
        'views/chi_tiet_luong.xml',
        'views/nhan_vien_extend.xml',
        'views/dashboard.xml',
        'data/ir_cron_data.xml',
        'report/phieu_luong_report.xml',
        'views/menu.xml',
        'data/sample_data.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
