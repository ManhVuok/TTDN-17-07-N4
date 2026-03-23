import os

directories_to_scan = [
    r"c:\TTDN-17-07-N4\addons\nhan_su",
    r"c:\TTDN-17-07-N4\addons\cham_cong",
    r"c:\TTDN-17-07-N4\addons\tinh_luong"
]

for d in directories_to_scan:
    for root, dirs, files in os.walk(d):
        for file in files:
            if file.endswith('.xml'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()

                new_content = content
                
                # REVERT globally
                new_content = new_content.replace('"department_id"', '"phong_ban_id"')
                new_content = new_content.replace("'department_id'", "'phong_ban_id'")
                new_content = new_content.replace('"job_id"', '"chuc_vu_id"')
                new_content = new_content.replace("'job_id'", "'chuc_vu_id'")
                
                if file == "nhan_vien.xml":
                    # But for hr.employee views in nhan_vien.xml, we NEED department_id and job_id for the top level employee fields!
                    # I will carefully replace them ONLY when not inside <field name="lich_su_cong_tac...
                    # It's easier to just do:
                    new_content = new_content.replace('<field name="phong_ban_id" readonly="1"', '<field name="department_id" readonly="1"')
                    new_content = new_content.replace('<field name="chuc_vu_id" readonly="1"', '<field name="job_id" readonly="1"')
                    
                    new_content = new_content.replace('<field name="phong_ban_id" widget="badge" decoration-success="1"', '<field name="department_id" widget="badge" decoration-success="1"')
                    new_content = new_content.replace('<field name="chuc_vu_id" widget="badge" decoration-info="1"', '<field name="job_id" widget="badge" decoration-info="1"')
                    
                    new_content = new_content.replace('<field name="phong_ban_id"/>\n                    <field name="email"/>', '<field name="department_id"/>\n                    <field name="email"/>')
                    new_content = new_content.replace('<field name="chuc_vu_id"/>\n                    <field name="phong_ban_id"/>', '<field name="job_id"/>\n                    <field name="department_id"/>')
                    
                    new_content = new_content.replace('group_by\':\'phong_ban_id\'', 'group_by\':\'department_id\'')
                    new_content = new_content.replace('group_by\':\'chuc_vu_id\'', 'group_by\':\'job_id\'')

                    new_content = new_content.replace('<field name="phong_ban_id" type="row"', '<field name="department_id" type="row"')
                    
                    new_content = new_content.replace('<field name="phong_ban_id"/>\n                    <field name="trang_thai"/>\n                </graph>', '<field name="department_id"/>\n                    <field name="trang_thai"/>\n                </graph>')
                
                if new_content != content:
                    print(f"Reverted {filepath}")
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
