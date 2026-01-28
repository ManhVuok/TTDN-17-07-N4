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

### 3.1. Quản lý nhân sự
    Quản lý hồ sơ nhân viên đầy đủ: thông tin cá nhân, liên hệ, ngân hàng, tình trạng làm việc
    
    Quản lý phòng ban, chức vụ theo mô hình phân cấp
    
    Theo dõi lịch sử công tác, điều chuyển, thăng chức
    
    Quản lý bằng cấp, chứng chỉ của nhân viên
    
    Dashboard thống kê nhân sự và xuất báo cáo PDF
### 3.2. Quản lý Chấm công & Ca làm việc

    Tổ chức đợt đăng ký ca làm theo tháng/năm
    
    Đăng ký ca làm việc theo ngày cho từng nhân viên
    
    Ghi nhận giờ vào – giờ ra, tự động tính đi muộn/về sớm
    
    Quản lý ca làm việc (hành chính, ca sáng, chiều, đêm) và hệ số lương
    
    Xem chấm công trực quan bằng Calendar và Dashboard

### 3.3. Quản lý Đơn từ & Nghỉ phép

    Quản lý các loại đơn: nghỉ phép, đi muộn, về sớm, công tác, báo ốm
    
    Quy trình duyệt đơn rõ ràng: Nháp → Chờ duyệt → Đã duyệt/Từ chối
    
    Quản lý phép năm, phép cộng thêm, phép chuyển năm
    
    Tự động tính số ngày đã nghỉ và số ngày còn lại
    
    Cảnh báo nhân viên sắp hết hoặc hết phép

### 3.4. Tính lương & Làm thêm giờ

    Quản lý hợp đồng lao động và mức lương theo từng nhân viên
    
    Tính lương theo tháng dựa trên chấm công, ca làm và tăng ca
    
    Tính lương làm thêm giờ theo ngày thường, cuối tuần, ngày lễ
    
    Hỗ trợ cấu hình phụ cấp, khấu trừ, bảo hiểm và thuế TNCN
    
    Theo dõi chi tiết bảng lương và phiếu lương (Payslip)

### 3.5. Tính lương & Làm thêm giờ
    Dashboard tổng hợp: nhân sự, chấm công, quỹ lương theo thời gian
    
    Biểu đồ phân tích theo phòng ban, chức vụ, thu nhập
    
    Xuất phiếu lương và báo cáo hệ thống dưới dạng PDF
    
    Tích hợp AI Assistant hỗ trợ tra cứu và hỏi đáp dữ liệu hệ thống
    
    Lưu lịch sử chat AI phục vụ quản trị và phân tích

## ⚙️ 4. Cài đặt

### 4.1. Cài đặt công cụ, môi trường và các thư viện cần thiết

#### 4.1.1. Tải project.
```
git clone https://github.com/duchoan25/TTDN-16-01-N14
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

## 📝 5. License

- 👨‍🎓 **Sinh viên thực hiện**: Nguyễn Đức Hoàn
- 🎓 **Khoa**: Công nghệ thông tin – Đại học Đại Nam
- 📧 **Email**: nguyenduchoan2050@gmail.com

---

    
