import os

directories_to_scan = [
    r"c:\TTDN-17-07-N4\addons\nhan_su",
    r"c:\TTDN-17-07-N4\addons\cham_cong",
    r"c:\TTDN-17-07-N4\addons\tinh_luong"
]

def safe_refactor():
    for d in directories_to_scan:
        for root, dirs, files in os.walk(d):
            for file in files:
                if file.endswith('.py'):
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

                    # Replace relations
                    new_content = new_content.replace("Many2one('nhan_vien'", "Many2one('hr.employee'")
                    new_content = new_content.replace('Many2one("nhan_vien"', 'Many2one("hr.employee"')
                    new_content = new_content.replace("Many2many('nhan_vien'", "Many2many('hr.employee'")
                    new_content = new_content.replace('Many2many("nhan_vien"', 'Many2many("hr.employee"')

                    # Replace field accesses
                    new_content = new_content.replace(".ho_va_ten", ".name")

                    if content != new_content:
                        print(f"Refactoring {filepath}")
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(new_content)

if __name__ == '__main__':
    safe_refactor()
