from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database import get_db
from schemas.school import EnrollmentCreate
from services import student as services

router = APIRouter()

@router.get("/students/{student_id}")
def read_student(student_id: int, db: Session = Depends(get_db)):
    return services.get_student_details(db, student_id)

@router.post("/enrollments", status_code=status.HTTP_201_CREATED)
def enroll_student(data: EnrollmentCreate, db: Session = Depends(get_db)):
    enrollment = services.create_new_enrollment(db, data)
    return {"message": "Đăng ký khóa học thành công!", "data": enrollment}