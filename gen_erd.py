import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import os

out = r'c:\TTDN-17-07-N4\docs'

fig, ax = plt.subplots(1, 1, figsize=(15, 10))
ax.set_xlim(0, 15)
ax.set_ylim(0, 10)
ax.axis('off')
fig.patch.set_facecolor('white')

ax.text(7.5, 9.5, 'SO DO QUAN HE THUC THE (ERD) - HE THONG ERP', ha='center', va='center',
        fontsize=18, fontweight='bold', color='#1a237e', family='Arial')

# Function to draw table
def draw_table(ax, x, y, w, h, title, fields, color_title='#1a237e'):
    # Header
    box_t = mpatches.Rectangle((x, y), w, 0.7, facecolor=color_title, edgecolor='#333', linewidth=1.5)
    ax.add_patch(box_t)
    ax.text(x + w/2, y + 0.35, title, ha='center', va='center', fontsize=12, fontweight='bold', color='white', family='Arial')
    
    # Body
    box_b = mpatches.Rectangle((x, y - h), w, h, facecolor='#f5f5f5', edgecolor='#333', linewidth=1.5)
    ax.add_patch(box_b)
    
    # Fields
    for i, field in enumerate(fields):
        ax.text(x + 0.2, y - 0.5 - (i*0.45), field, ha='left', va='center', fontsize=11, family='Consolas')

# Draw tables
# 1. hr.employee (Center)
t1_fields = ['PK  id (Int)', '    name (Char)', '    cccd_number (Char)', '    marital (Selection)', '    bank_account_id (M2o)']
draw_table(ax, 6, 7, 3.2, 2.5, 'hr.employee\n(Ho Sơ Nhan Vien)', t1_fields, '#1565c0')

# 2. hr.dependent (Top Left)
t2_fields = ['PK  id (Int)', 'FK  employee_id (M2o)', '    name (Char)', '    birth_date (Date)', '    auto_age (Int)']
draw_table(ax, 1.5, 9, 3.2, 2.5, 'hr.dependent\n(Nguoi Phu Thuoc)', t2_fields, '#0277bd')

# 3. hr.contract (Top Right)
t3_fields = ['PK  id (Int)', 'FK  employee_id (M2o)', '    wage (Float)', '    insurance_wage (Float)', '    state (Selection)']
draw_table(ax, 10.5, 9, 3.2, 2.5, 'hr.contract\n(Hop Dong LD)', t3_fields, '#00695c')

# 4. bang.cham.cong (Bottom Left)
t4_fields = ['PK  id (Int)', 'FK  employee_id (M2o)', '    check_in (Datetime)', '    check_out (Datetime)', '    late_minutes (Int)']
draw_table(ax, 2, 4.5, 3.4, 2.5, 'hr.attendance\n(Bang Cham Cong)', t4_fields, '#2e7d32')

# 5. bang.luong.thang (Bottom Right)
t5_fields = ['PK  id (Int)', 'FK  employee_id (M2o)', 'FK  contract_id (M2o)', '    net_wage (Float)', '    ai_comment (Text)']
draw_table(ax, 10, 5, 3.5, 2.5, 'hr.payslip.run\n(Bang Luong Tong)', t5_fields, '#e65100')

# 6. chi.tiet.luong (Far Bottom Right - Adjusted Y)
t6_fields = ['PK  id (Int)', 'FK  payslip_id (M2o)', '    name (Char)', '    code (Char)', '    amount (Float)']
draw_table(ax, 10, 1.5, 3.5, 2.5, 'hr.payslip.line\n(Chi Tiet Luong)', t6_fields, '#d84315')

# Symbol Lines
def draw_line(ax, x1, y1, x2, y2):
    ax.plot([x1, x2], [y1, y2], color='#555', linewidth=2.5, zorder=0)
    ax.text((x1+x2)/2 + 0.1, (y1+y2)/2 + 0.2, '1', color='#d32f2f', fontweight='bold', fontsize=12)
    ax.text((x1+x2)/2 - 0.2, (y1+y2)/2 - 0.2, 'N', color='#1565c0', fontweight='bold', fontsize=12)

# Employee to Dependent
draw_line(ax, 7.6, 7.7, 3.1, 6.5) # Employee top to Dependent bottom
# Employee to Contract
draw_line(ax, 7.6, 7.7, 12.1, 6.5) # Employee top to Contract bottom
# Employee to Attendance
draw_line(ax, 6, 5.75, 3.7, 4.5) # Emloyee bottom-left to Attendance top
# Employee to Payslip Run
draw_line(ax, 9.2, 5.75, 11.7, 5) # Employee bottom-right to Payslip Run top
# Payslip Run to Payslip Line
draw_line(ax, 11.75, 2.5, 11.75, 1.5) # Payslip Run bottom to Line top

# Notation box
box_n = mpatches.Rectangle((0.5, 0.5), 4.5, 1.5, facecolor='#eeeeee', edgecolor='#999', linewidth=1)
ax.add_patch(box_n)
ax.text(0.7, 1.6, 'GHI CHU MO HINH DLD (ODOO ORM):', fontweight='bold', fontsize=11, family='Arial')
ax.text(0.7, 1.1, 'PK : Khoa Chinh (Primary Key)\nFK : Khoa Ngoai (M2o - Many2one)\n1-N: Quan de Mot-Nhieu (One2many)', fontsize=11, family='Consolas')

plt.tight_layout()
fig.savefig(os.path.join(out, 'ERD_Database.png'), dpi=150, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close()

print("DONE FIX - ERD_Database.png")
