import os
import re

directories_to_scan = [
    r"c:\TTDN-17-07-N4\addons\nhan_su",
    r"c:\TTDN-17-07-N4\addons\cham_cong",
    r"c:\TTDN-17-07-N4\addons\tinh_luong"
]

def refactor_files():
    for d in directories_to_scan:
        for root, dirs, files in os.walk(d):
            # Update Python files
            for file in files:
                if file.endswith('.py') or file.endswith('.xml') or file.endswith('.csv'):
                    filepath = os.path.join(root, file)
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()

                    new_content = content
                    
                    if file == '__manifest__.py':
                        if "'depends': ['base'" in new_content and "'hr'" not in new_content:
                            new_content = new_content.replace("'depends': ['base'", "'depends': ['base', 'hr'")
                        if '"depends": ["base"' in new_content and '"hr"' not in new_content:
                            new_content = new_content.replace('"depends": ["base"', '"depends": ["base", "hr"')
                        if "'depends': ['base'" in new_content and "'hr'" not in new_content:
                            new_content = new_content.replace("'depends': ['base',", "'depends': ['base', 'hr',")

                    if file.endswith('.csv'):
                        # removing nhan_vien from IR access
                        if "nhan_vien" in new_content:
                            new_content = new_content.replace("access_nhan_vien", "access_custom_nhan_vien")

                    if file.endswith('.py'):
                        if file == 'nhan_vien.py':
                            # specifically change to inherit
                            new_content = new_content.replace("_name = 'nhan_vien'", "_inherit = 'hr.employee'")
                            new_content = new_content.replace("_name = \"nhan_vien\"", "_inherit = 'hr.employee'")
                            # disable duplicate fields
                            new_content = re.sub(r"(ho_va_ten\s*=\s*)", r"# \1", new_content)
                            new_content = re.sub(r"(anh\s*=\s*)", r"# \1", new_content)
                            new_content = re.sub(r"(gioi_tinh\s*=\s*fields\.Selection)", r"# \1", new_content)
                            new_content = re.sub(r"(email\s*=\s*)", r"# \1", new_content)
                            new_content = re.sub(r"(so_dien_thoai\s*=\s*)", r"# \1", new_content)
                            new_content = re.sub(r"(phong_ban_id\s*=\s*)", r"# \1", new_content)
                            new_content = re.sub(r"(chuc_vu_id\s*=\s*)", r"# \1", new_content)

                        # Relationships
                        new_content = new_content.replace("Many2one('nhan_vien'", "Many2one('hr.employee'")
                        new_content = new_content.replace("Many2one(\"nhan_vien\"", "Many2one(\"hr.employee\"")
                        new_content = new_content.replace("Many2many('nhan_vien'", "Many2many('hr.employee'")
                        new_content = new_content.replace("Many2many(\"nhan_vien\"", "Many2many(\"hr.employee\"")

                        new_content = new_content.replace(".ho_va_ten", ".name")
                        new_content = new_content.replace("nhan_vien_id.ho_va_ten", "nhan_vien_id.name")

                    if file.endswith('.xml'):
                        # Replacing tree and form reference of ho_va_ten to name
                        new_content = new_content.replace("name=\"ho_va_ten\"", "name=\"name\"")
                        new_content = new_content.replace("name=\"anh\"", "name=\"image_1920\"")
                        new_content = new_content.replace("name=\"gioi_tinh\"", "name=\"gender\"")
                        new_content = new_content.replace("name=\"email\"", "name=\"work_email\"")
                        new_content = new_content.replace("name=\"so_dien_thoai\"", "name=\"work_phone\"")

                    if content != new_content:
                        print(f"Refactoring {filepath}")
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(new_content)

if __name__ == '__main__':
    refactor_files()
