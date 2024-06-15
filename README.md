"# intern_pdfmobile_GradNU" 
♥ ถ้ายังไม่ติดตั้งอะไรเลย
[1.] pip install -r requirements.txt

♥ HTTP Response
ใช้ Docs ไว้ดู HTTP Response ของ FastAPI เอง โดยไม่ต้องใช้ Postman --->  http://127.0.0.1:8000/

♥ ถ้าติดตั้งหมดแล้ว -> Start project
[1.แอคติเวทvirtual environment] .\venv\Scripts\activate
[2.ใช้ api เรียกใช้ app ในไฟล์ main.py *ปล. --reload คือป้องกันเวลาเรากด ctrl+c แล้วไปตัดการเชื่อมต่อ api แล้วก็ทุกครั้งที่อัพเดทโค้ดมันจะรีโหลดหน้าเว็บให้ออโต้เลย*] uvicorn main:app --reload