# AGO Fruit - Trade Document Automation (PoC)

Giới thiệu
Đây là Proof of Concept (PoC) cho hệ thống tự động hóa xử lý chứng từ xuất nhập khẩu (Option A). 
API sử dụng FastAPI và Multimodal LLM (Gemini 2.5 Flash) để trích xuất trực tiếp thông tin từ hình ảnh chứng từ (Invoice, Packing List) thành định dạng JSON chuẩn xác mà không cần qua các công cụ OCR trung gian.

Cài đặt và Chạy thử

1. Clone repository và thiết lập môi trường:**
```bash
git clone 
cd ago-fruit-poc
python -m venv venv

# Kích hoạt môi trường
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate

2. Cài đặt thư viện:
Bash
pip install -r requirements.txt

3. Thiết lập biến môi trường:
Tạo một file .env ở thư mục gốc và thêm API key của Google Gemini:

Code snippet
GEMINI_API_KEY=your_api_key_here

4. Chạy Server:

Bash
python main.py
Server sẽ chạy tại: http://localhost:8000

Cách Test
Mở trình duyệt và truy cập vào Swagger UI: http://localhost:8000/docs

Tìm đến API POST /api/v1/extract -> Bấm Try it out.

Upload một file ảnh hóa đơn bất kỳ (.jpg, .png) và bấm Execute.

Kết quả trả về sẽ là cấu trúc JSON chi tiết của hóa đơn.