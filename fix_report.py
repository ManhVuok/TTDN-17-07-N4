import os

report_file = r"c:\TTDN-17-07-N4\addons\nhan_su\report\ho_so_nhan_vien_report.xml"

if os.path.exists(report_file):
    with open(report_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Model ref
    content = content.replace('ref="model_nhan_vien"', 'ref="hr.model_hr_employee"')
    content = content.replace('object.ho_va_ten', 'object.name')
    
    # Object properties
    content = content.replace('o.ho_va_ten', 'o.name')
    content = content.replace('o.anh', 'o.image_1920')
    content = content.replace('o.phong_ban_id', 'o.department_id')
    content = content.replace('o.chuc_vu_id', 'o.job_id')
    content = content.replace('o.gioi_tinh', 'o.gender')
    content = content.replace('o.email"', 'o.work_email"')
    content = content.replace('o.so_dien_thoai', 'o.work_phone')

    # Fix history properties inside <t t-foreach="o.lich_su_cong_tac_ids" t-as="ls">
    content = content.replace('ls.phong_ban_id', 'ls.phong_ban_id') # lich_su_cong_tac uses phong_ban_id
    content = content.replace('ls.chuc_vu_id', 'ls.chuc_vu_id')
    
    # In earlier replacement my script might have accidentally overwritten ls.department_id back to ls.phong_ban_id anyway
    # But wait, earlier I replaced o.department_id! Let's just be explicit:
    content = content.replace('<td><span t-field="ls.department_id"/></td>', '<td><span t-field="ls.phong_ban_id"/></td>')
    content = content.replace('<td><span t-field="ls.job_id"/></td>', '<td><span t-field="ls.chuc_vu_id"/></td>')

    # Also fix email and work_email just in case
    # <span t-field="o.email"/> -> <span t-field="o.work_email"/>
    content = content.replace('<span t-field="o.email"/>', '<span t-field="o.work_email"/>')

    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print("Fixed ho_so_nhan_vien_report.xml thoroughly")
