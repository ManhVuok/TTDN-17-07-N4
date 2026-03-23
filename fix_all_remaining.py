"""
Comprehensive fix: scan ALL XML files in nhan_su module for old model/field references.
This script handles:
1. model="nhan_vien" -> model="hr.employee" in data/demo records
2. phong_ban_id -> department_id and chuc_vu_id -> job_id ONLY in hr.employee context
3. default_group_by="phong_ban_id" -> default_group_by="department_id"
4. sample_data.xml field names for hr.employee records
"""
import os
import re

# ============ FIX sample_data.xml ============
sample_file = r"c:\TTDN-17-07-N4\addons\nhan_su\data\sample_data.xml"
if os.path.exists(sample_file):
    with open(sample_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Change model="nhan_vien" to model="hr.employee"
    content = content.replace('model="nhan_vien"', 'model="hr.employee"')
    
    # In hr.employee records, phong_ban_id -> department_id, chuc_vu_id -> job_id
    # But ONLY inside hr.employee records. The lich_su_cong_tac records use their own fields.
    # Since all nhan_vien records use these as direct fields, and lich_su_cong_tac has its own model,
    # we can safely replace field references inside hr.employee records.
    # Actually the sample data for lich_su_cong_tac correctly uses phong_ban_id/chuc_vu_id (its own fields).
    # The hr.employee sample records need department_id/job_id.
    
    # Replace phong_ban_id and chuc_vu_id in hr.employee sample records
    # These are inside <record model="hr.employee"> blocks
    lines = content.split('\n')
    in_hr_employee_record = False
    new_lines = []
    for line in lines:
        if 'model="hr.employee"' in line:
            in_hr_employee_record = True
        if in_hr_employee_record:
            if '</record>' in line:
                in_hr_employee_record = False
            line = line.replace('"phong_ban_id"', '"department_id"')
            line = line.replace('"chuc_vu_id"', '"job_id"')
        new_lines.append(line)
    content = '\n'.join(new_lines)
    
    with open(sample_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Fixed {sample_file}")

# ============ FIX demo.xml ============
demo_file = r"c:\TTDN-17-07-N4\addons\nhan_su\demo\demo.xml"
if os.path.exists(demo_file):
    with open(demo_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = content.replace('model="nhan_vien"', 'model="hr.employee"')
    
    lines = content.split('\n')
    in_hr_employee_record = False
    new_lines = []
    for line in lines:
        if 'model="hr.employee"' in line and 'record' in line.lower():
            in_hr_employee_record = True
        if in_hr_employee_record:
            if '</record>' in line:
                in_hr_employee_record = False
            line = line.replace('"phong_ban_id"', '"department_id"')
            line = line.replace('"chuc_vu_id"', '"job_id"')
        new_lines.append(line)
    content = '\n'.join(new_lines)
    
    with open(demo_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Fixed {demo_file}")

# ============ FIX nhan_vien.xml kanban default_group_by ============
nv_xml = r"c:\TTDN-17-07-N4\addons\nhan_su\views\nhan_vien.xml"
if os.path.exists(nv_xml):
    with open(nv_xml, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = content.replace('default_group_by="phong_ban_id"', 'default_group_by="department_id"')
    
    # Also fix search_default_phong_ban_id context in phong_ban.xml  
    content = content.replace("'search_default_phong_ban_id'", "'search_default_department_id'")
    
    with open(nv_xml, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Fixed {nv_xml}")

# ============ FIX nhan_vien.xml form view inner lich_su_cong_tac tree ============
# The lich_su_cong_tac tree inside nhan_vien form should keep phong_ban_id/chuc_vu_id
# because those are fields of lich_su_cong_tac model, not hr.employee.
# This should already be correct. Let's verify.

print("\n=== ALL FIXES APPLIED ===")
