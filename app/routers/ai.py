from fastapi import APIRouter
from ..schemas.ai import AISchema
from openai import OpenAI
import os


# شناسایی مدل
from fastapi import Depends
from sqlalchemy.orm import Session
from ..database import get_session

from sqlalchemy import text


client = OpenAI(
    base_url="https://ai.liara.ir/api/69560d1b7ac6eb7bf9fe31aa/v1",
    api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJrZXkiOiI2OTU2MGQ1YTVmNjVkNjE0ODA0OGMzOGIiLCJ0eXBlIjoiYWlfa2V5IiwiaWF0IjoxNzY3MjQ3MTk0fQ.twu6xRE4Q_TZhOlS2cnks22zc3LrbT8gTCCsmb0sSoc"
)

router = APIRouter(prefix="/ai", tags=["AI"])

@router.post("/chat")
def chat_with_ai(request: AISchema, db: Session = Depends(get_session)):
    

    query = text("SELECT province.province, city.city, city.province_id FROM province, city WHERE city.province_id = province.id ")
    result = db.execute(query).fetchall()

    db_context = "\n".join(
        [f"id: {r.province_id}, name: {r.province}, email: {r.city}" for r in result]
    )

    completion = client.chat.completions.create(
        model="openai/gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": "فقط بر اساس داده‌های دیتابیس پاسخ بده."
            },
            {
                "role": "system",
                "content": f"داده‌ها:\n{db_context}"
            },
            {
                "role": "user",
                "content": request.message
            }
        ]
    )

    return {
        "response": completion.choices[0].message.content
    }
