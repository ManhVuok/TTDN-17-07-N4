import os

directories_to_scan = [
    r"c:\TTDN-17-07-N4\addons\nhan_su",
    r"c:\TTDN-17-07-N4\addons\cham_cong",
    r"c:\TTDN-17-07-N4\addons\tinh_luong"
]

def refactor_env():
    for d in directories_to_scan:
        for root, dirs, files in os.walk(d):
            for file in files:
                if file.endswith('.py'):
                    filepath = os.path.join(root, file)
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()

                    new_content = content
                    
                    new_content = new_content.replace("env['nhan_vien']", "env['hr.employee']")
                    new_content = new_content.replace('env["nhan_vien"]', 'env["hr.employee"]')
                    
                    if content != new_content:
                        print(f"Refactored env in {filepath}")
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(new_content)

if __name__ == '__main__':
    refactor_env()
