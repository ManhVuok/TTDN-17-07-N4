# -*- coding: utf-8 -*-
{
    'name': "Chấm công",
    'summary': """
        Module quản lý chấm công, đăng ký ca làm và đơn từ của nhân viên.""",
    'description': """
        Module Chấm công
        ================
        
        Tính năng chính:
        - Đăng ký ca làm theo đợt (tháng)
        - Đăng ký ca làm theo ngày (Sáng/Chiều/Cả ngày)
        - Chấm công giờ vào/ra thực tế
        - Tự động tính đi muộn, về sớm
        - Quản lý đơn xin phép (nghỉ, đi muộn, về sớm)
        - Quản lý ca làm việc
        - Quản lý đăng ký tăng ca (OT)
        - Quản lý nghỉ phép năm
        - Dashboard thống kê chấm công
        - Lịch chấm công dạng Calendar
    """,
    'author': "Business Internship Team",
    'website': "http://www.yourcompany.com",
    'category': 'Human Resources',
    'version': '1.1',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'nhan_su'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/ca_lam_viec.xml',
        'views/dang_ky_ca_lam_theo_ngay.xml',
        'views/bang_cham_cong.xml',
        'views/dot_dang_ky.xml',
        'views/don_tu.xml',
        'views/nghi_phep_nam.xml',
        'data/ir_cron_data.xml',
        'views/dashboard.xml',
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
