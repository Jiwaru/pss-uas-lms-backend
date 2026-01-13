from ninja import Schema
from typing import Optional
from datetime import datetime

# Schema untuk Input Register
class RegisterSchema(Schema):
    username: str
    password: str
    email: Optional[str] = None
    role: int  # 0=Admin, 1=Dosen, 2=Mahasiswa

# Schema untuk Input Login
class LoginSchema(Schema):
    username: str
    password: str

# Schema untuk Response User (Output)
class UserSchema(Schema):
    id: int
    username: str
    role: str # Kita akan return label role-nya (Admin/Dosen/dll)
    
    @staticmethod
    def resolve_role(obj):
        # Mengubah angka role menjadi teks label
        return obj.get_role_display()

# Schema untuk Token JWT
class TokenSchema(Schema):
    access_token: str
    token_type: str = "bearer"
    expires_in: int  # dalam detik

    # Tambahkan di lms/schemas.py

class CourseCreateSchema(Schema):
    title: str
    description: str

class CourseSchema(Schema):
    id: int
    title: str
    description: str
    instructor_name: str 
    
    @staticmethod
    def resolve_instructor_name(obj):
        # Mengambil nama username dari relasi instructor
        return obj.instructor.username