from ninja import NinjaAPI
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import get_object_or_404
from django.core.cache import cache
from typing import List

from .models import User, Course
from .schemas import RegisterSchema, LoginSchema, TokenSchema, UserSchema, CourseSchema, CourseCreateSchema
from .jwt_auth import create_token, AuthBearer, EXPIRATION_MINUTES
from .utils.rate_limit import check_rate_limit
from .rbac import assert_is_dosen_or_admin

# Inisiasi API
api = NinjaAPI(title="Simple LMS Backend", version="1.0.0")

# --- AUTH ENDPOINTS ---

@api.post("/auth/register", response=UserSchema, tags=["Auth"])
def register(request, data: RegisterSchema):
    """
    Mendaftarkan user baru dengan Role:
    0 = Admin, 1 = Dosen, 2 = Mahasiswa
    """
    hashed_password = make_password(data.password)
    
    # Mencegah error jika email None, ganti dengan string kosong
    email_val = data.email if data.email else ""

    user = User.objects.create(
        username=data.username,
        password=hashed_password,
        role=data.role,
        email=email_val
    )
    return user

@api.post("/auth/login", response=TokenSchema, tags=["Auth"])
def login(request, data: LoginSchema):
    ip = request.META.get('REMOTE_ADDR')
    check_rate_limit(ip)
    """
    Login user dan mendapatkan JWT Token
    """
    user = get_object_or_404(User, username=data.username)
    
    if not check_password(data.password, user.password):
        return api.create_response(request, {"detail": "Invalid credentials"}, status=401)
    
    token = create_token(user.id)
    
    return {
        "access_token": token,
        "expires_in": EXPIRATION_MINUTES * 60
    }

# --- COURSE ENDPOINTS ---

@api.post("/courses", ...)
def create_course(request, data: CourseCreateSchema):
    assert_is_dosen_or_admin(request)
    """
    Hanya Admin (0) atau Dosen (1) yang boleh buat course.
    """
    # RBAC CHECK: Jika role 2 (Mahasiswa), tolak!
    if request.user.role == 2:
        return api.create_response(request, {"detail": "Mahasiswa dilarang membuat course!"}, status=403)

    course = Course.objects.create(
        title=data.title,
        description=data.description,
        instructor=request.user
    )
    
    # HAPUS CACHE (Agar data baru muncul di list)
    cache.delete("courses_data")
    
    return course

@api.get("/courses", response=List[CourseSchema], auth=AuthBearer(), tags=["Course"])
def list_courses(request):
    """
    Mengambil semua course dengan Caching Redis.
    """
    # 1. Cek Redis dulu
    cached_data = cache.get("courses_data")
    if cached_data:
        return cached_data # Return data cache (Cepat!)

    # 2. Kalau tidak ada, ambil dari DB
    courses = list(Course.objects.all())
    
    # 3. Simpan ke Redis (Expire 15 menit)
    cache.set("courses_data", courses, timeout=900)
    
    return courses

@api.delete("/courses/{course_id}", auth=AuthBearer(), tags=["Course"])
def delete_course(request, course_id: int):
    """
    Menghapus course. Hanya Admin/Dosen.
    """
    # RBAC Check
    if request.user.role == 2:
        return api.create_response(request, {"detail": "Forbidden"}, status=403)
        
    course = get_object_or_404(Course, id=course_id)
    course.delete()
    
    # Hapus cache juga saat delete
    cache.delete("courses_data")
    
    return {"success": True}

    # --- SESSION ENDPOINT (Sesuai Soal C.2) ---

@api.get("/test-session", tags=["Session"])
def test_session_redis(request):
    """
    Endpoint untuk membuktikan Session tersimpan di Redis.
    Setiap kali di-refresh, hitungan 'visit_count' akan bertambah.
    """
    # Ambil data dari session, default 0
    count = request.session.get('visit_count', 0)
    
    # Tambah 1
    new_count = count + 1
    
    # Simpan balik ke session
    request.session['visit_count'] = new_count
    
    return {
        "message": "Session is working via Redis!",
        "visit_count": new_count,
        "session_key": request.session.session_key
    }