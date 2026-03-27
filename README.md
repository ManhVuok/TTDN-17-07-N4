<h2 align="center">
    <a href="https://dainam.edu.vn/vi/khoa-cong-nghe-thong-tin">
    🎓 Faculty of Information Technology (DaiNam University)
    </a>
</h2>
<h2 align="center">
    Hệ thống quản lý nhân sự, chấm công và tính lương trên nền tảng Odoo 15
</h2>
<div align="center">
    <p align="center">
        <img src="docs/logo/aiotlab_logo.png" alt="AIoTLab Logo" width="170"/>
        <img src="docs/logo/fitdnu_logo.png" alt="AIoTLab Logo" width="180"/>
        <img src="docs/logo/dnu_logo.png" alt="DaiNam University Logo" width="200"/>
    </p>

[![AIoTLab](https://img.shields.io/badge/AIoTLab-green?style=for-the-badge)](https://www.facebook.com/DNUAIoTLab)
[![Faculty of Information Technology](https://img.shields.io/badge/Faculty%20of%20Information%20Technology-blue?style=for-the-badge)](https://dainam.edu.vn/vi/khoa-cong-nghe-thong-tin)
[![DaiNam University](https://img.shields.io/badge/DaiNam%20University-orange?style=for-the-badge)](https://dainam.edu.vn)

</div>

## 📖 1. Giới thiệu
Hệ thống Quản lý Chấm công – Tính lương được xây dựng nhằm hỗ trợ doanh nghiệp quản lý nhân sự, theo dõi thời gian làm việc và tính lương cho người lao động một cách chính xác, minh bạch và hiệu quả. Hệ thống giúp thay thế các phương pháp quản lý thủ công, giảm sai sót và tiết kiệm thời gian cho bộ phận nhân sự.

Hệ thống được phát triển trên nền tảng Odoo ERP, gồm ba module chính: Nhân sự, Chấm công và Tính lương. Module Nhân sự quản lý hồ sơ nhân viên, phòng ban, chức vụ và dữ liệu nền. Module Chấm công ghi nhận ca làm việc, giờ vào – ra, nghỉ phép, đơn từ và tăng ca. Module Tính lương tự động tính bảng lương và phiếu lương dựa trên dữ liệu chấm công, hợp đồng lao động, phụ cấp, khấu trừ và thuế.

Với kiến trúc module hóa và khả năng mở rộng cao, hệ thống phù hợp với các doanh nghiệp vừa và nhỏ, đồng thời là nền tảng cho việc phát triển và tích hợp các chức năng nâng cao trong tương lai.

## 🔧 2. Các công nghệ được sử dụng
<div align="center">

### Hệ điều hành
[![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)](https://ubuntu.com/)
### Công nghệ chính
[![Odoo](https://img.shields.io/badge/Odoo-714B67?style=for-the-badge&logo=odoo&logoColor=white)](https://www.odoo.com/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![XML](https://img.shields.io/badge/XML-FF6600?style=for-the-badge&logo=codeforces&logoColor=white)](https://www.w3.org/XML/)
### Cơ sở dữ liệu
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
</div>

## 🚀 3. Các chức năng chính

Hệ thống cung cấp các chức năng quản lý nghiệp vụ cốt lõi của doanh nghiệp, được triển khai dưới dạng các module độc lập nhưng có khả năng liên kết và chia sẻ dữ liệu với nhau.

### 3.1. Quản lý Nhân sự (Mức 1 - Cơ bản)
    Số hóa hồ sơ nhân viên tập trung: Thông tin cá nhân, liên hệ, ngân hàng, ảnh chân dung.
    
    Quản lý Hợp đồng lao động: Lưu trữ lương cơ bản, lương bảo hiểm, phụ cấp và số người phụ thuộc làm dữ liệu gốc chuẩn xác.
    
    Phân quyền theo mô hình phân cấp: Quản lý phòng ban, chức danh và luồng phê duyệt đơn từ.
    
    Theo dõi chi tiết lịch sử công tác, quá trình điều chuyển, thăng chức của nhân viên.
### 3.2. Quản lý Chấm công & Ca làm việc (Mức 2 - Tự động hóa)
    Quản lý đa dạng ca làm việc: Hành chính, ca gãy, ca đêm với hệ số lương và khung giờ khác nhau.
    
    Tự động hóa tính toán vi phạm: Hệ thống tự đối soát giờ quẹt thẻ thực tế với ca làm để tính chính xác đến từng phút đi muộn/về sớm.
    
    Cơ chế nạp dữ liệu thông minh: Hỗ trợ mô phỏng hàng nghìn bản ghi chấm công từ XML nhằm đảm bảo tính thực tế khi demo.
    
    Dashboard Chấm công hiện đại: Trực quan hóa dữ liệu hiển thị dưới dạng Calendar, Graph và Pivot view thông qua Odoo.

### 3.3. Quản lý Đơn từ & Nghỉ phép (Mức 2 - Tự động hóa)
    Quy trình phê duyệt khép kín: Nháp → Chờ duyệt → Đã duyệt/Từ chối, hỗ trợ nhiều cấp bậc quản lý.
    
    Tự động hóa luồng dữ liệu (Event-driven): Tự động ghi nhận "Vắng có phép" vào Bảng chấm công ngay sau khi đơn được phê duyệt.
    
    Quản lý quỹ phép thông minh: Hệ thống tự cộng dồn phép tồn, tính phép năm và cảnh báo nhân viên sắp hết phép.

### 3.4. Tính lương & Khấu trừ (Mức 2 - Tự động hóa)
    Cơ chế "Một nút bấm": Tự động vét dữ liệu chấm công sang Bảng lương, giảm tải 90% công việc nhập liệu thủ công.
    
    Tự động hóa tính toán phức tạp: Tính bảo hiểm (BHXH, BHYT, BHTN), Thuế TNCN biểu thuế lũy tiến từng phần và tiền phạt chuyên cần chuẩn 100%.
    
    Linh hoạt cấu hình: Cho phép điều chỉnh mức giảm trừ gia cảnh, ngưỡng phạt đi muộn và các loại phụ cấp đặc thù.

### 3.5. Trợ lý AI Assistant & Tích hợp (Nâng cao)
    Trợ lý ảo AI Gemini 2.0: Hỗ trợ nhân viên tra cứu nội quy, chính sách và giải đáp thắc mắc 24/7 qua khung chat trực tuyến.
    
    Tự động hóa thông báo: Gửi tin nhắn phê duyệt bảng lương và đơn từ qua Telegram Bot API tới quản lý.
    
    AI Đánh giá hiệu suất: Sử dụng LLM để phân tích dữ liệu bảng lương và đưa ra lời nhận xét cá nhân hóa trên từng phiếu lương.
    
    Gửi phiếu lương tự động: Hệ thống tự động gửi email phiếu lương kèm nhận xét của AI tới hòm thư cá nhân của nhân viên sau khi chốt lương.
    
    Dashboard B.I chuyên sâu: Biểu đồ trực quan hóa dữ liệu nhân sự, biến động quỹ lương và hiệu suất làm việc.

## ⚙️ 4. Cài đặt

### 4.1. Cài đặt công cụ, môi trường và các thư viện cần thiết

#### 4.1.1. Tải project.
```
git clone https://github.com/ManhVuok/TTDN-17-07-N4.git
git checkout 
```
#### 4.1.2. Cài đặt các thư viện cần thiết
Người sử dụng thực thi các lệnh sau đề cài đặt các thư viện cần thiết

```
sudo apt-get install libxml2-dev libxslt-dev libldap2-dev libsasl2-dev libssl-dev python3.10-distutils python3.10-dev build-essential libssl-dev libffi-dev zlib1g-dev python3.10-venv libpq-dev
```
#### 4.1.3. Khởi tạo môi trường ảo.
- Khởi tạo môi trường ảo
```
python3.10 -m venv ./venv
```
- Thay đổi trình thông dịch sang môi trường ảo
```
source venv/bin/activate
```
- Chạy requirements.txt để cài đặt tiếp các thư viện được yêu cầu
```
pip3 install -r requirements.txt
```
### 4.2. Setup database

Khởi tạo database trên docker bằng việc thực thi file dockercompose.yml.
```
sudo docker-compose up -d
```
### 4.3. Setup tham số chạy cho hệ thống
Tạo tệp **odoo.conf** có nội dung như sau:
```
[options]
addons_path = addons
db_host = localhost
db_password = odoo
db_user = odoo
db_port = 5431
xmlrpc_port = 8069
```
Có thể kế thừa từ file **odoo.conf.template**
### 4.4. Chạy hệ thống và cài đặt các ứng dụng cần thiết
Lệnh chạy
```
python3 odoo-bin.py -c odoo.conf -u all
```
Người sử dụng truy cập theo đường dẫn _http://localhost:8069/_ để đăng nhập vào hệ thống.

## 📈 5. Luồng Nghiệp Vụ Chấm Công - Tính Lương (End-to-End)

Quá trình "Chấm Công - Tính Lương" được thực hiện với các bước chính và bao gồm điểm tích hợp trọng tâm giữa các module HRM, Chấm Công, Tính Lương cùng với các sự kiện tự động hoá/API. Sơ đồ chi tiết được đánh kèm tại `docs/businessflow/Nhom01_BusinessFlow_ChamCong_TinhLuong.png`.

1. **Nhân viên** tạo *Đơn xin nghỉ* nộp lên hệ thống.
2. **Hệ thống** gọi External API (Telegram) để nổ tin nhắn thông báo có đơn mới đến Quản lý **[Tích hợp Mức 3: External API]**.
3. **Quản lý/HR** nhận được thông báo, truy cập Odoo để *Phê duyệt Đơn từ*.
4. **Hệ thống** tự động dựa vào sự kiện Đơn từ được duyệt (Event-driven): Tự động tạo/cập nhật *Bảng chấm công* của nhân viên trong ngày nghỉ đó với trạng thái "Vắng có phép" **[Tích hợp Mức 2: Tự động hóa tạo Record]**.
5. Đầu tháng sau, **HR** tạo Bảng lương. **Hệ thống** tự dùng data thực tế từ *Hồ sơ nhân sự* và *Chấm công* để ra thu nhập (Net, Gross, Thuế).
6. Sau khi chốt & Phê duyệt Lương, **HR** bấm nút xuất Payslip & Đánh giá AI.
7. **Hệ thống** gửi Input (Số phút đi muộn, Ngày vắng, Lương net) tới Google Gemini API **[Tích hợp Mức 3: AI/LLM]**.
8. **AI** đóng vai trò tự động trả về Output là 4 câu nhận xét/khuyên nhủ nhân viên. Cuối cùng Hệ thống sinh file Payslip PDF gửi Email kèm lời nhận xét của AI cho nhân viên!

## 📝 6. License

- 👨‍🎓 **Sinh viên thực hiện**: Nguyễn Văn Thuyết, Vũ Duy Mạnh
- 🎓 **Khoa**: Công nghệ thông tin – Đại học Đại Nam
- 📧 **Email**: thuyet1230@gmail.com, vu2873726@gmail.com

## 7. Nguồn tham khảo

Dự án được xây dựng và tham khảo dựa trên các hệ thống từ khóa học trước (Khóa K16) nhằm tối ưu hóa luồng nghiệp vụ và kiến trúc module:

- **Repository tham khảo chính**: `TTDN-16-06-N13` (Lớp CNTT 16-06 - Nhóm 13)
- **Nền tảng học phần**: Business-Internship (FIT-DNU)

---
