"""
Add 'name' field to all hr.employee records in sample_data.xml and demo.xml
by combining ho_ten_dem + ten, since hr.employee requires name NOT NULL.
"""
import re
import os

# map of ho_ten_dem + ten combinations from the XML data
NHAN_VIEN_NAMES = {
    'demo_nhan_vien_1': ('Nguyễn Văn', 'An'),
    'demo_nhan_vien_2': ('Trần Thị', 'Bình'),
    'demo_nhan_vien_3': ('Lê Hoàng', 'Cường'),
    'demo_nhan_vien_4': ('Phạm Thị', 'Dung'),
    'demo_nhan_vien_5': ('Hoàng Minh', 'Đức'),
    'demo_nhan_vien_6': ('Ngô Thị', 'Hoa'),
    'demo_nhan_vien_7': ('Đỗ Văn', 'Gia'),
    'demo_nhan_vien_8': ('Bùi Thị', 'Huệ'),
    'demo_nhan_vien_9': ('Vũ Văn', 'Hùng'),
    'demo_nhan_vien_10': ('Lý Thị', 'Lan'),
}

# Also demo.xml names (from the original demo.xml)
DEMO_NAMES = {
    'demo_nhan_vien_1': ('Nguyễn Văn', 'An'),
    'demo_nhan_vien_2': ('Trần Thị', 'Bình'),
    'demo_nhan_vien_3': ('Lê Hoàng', 'Cường'),
    'demo_nhan_vien_4': ('Phạm Thị', 'Dung'),
    'demo_nhan_vien_5': ('Hoàng Minh', 'Đức'),
}

def add_name_to_records(filepath, names_map):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    for rec_id, (ho_ten_dem, ten) in names_map.items():
        full_name = f"{ho_ten_dem} {ten}"
        # Add <field name="name">...</field> after the record id opening tag
        # Find: <record id="demo_nhan_vien_X" model="hr.employee">
        pattern = rf'(<record id="{rec_id}" model="hr\.employee">)'
        replacement = rf'\1\n            <field name="name">{full_name}</field>'
        new_content = re.sub(pattern, replacement, content)
        if new_content != content:
            print(f"  Added name '{full_name}' to {rec_id}")
            content = new_content
        else:
            print(f"  WARN: Could not find/update {rec_id}")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

sample_file = r"c:\TTDN-17-07-N4\addons\nhan_su\data\sample_data.xml"
demo_file = r"c:\TTDN-17-07-N4\addons\nhan_su\demo\demo.xml"

print("=== Fixing sample_data.xml ===")
add_name_to_records(sample_file, NHAN_VIEN_NAMES)

print("\n=== Fixing demo.xml ===")
if os.path.exists(demo_file):
    add_name_to_records(demo_file, DEMO_NAMES)

print("\nDone!")
