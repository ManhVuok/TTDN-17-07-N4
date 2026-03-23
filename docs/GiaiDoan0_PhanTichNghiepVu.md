# GIAI ĐOẠN 0: PHÂN TÍCH NGHIỆP VỤ & THIẾT KẾ KIẾN TRÚC

**Dự án:** Hệ thống quản lý nhân sự, chấm công và tính lương trên nền tảng Odoo 15
**Nhóm thực hiện:** Nhóm 02 (Nguyễn Văn Thuyết, Vũ Duy Mạnh)

---

## 1. Hồ sơ doanh nghiệp giả định
Dựa trên đặc thù của chức năng phân tích (Quản trị Nhân sự, Chấm công, Tính lương), nhóm quyết định chọn **Mô hình B: Công ty Dịch vụ/Dự án** làm bối cảnh chính để xây dựng mock-data và luồng hệ thống.

*   **Tên công ty:** Công ty Cổ phần Giải pháp Công nghệ DNU-Soft
*   **Lĩnh vực hoạt động:** Dịch vụ Công nghệ thông tin, lập trình gia công (Outsourcing) và tư vấn triển khai phần mềm. Bán chất xám và "Giờ làm việc" (Man-hour).
*   **Đặc thù nghiệp vụ:** Nhân viên làm việc theo ca hành chính/ca linh hoạt, có chính sách phạt đi muộn/về sớm tự động, yêu cầu quản lý sát sao thời gian làm việc để tối ưu hóa chi phí dự án.

**Sơ đồ tổ chức cơ bản:**
*   Ban Giám đốc (Board of Directors)
    *   Phòng Hành chính - Nhân sự (HR & Admin): Quản lý tuyển dụng, hồ sơ, hợp đồng.
    *   Phòng Kế toán - Tài chính (Accounting): Quản lý dòng tiền, trả lương, thuế.
    *   Khối Kỹ thuật (Engineering/Delivery): Bao gồm các đội ngũ Dev, Tester, BA.

---

## 2. Bảng phân rã chức năng (The Matrix)
Để tránh tình trạng "lẩu thập cẩm" và vi phạm nguyên tắc "Bất khả xâm phạm" trong hệ thống ERP, quyền hạn và chức năng được phân nhỏ rạch ròi cho 3 Module như sau:

| Hạng mục | Module NHÂN SỰ (HR) | Module CHẤM CÔNG (Attendance & Leave) | Module TÍNH LƯƠNG (Payroll) |
| :--- | :--- | :--- | :--- |
| **Vai trò** | **"Người quản người"** | **"Người quản thời gian"** | **"Người quản tiền"** |
| **Chức năng chính** | - Quản lý Hồ sơ nhân viên (Thông tin, bảo hiểm, liên hệ).<br>- Quản lý Cơ cấu tổ chức (Phòng ban, Chức vụ).<br>- Quản lý Hợp đồng lao động (Lương cơ bản, phụ cấp). | - Quản lý và cấu hình Ca làm việc.<br>- Ghi nhận dữ liệu check-in/check-out.<br>- Quản lý Đơn từ (Nghỉ phép, CT, OT).<br>- Tự động tính toán số phút đi muộn/về sớm. | - Kế thừa dữ liệu Chấm công và Hợp đồng để tạo Bảng lương.<br>- Tính toán Bảo hiểm bắt buộc, Thuế TNCN.<br>- Tính lương Thực lãnh (Net Salary).<br>- Triển khai gửi phiếu lương (Payslip). |
| **Đầu ra (Output)** | Hồ sơ nhân viên hoàn chỉnh, Hợp đồng lao động có hiệu lực | Bảng tổng hợp công tháng chính xác, chi tiết tình trạng đi làm | Bảng lương hàng tháng đã duyệt, Bút toán chi phí nhân sự |
| **CẤM KỴ** (Hard Boundaries) | 🚫 **Không được sửa Bảng lương** đã được Kế toán chốt duyệt. 🚫 **Không can thiệp** vào quá trình chấm công hàng ngày. | 🚫 **Không được sửa thông tin Lương cơ bản** trong Hợp đồng lao động. 🚫 **Không được thay đổi Hệ số đóng bảo hiểm**. | 🚫 **Không được tự ý điều chỉnh Giờ công** của nhân viên. 🚫 **Không được tự thêm tên nhân sự** nếu Bộ phận HR chưa tạo hồ sơ. |

---

## 3. Kịch bản nghiệp vụ (User Scenario)
_Kịch bản E2E kết nối cả 3 Module dưới dạng câu chuyện thực tế tại DNU-Soft:_

**"Quy trình Onboarding đến trả lương không chạm"**

Sáng kỳ trả lương cuối tháng, **nhân viên Nguyễn Văn A** (Khối Kỹ thuật) đăng nhập ứng dụng xem tình hình công tháng qua của mình. Lúc này, A nhớ ra tuần thứ 2 mình có nộp đơn xin nghỉ phép 1 ngày thông qua Module Chấm Công và đã được Manager phê duyệt ngay trên ứng dụng di động. Sau khi đơn được duyệt, hệ thống đã **tự động (event-driven)** ghi nhận "Vắng có phép" (nghỉ hưởng nguyên lương) vào bảng tổng hợp công của anh A tháng đó. Đồng thời, những hôm A đi muộn tổng cộng 45 phút cũng được máy chấm công ghi nhận chính xác vào cơ sở dữ liệu.

Đến ngày mùng 2 tháng kế tiếp, **chị B (Phòng Hành chính - Nhân sự)** không cần phải cầm tệp Excel chạy qua cho Kế toán nữa. Chị chỉ việc kiểm tra chắc chắn các HĐLĐ trên hệ thống đều còn hiệu lực.
Ngay lúc đó, **anh C (Phòng Kế toán)** đăng nhập vào hệ thống, mở Module Tính Lương và chọn "Tạo Bảng lương tháng". Hệ thống lập tức vét dữ liệu _(Dữ liệu cơ bản từ module nhân sự + Số giờ công/phút đi muộn/nghỉ phép từ module chấm công)_ và chạy luồng tự động để tính ra chính xác mức trích nộp bảo hiểm, thuế TNCN, phạt đi muộn và cho ra Lương Net cuối cùng của A.

Sau khi Bảng lương được Giám đốc C-Level nhấn **Approve (Phê duyệt)**, hệ thống lập tức **gọi AI Gemini** để dựa theo số công đi muộn của anh A mà sinh ra một lời nhắc nhở/nhận xét được cá nhân hóa hoàn toàn. Cuối cùng, 1 file PDF Payslip (Phiếu lương) có đính kèm lời dặn dò từ AI sẽ được gửi tự động và bảo mật qua Email / Telegram tới cá nhân Nguyễn Văn A. Cán bộ Kế toán hoàn thành chu trình mà gần như không cần đánh máy bất kỳ một con số nào.
