import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

out = r'c:\TTDN-17-07-N4\docs\ERD_Database.png'

fig, ax = plt.subplots(1, 1, figsize=(16, 14))
ax.set_xlim(0, 16)
ax.set_ylim(0, 14)
ax.axis('off')
fig.patch.set_facecolor('white')

ax.text(8, 13.2, 'SO DO QUAN HE THUC THE (ERD) - HE THONG ERP', ha='center', va='center',
        fontsize=22, fontweight='bold', color='#1a237e', family='Arial')

def draw_table(ax, x, y, w, h, title, fields, color_title='#1a237e'):
    # Header
    box_t = mpatches.Rectangle((x, y), w, 0.8, facecolor=color_title, edgecolor='#333', linewidth=1.5)
    ax.add_patch(box_t)
    ax.text(x + w/2, y + 0.4, title, ha='center', va='center', fontsize=13, fontweight='bold', color='white', family='Arial')
    
    # Body
    box_b = mpatches.Rectangle((x, y - h), w, h, facecolor='#f5f5f5', edgecolor='#333', linewidth=1.5)
    ax.add_patch(box_b)
    
    # Fields
    for i, field in enumerate(fields):
        ax.text(x + 0.2, y - 0.5 - (i*0.5), field, ha='left', va='center', fontsize=12, family='Consolas')

# Draw tables
t1 = ['PK  id (Int)', '    name (Char)', '    cccd_number (Char)', '    marital (Selection)', '    bank_account_id (M2o)']
draw_table(ax, 6.25, 9, 3.5, 2.8, 'hr.employee\n(Ho So Nhan Vien)', t1, '#1565c0')

t2 = ['PK  id (Int)', 'FK  employee_id (M2o)', '    name (Char)', '    birth_date (Date)', '    auto_age (Int)']
draw_table(ax, 1, 12, 3.6, 2.8, 'hr.dependent\n(Nguoi Phu Thuoc)', t2, '#0277bd')

t3 = ['PK  id (Int)', 'FK  employee_id (M2o)', '    wage (Float)', '    insurance_wage (Float)', '    state (Selection)']
draw_table(ax, 11.5, 12, 3.6, 2.8, 'hr.contract\n(Hop Dong LD)', t3, '#00695c')

t4 = ['PK  id (Int)', 'FK  employee_id (M2o)', '    check_in (Datetime)', '    check_out (Datetime)', '    late_minutes (Int)']
draw_table(ax, 1, 6, 3.6, 2.8, 'hr.attendance\n(Bang Cham Cong)', t4, '#2e7d32')

t5 = ['PK  id (Int)', 'FK  employee_id (M2o)', 'FK  contract_id (M2o)', '    net_wage (Float)', '    ai_comment (Text)']
draw_table(ax, 11.5, 7.5, 3.6, 2.8, 'hr.payslip.run\n(Bang Luong Tong)', t5, '#e65100')

t6 = ['PK  id (Int)', 'FK  payslip_id (M2o)', '    name (Char)', '    code (Char)', '    amount (Float)']
draw_table(ax, 11.5, 3.5, 3.6, 2.8, 'hr.payslip.line\n(Chi Tiet Luong)', t6, '#d84315')

def draw_line(ax, x1, y1, x2, y2, l1='1', l2='N'):
    ax.plot([x1, x2], [y1, y2], color='#444', linewidth=2.5, zorder=0)
    ax.text(x1 + (x2-x1)*0.2, y1 + (y2-y1)*0.2 + 0.3, l1, color='#d32f2f', fontweight='bold', fontsize=14)
    ax.text(x1 + (x2-x1)*0.8 - 0.3, y1 + (y2-y1)*0.8 - 0.3, l2, color='#1565c0', fontweight='bold', fontsize=14)

# Relations center points
# Employee: Left(6.25, 7.6), Right(9.75, 7.6)
# Dependent: Right(4.6, 10.6)
draw_line(ax, 6.25, 8.5, 4.6, 10.6)

# Contract: Left(11.5, 10.6)
draw_line(ax, 9.75, 8.5, 11.5, 10.6)

# Attendance: Right(4.6, 4.6)
draw_line(ax, 6.25, 6.6, 4.6, 4.6)

# Payslip Run: Left(11.5, 6.1)
draw_line(ax, 9.75, 6.6, 11.5, 6.1)

# Payslip Line: Top(13.3, 4.3)
# Payslip Run: Bottom(13.3, 4.7)
ax.plot([13.3, 13.3], [4.7, 4.3], color='#444', linewidth=2.5, zorder=0)
ax.text(13.5, 4.5, '1', color='#d32f2f', fontweight='bold', fontsize=14)
ax.text(13.5, 4.0, 'N', color='#1565c0', fontweight='bold', fontsize=14)

# Notation box
box_n = mpatches.Rectangle((1, 0.5), 6.5, 2.2, facecolor='#eeeeee', edgecolor='#999', linewidth=1.5)
ax.add_patch(box_n)
ax.text(1.2, 2.3, 'GHI CHU MO HINH DLD (ODOO ORM):', fontweight='bold', fontsize=13, family='Arial')
ax.text(1.2, 1.4, 'PK : Khoa Chinh (Primary Key)\nFK : Khoa Ngoai (M2o - Many2one)\n1-N: Quan he Mot-Nhieu (One2many)', fontsize=13, family='Consolas')

plt.tight_layout()
fig.savefig(out, dpi=150, bbox_inches='tight', facecolor='white', edgecolor='none')
plt.close()
print('DONE ERD FINAL')
