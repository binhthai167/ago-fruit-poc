from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from google import genai
from PIL import Image
import io
import os
import json
from dotenv import load_dotenv

# Load biến môi trường từ .env
load_dotenv()

# Cấu hình Gemini bằng SDK mới
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("Chưa cấu hình GEMINI_API_KEY trong file .env")

# Khởi tạo Client theo chuẩn mới của google-genai
client = genai.Client(api_key=api_key)

app = FastAPI(
    title="AGO Fruit - Document Extraction API",
    description="API bóc tách dữ liệu hóa đơn chứng từ bằng Multimodal LLM (Sử dụng google-genai SDK mới nhất)",
    version="1.0.0"
)

SYSTEM_PROMPT = """
Bạn là một trợ lý AI chuyên nghiệp hỗ trợ phòng Logistics.
Nhiệm vụ của bạn là đọc hình ảnh chứng từ (Invoice, Packing List...) và trích xuất dữ liệu thành định dạng JSON CHÍNH XÁC.
Schema yêu cầu:
{
  "document_type": "Tên loại tài liệu",
  "company_name": "Tên công ty xuất/nhập khẩu",
  "total_amount": "Tổng tiền kèm đơn vị (nếu có)",
  "items": [{"name": "Tên hàng hóa", "quantity": "Số lượng"}],
  "confidence_score": "Điểm từ 0.0 đến 1.0 đánh giá độ tự tin của bạn về kết quả"
}
Lưu ý:
- Chỉ trả về duy nhất chuỗi JSON, không giải thích gì thêm, không dùng markdown block ```json.
- Nếu không tìm thấy thông tin cho một trường, hãy để giá trị là null.
"""

@app.post("/api/v1/extract", tags=["Document Processing"])
async def process_document(file: UploadFile = File(...)):
    # Validate định dạng file
    if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        raise HTTPException(status_code=400, detail="PoC hiện tại chỉ hỗ trợ định dạng ảnh (.png, .jpg, .jpeg)")
    
    try:
        # Đọc dữ liệu file
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        # Gọi API bằng SDK mới
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=[SYSTEM_PROMPT, image]
        )
        raw_text = response.text.strip()
        
        # Clean up text
        if raw_text.startswith("```json"):
            raw_text = raw_text[7:-3].strip()
        elif raw_text.startswith("```"):
            raw_text = raw_text[3:-3].strip()
            
        # Parse JSON
        parsed_data = json.loads(raw_text)
        
        return JSONResponse(content={
            "status": "success",
            "filename": file.filename,
            "data": parsed_data
        })
        
    except json.JSONDecodeError:
         raise HTTPException(status_code=500, detail="AI trả về dữ liệu không đúng chuẩn JSON.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi hệ thống: {str(e)}")

@app.get("/", tags=["Health Check"])
async def root():
    return {"message": "AGO Fruit Document API is running. Truy cập /docs để test API."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)