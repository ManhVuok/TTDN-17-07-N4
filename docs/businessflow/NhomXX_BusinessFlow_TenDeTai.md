# SƠ ĐỒ LUỒNG NGHIỆP VỤ END-TO-END (ERP HRM SYSTEM)

Dưới đây là sơ đồ luồng nghiệp vụ tổng quan của hệ thống, thể hiện sự tích hợp giữa các module (HRM, Chấm công, Tính lương) và các điểm ứng dụng công nghệ AI/API.

```mermaid
swimlane
    title Luồng nghiệp vụ Quản trị Nhân sự & Lương (E2E)
    
    group Admin / HR
        task "1. Tiếp nhận & Tạo hồ sơ NV" as p1
        task "2. Ký Hợp đồng lao động" as p2
        task "8. Cập nhật Nghỉ việc" as p8
    end
    
    group Nhân viên
        task "3. Chấm công (Sáng/Chiều)" as p3
        task "4. Tra cứu Nội quy (Hỏi AI)" as p4
    end
    
    group Hệ thống (ERP)
        task "5. Tự động tính đi muộn/về sớm" as p5
        task "6. Gửi báo cáo ngày qua Telegram" as p6
        task "9. Tự động đóng Hợp đồng" as p9
    end
    
    group Kế toán / Quản lý
        task "7. Duyệt Bảng lương tháng" as p7
        task "10. Nhận thông báo Telegram" as p10
    end

    p1 -> p2: Khởi tạo dữ liệu gốc
    p2 -> p3: Bắt đầu làm việc
    p3 -> p5: Ghi nhận logs
    p5 -> p6: [Mức 2] Trigger hàng ngày
    p6 -> p10: [Mức 3] Gửi API
    p3 -> p4: [Mức 3] Tương tác AI
    p7 -> p10: [Mức 3] Thông báo duyệt lương
    p8 -> p9: [Mức 2] Event-driven
```

### Giải thích các điểm tích hợp:

1.  **Dữ liệu gốc (Mức 1)**: Thông tin Nhân viên từ module `nhan_su` là nguồn dữ liệu duy nhất cung cấp cho Chấm công và Tính lương.
2.  **Tự động hóa (Mức 2)**:
    *   **Scheduled**: Hệ thống tự động tổng hợp và gửi báo cáo hàng ngày (p6).
    *   **Event-driven**: Khi Admin cập nhật trạng thái "Nghỉ việc", hệ thống tự động khóa hợp đồng (p9).
3.  **Công nghệ AI & API (Mức 3)**:
    *   **AI/LLM**: Nhân viên có thể hỏi AI về nội quy (p4) dựa trên dữ liệu context được huấn luyện.
    *   **External API**: Hệ thống tích hợp Telegram Bot để gửi các thông báo quan trọng (p6, p10).
