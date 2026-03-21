# -*- coding: utf-8 -*-
{
    'name': "Quản lý Nhân sự",
    'summary': """
        Module quản lý hồ sơ nhân viên, phòng ban, chức vụ và lịch sử công tác.""",
    'description': """
        Module Quản lý Nhân sự
        ======================
        
        Tính năng chính:
        - Quản lý hồ sơ nhân viên đầy đủ
        - Quản lý cơ cấu phòng ban
        - Quản lý chức vụ và cấp bậc
        - Theo dõi lịch sử công tác
        - Quản lý bằng cấp, chứng chỉ
        - Dashboard thống kê nhân sự
        - AI Assistant tích hợp (OpenRouter API)
    """,
    'author': "Business Internship Team",
    'website': "http://www.yourcompany.com",
    'category': 'Human Resources',
    'version': '1.1',
    'license': 'LGPL-3',
    'depends': ['base'],
    'external_dependencies': {
        'python': ['requests'],
    },
    'data': [
        'security/ir.model.access.csv',
        'views/nhan_vien.xml',
        'views/phong_ban.xml',
        'views/chuc_vu.xml',
        'views/lich_su_cong_tac.xml',
        'views/chung_chi_bang_cap.xml',
        'views/danh_sach_chung_chi_bang_cap.xml',
        'views/ai_assistant.xml',
        'views/dashboard.xml',
        'views/telegram_config.xml',
        'report/ho_so_nhan_vien_report.xml',
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
