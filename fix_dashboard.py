import os

files_to_fix = [
    r"c:\TTDN-17-07-N4\addons\nhan_su\views\dashboard.xml",
    r"c:\TTDN-17-07-N4\addons\nhan_su\report\ho_so_nhan_vien_report.xml"
]

for filepath in files_to_fix:
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        new_content = content.replace('"phong_ban_id"', '"department_id"')
        new_content = new_content.replace("'phong_ban_id'", "'department_id'")
        new_content = new_content.replace('"chuc_vu_id"', '"job_id"')
        new_content = new_content.replace("'chuc_vu_id'", "'job_id'")
        
        if content != new_content:
            print(f"Fixed {filepath}")
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
