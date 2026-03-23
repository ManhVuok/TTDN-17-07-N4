import os
import re

directories_to_scan = [
    r"c:\TTDN-17-07-N4\addons\nhan_su",
    r"c:\TTDN-17-07-N4\addons\cham_cong",
    r"c:\TTDN-17-07-N4\addons\tinh_luong"
]

def refactor_xml_and_csv():
    for d in directories_to_scan:
        for root, dirs, files in os.walk(d):
            for file in files:
                filepath = os.path.join(root, file)
                
                if file.endswith('.xml'):
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()

                    new_content = content
                    
                    # Update model and action references
                    new_content = new_content.replace('name="model">nhan_vien<', 'name="model">hr.employee<')
                    new_content = new_content.replace('name="res_model">nhan_vien<', 'name="res_model">hr.employee<')
                    new_content = new_content.replace("kanban_image('nhan_vien'", "kanban_image('hr.employee'")
                    
                    # Update field names inside quotes
                    new_content = new_content.replace('"ho_va_ten"', '"name"')
                    new_content = new_content.replace("'ho_va_ten'", "'name'")
                    new_content = new_content.replace('"anh"', '"image_1920"')
                    new_content = new_content.replace("'anh'", "'image_1920'")
                    new_content = new_content.replace('"gioi_tinh"', '"gender"')
                    new_content = new_content.replace("'gioi_tinh'", "'gender'")
                    new_content = new_content.replace('"email"', '"work_email"')
                    new_content = new_content.replace("'email'", "'work_email'")
                    new_content = new_content.replace('"so_dien_thoai"', '"work_phone"')
                    new_content = new_content.replace("'so_dien_thoai'", "'work_phone'")
                    new_content = new_content.replace('"phong_ban_id"', '"department_id"')
                    new_content = new_content.replace("'phong_ban_id'", "'department_id'")
                    new_content = new_content.replace('"chuc_vu_id"', '"job_id"')
                    new_content = new_content.replace("'chuc_vu_id'", "'job_id'")
                    
                    if new_content != content:
                        print(f"Refactored XML: {filepath}")
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                            
                elif file.endswith('.csv'):
                    with open(filepath, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                    
                    new_lines = []
                    for line in lines:
                        if 'model_nhan_vien' not in line:
                            new_lines.append(line)
                            
                    if len(new_lines) != len(lines):
                        print(f"Refactored CSV: {filepath}")
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.writelines(new_lines)

                elif file.endswith('.py'):
                    # Also fix related field references in python models (like hop_dong_lao_dong)
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    new_content = content
                    new_content = new_content.replace('nhan_vien_id.phong_ban_id', 'nhan_vien_id.department_id')
                    new_content = new_content.replace('nhan_vien_id.chuc_vu_id', 'nhan_vien_id.job_id')
                    
                    if new_content != content:
                        print(f"Refactored Python refs: {filepath}")
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(new_content)

if __name__ == '__main__':
    refactor_xml_and_csv()
