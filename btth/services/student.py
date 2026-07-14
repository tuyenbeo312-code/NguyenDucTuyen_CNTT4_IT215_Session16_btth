from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from models.student import Student
from models.department import Department
from models.enrollment import Enrollment
from models.course import Course
from schemas.school import EnrollmentCreate


def get_student_details(db: Session, student_id: int):
    student = db.query(Student).filter(Student.id == student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Sinh viên không tồn tại")

    department = (
        db.query(Department).filter(Department.id == student.department_id).first()
    )

    enrollments = db.query(Enrollment).filter(Enrollment.student_id == student_id).all()
    course_ids = [e.course_id for e in enrollments]
    courses = (
        db.query(Course).filter(Course.id.in_(course_ids)).all() if course_ids else []
    )

    return {"Student": student, "Department": department, "Courses": courses}


def create_new_enrollment(db: Session, data: EnrollmentCreate):
    student = db.query(Student).filter(Student.id == data.student_id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Sinh viên không tồn tại")
    if student.status != "ACTIVE":
        raise HTTPException(
            status_code=400, detail="Sinh viên không ở trạng thái ACTIVE"
        )

    course = db.query(Course).filter(Course.id == data.course_id).first()
    if not course:
        raise HTTPException(status_code=404, detail="Khóa học không tồn tại")
    if course.status != "OPEN":
        raise HTTPException(status_code=400, detail="Khóa học hiện không mở")

    existing = (
        db.query(Enrollment)
        .filter(
            Enrollment.student_id == data.student_id,
            Enrollment.course_id == data.course_id,
        )
        .first()
    )
    if existing:
        raise HTTPException(status_code=400, detail="Sinh viên đã đăng ký khóa học này")

    new_enrollment = Enrollment(student_id=data.student_id, course_id=data.course_id)
    db.add(new_enrollment)
    db.commit()
    db.refresh(new_enrollment)
    return new_enrollment
