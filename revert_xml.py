import os

files_to_revert = [
    r"c:\TTDN-17-07-N4\addons\nhan_su\views\lich_su_cong_tac.xml",
    r"c:\TTDN-17-07-N4\addons\nhan_su\views\phong_ban.xml",
    r"c:\TTDN-17-07-N4\addons\nhan_su\views\chuc_vu.xml",
    r"c:\TTDN-17-07-N4\addons\nhan_su\report\ho_so_nhan_vien_report.xml",
    r"c:\TTDN-17-07-N4\addons\cham_cong\views\bang_cham_cong.xml",
    r"c:\TTDN-17-07-N4\addons\cham_cong\views\ca_lam_viec.xml",
    r"c:\TTDN-17-07-N4\addons\tinh_luong\views\bang_luong.xml",
    r"c:\TTDN-17-07-N4\addons\tinh_luong\views\chi_tiet_luong.xml"
]

for filepath in files_to_revert:
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # Revert XML field namings where the base model is NOT hr.employee
        # Wait, if I just globally revert in those files it might revert hr.employee field usages inside them?
        # Typically bang_cham_cong relates to nhan_vien_id, which points to hr.employee!
        # hr.employee DOES have "department_id" and "job_id".
        # But wait! If the model is `bang_cham_cong`, it doesn't have `department_id`, it might use `nhan_vien_id.department_id`.
        # Previously my script did: `new_content.replace('"phong_ban_id"', '"department_id"')`.
        # So `<field name="phong_ban_id"/>` became `<field name="department_id"/>`.
        # If the view is for `lich_su_cong_tac`, it needs `phong_ban_id` because the model has `phong_ban_id`.
        # So I will just revert `"department_id"` -> `"phong_ban_id"` and `"job_id"` -> `"chuc_vu_id"` in `lich_su_cong_tac.xml` ONLY!
        
        # Let's just fix lich_su_cong_tac.xml manually here
        if "lich_su_cong_tac.xml" in filepath:
            content = content.replace('"department_id"', '"phong_ban_id"')
            content = content.replace("'department_id'", "'phong_ban_id'")
            content = content.replace('"job_id"', '"chuc_vu_id"')
            content = content.replace("'job_id'", "'chuc_vu_id'")
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
