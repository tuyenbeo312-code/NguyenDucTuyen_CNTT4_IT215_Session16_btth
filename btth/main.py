from fastapi import FastAPI
from database import engine
from models import department, student, course, enrollment
from routers import student as router_student

department.Base.metadata.create_all(bind=engine)
student.Base.metadata.create_all(bind=engine)
course.Base.metadata.create_all(bind=engine)
enrollment.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(router_student.router)


@app.get("/")
def root():
    return {"message": "Hệ thống quản lý trung tâm đào tạo đang hoạt động!"}
