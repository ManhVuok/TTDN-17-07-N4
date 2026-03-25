import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import os

out = r'c:\TTDN-17-07-N4\docs'

# ============ 1. SO DO TO CHUC ============
fig, ax = plt.subplots(1, 1, figsize=(12, 7))
ax.set_xlim(0, 12)
ax.set_ylim(0, 7)
ax.axis('off')
fig.patch.set_facecolor('white')

def draw_box(ax, x, y, w, h, text, color, fontsize=11, textcolor='white'):
    box = FancyBboxPatch((x - w/2, y - h/2), w, h,
                         boxstyle="round,pad=0.15", facecolor=color, edgecolor='#333', linewidth=1.5)
    ax.add_patch(box)
    ax.text(x, y, text, ha='center', va='center', fontsize=fontsize,
            fontweight='bold', color=textcolor, family='Arial')

def draw_line(ax, x1, y1, x2, y2):
    ax.plot([x1, x2], [y1, y2], color='#555', linewidth=1.5, zorder=0)

# Title
ax.text(6, 6.5, 'SO DO TO CHUC - CONG TY DNU-SOFT', ha='center', va='center',
        fontsize=16, fontweight='bold', color='#1a237e', family='Arial')

# Level 1
draw_box(ax, 6, 5.5, 3.5, 0.7, 'BAN GIAM DOC\n(Board of Directors)', '#1a237e')

# Lines to level 2
draw_line(ax, 6, 5.15, 2.5, 4.2)
draw_line(ax, 6, 5.15, 6, 4.2)
draw_line(ax, 6, 5.15, 9.5, 4.2)

# Level 2
draw_box(ax, 2.5, 3.8, 3, 0.7, 'PHONG HC - NHAN SU\n(HR & Admin)', '#2e7d32')
draw_box(ax, 6, 3.8, 3, 0.7, 'PHONG KE TOAN - TAI CHINH\n(Accounting)', '#e65100')
draw_box(ax, 9.5, 3.8, 3, 0.7, 'KHOI KY THUAT\n(Engineering)', '#4a148c')

# Lines to level 3
draw_line(ax, 9.5, 3.45, 8, 2.7)
draw_line(ax, 9.5, 3.45, 9.5, 2.7)
draw_line(ax, 9.5, 3.45, 11, 2.7)

# Level 3
draw_box(ax, 8, 2.3, 1.8, 0.6, 'Dev Team', '#7b1fa2')
draw_box(ax, 9.5, 2.3, 1.8, 0.6, 'Tester Team', '#7b1fa2')
draw_box(ax, 11, 2.3, 1.8, 0.6, 'BA Team', '#7b1fa2')

# Notes
ax.text(2.5, 2.8, 'Quan ly ho so, hop dong\nModule: nhan_su', ha='center',
        fontsize=9, color='#2e7d32', style='italic', family='Arial')
ax.text(6, 2.8, 'Tra luong, thue, bao hiem\nModule: tinh_luong', ha='center',
        fontsize=9, color='#e65100', style='italic', family='Arial')

plt.tight_layout()
fig.savefig(os.path.join(out, 'SoDoToChuc.png'), dpi=150, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close()

# ============ 2. KIEN TRUC MODULE ============
fig, ax = plt.subplots(1, 1, figsize=(13, 8))
ax.set_xlim(0, 13)
ax.set_ylim(0, 8)
ax.axis('off')
fig.patch.set_facecolor('white')

ax.text(6.5, 7.5, 'KIEN TRUC HE THONG - 3 MODULE', ha='center', va='center',
        fontsize=16, fontweight='bold', color='#1a237e', family='Arial')

# Module boxes
draw_box(ax, 6.5, 6, 4, 1, 'MODULE NHAN SU (nhan_su)\nhr.employee - Trai tim du lieu', '#1a237e', 12)
draw_box(ax, 3, 3.5, 4.2, 1, 'MODULE CHAM CONG (cham_cong)\nCa lam, Check-in/out, Don tu', '#2e7d32', 12)
draw_box(ax, 10, 3.5, 4.2, 1, 'MODULE TINH LUONG (tinh_luong)\nBang luong, BH, Thue, Net', '#e65100', 12)

# Arrows
ax.annotate('', xy=(4, 4.05), xytext=(5.5, 5.45),
            arrowprops=dict(arrowstyle='->', color='#1a237e', lw=2))
ax.text(4.2, 4.9, 'Ho so NV', fontsize=10, color='#1a237e', fontweight='bold',
        rotation=30, family='Arial')

ax.annotate('', xy=(9, 4.05), xytext=(7.5, 5.45),
            arrowprops=dict(arrowstyle='->', color='#1a237e', lw=2))
ax.text(8.3, 4.9, 'Ho so NV', fontsize=10, color='#1a237e', fontweight='bold',
        rotation=-30, family='Arial')

ax.annotate('', xy=(7.85, 3.5), xytext=(5.15, 3.5),
            arrowprops=dict(arrowstyle='->', color='#388e3c', lw=2.5))
ax.text(6.5, 3.85, 'Du lieu cham cong', fontsize=10, color='#388e3c',
        fontweight='bold', ha='center', family='Arial')

# External APIs
def draw_cloud(ax, x, y, text, color):
    box = FancyBboxPatch((x - 1.3, y - 0.3), 2.6, 0.6,
                         boxstyle="round,pad=0.2", facecolor=color, edgecolor='#666',
                         linewidth=1, alpha=0.85)
    ax.add_patch(box)
    ax.text(x, y, text, ha='center', va='center', fontsize=9,
            fontweight='bold', color='white', family='Arial')

draw_cloud(ax, 1.5, 6.5, 'Google Gemini AI', '#8e24aa')
draw_cloud(ax, 11.5, 6.5, 'Telegram Bot API', '#0088cc')
draw_cloud(ax, 11.5, 2, 'Email SMTP', '#d32f2f')

ax.annotate('', xy=(4.45, 6.2), xytext=(2.8, 6.4),
            arrowprops=dict(arrowstyle='->', color='#8e24aa', lw=1.5, ls='--'))
ax.annotate('', xy=(8.55, 6.2), xytext=(10.2, 6.4),
            arrowprops=dict(arrowstyle='->', color='#0088cc', lw=1.5, ls='--'))
ax.annotate('', xy=(11.5, 2.95), xytext=(11.5, 2.35),
            arrowprops=dict(arrowstyle='->', color='#d32f2f', lw=1.5, ls='--'))

# DB
draw_box(ax, 6.5, 1.5, 4, 0.7, 'PostgreSQL Database (Docker)', '#37474f', 11)
draw_line(ax, 3, 2.95, 5.5, 1.9)
draw_line(ax, 10, 2.95, 7.5, 1.9)

plt.tight_layout()
fig.savefig(os.path.join(out, 'KienTrucModule.png'), dpi=150, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close()

# ============ 3. LUONG NGHIEP VU ============
fig, ax = plt.subplots(1, 1, figsize=(14, 6))
ax.set_xlim(0, 14)
ax.set_ylim(0, 6)
ax.axis('off')
fig.patch.set_facecolor('white')

ax.text(7, 5.5, 'LUONG NGHIEP VU END-TO-END: CHAM CONG - TINH LUONG', ha='center',
        fontsize=14, fontweight='bold', color='#1a237e', family='Arial')

steps = [
    (1.5, 4.2, '1', 'NV nop don\nxin nghi', '#1565c0'),
    (3.5, 4.2, '2', 'Telegram\nthong bao QL', '#0088cc'),
    (5.5, 4.2, '3', 'Quan ly\nphe duyet', '#1565c0'),
    (7.5, 4.2, '4', 'Tu dong tao\nVang co phep', '#2e7d32'),
    (1.5, 1.8, '5', 'HR tao\nBang luong', '#1565c0'),
    (4.5, 1.8, '6', 'Tinh tu dong\nBH+Thue+Phat\n=> Net', '#2e7d32'),
    (8, 1.8, '7', 'AI Gemini\ndanh gia\nhieu suat', '#8e24aa'),
    (11.5, 1.8, '8', 'Gui Email\nPhieu luong PDF\n+ nhan xet AI', '#d32f2f'),
]

for x, y, num, text, color in steps:
    circle = plt.Circle((x, y + 0.5), 0.3, color=color, zorder=3)
    ax.add_patch(circle)
    ax.text(x, y + 0.5, num, ha='center', va='center', fontsize=13,
            fontweight='bold', color='white', family='Arial', zorder=4)
    ax.text(x, y - 0.15, text, ha='center', va='center', fontsize=9,
            color='#333', family='Arial', fontweight='bold')

# Arrows row 1
for i in range(3):
    x1 = steps[i][0] + 0.4
    x2 = steps[i+1][0] - 0.4
    y = 4.7
    ax.annotate('', xy=(x2, y), xytext=(x1, y),
                arrowprops=dict(arrowstyle='->', color='#555', lw=1.8))

# Arrow down from step 4 to step 5
ax.annotate('', xy=(1.5, 2.65), xytext=(7.5, 3.85),
            arrowprops=dict(arrowstyle='->', color='#555', lw=1.8,
                           connectionstyle='arc3,rad=0.3'))

# Arrows row 2
pairs = [(4, 5), (5, 6), (6, 7)]
for i, j in pairs:
    x1 = steps[i][0] + 0.5
    x2 = steps[j][0] - 0.5
    y = 2.3
    ax.annotate('', xy=(x2, y), xytext=(x1, y),
                arrowprops=dict(arrowstyle='->', color='#555', lw=1.8))

# Labels for integration levels
ax.text(7.5, 3.55, 'Event-driven', ha='center', fontsize=8, color='#2e7d32',
        style='italic', family='Arial',
        bbox=dict(boxstyle='round,pad=0.2', facecolor='#e8f5e9', edgecolor='#2e7d32'))
ax.text(8, 1.15, 'AI/LLM', ha='center', fontsize=8, color='#8e24aa',
        style='italic', family='Arial',
        bbox=dict(boxstyle='round,pad=0.2', facecolor='#f3e5f5', edgecolor='#8e24aa'))
ax.text(3.5, 3.55, 'External API', ha='center', fontsize=8, color='#0088cc',
        style='italic', family='Arial',
        bbox=dict(boxstyle='round,pad=0.2', facecolor='#e3f2fd', edgecolor='#0088cc'))

plt.tight_layout()
fig.savefig(os.path.join(out, 'LuongNghiepVu.png'), dpi=150, bbox_inches='tight',
            facecolor='white', edgecolor='none')
plt.close()

print("DONE - 3 so do da tao tai docs/")
