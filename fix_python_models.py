import os

files_and_fixes = [
    r'c:\TTDN-17-07-N4\addons\cham_cong\models\nghi_phep_nam.py',
    r'c:\TTDN-17-07-N4\addons\cham_cong\models\don_tu.py',
    r'c:\TTDN-17-07-N4\addons\tinh_luong\models\hop_dong_lao_dong.py',
    r'c:\TTDN-17-07-N4\addons\tinh_luong\models\chi_tiet_luong.py',
    r'c:\TTDN-17-07-N4\addons\tinh_luong\models\nhan_vien_extend.py',
    r'c:\TTDN-17-07-N4\addons\cham_cong\models\bang_cham_cong.py',
    r'c:\TTDN-17-07-N4\addons\cham_cong\models\don_tu.py',
    r'c:\TTDN-17-07-N4\addons\cham_cong\models\dot_dang_ky.py',
    r'c:\TTDN-17-07-N4\addons\cham_cong\models\nghi_phep_nam.py',
]

for fp in files_and_fixes:
    if not os.path.exists(fp):
        continue
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()
    new = content.replace("'nhan_vien'", "'hr.employee'")
    new = new.replace('"nhan_vien"', '"hr.employee"')
    new = new.replace("_inherit = 'hr.employee'", "_inherit = 'hr.employee'")  # no-op, already ok
    if new != content:
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(new)
        print('Fixed:', fp)
    else:
        print('No change:', fp)
