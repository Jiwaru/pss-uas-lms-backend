Berikut adalah isi file `README.md` lengkap yang disusun secara profesional untuk memenuhi standar penilaian UAS .

Silakan buat file bernama **`README.md`** di folder utama proyek kamu, lalu _copy-paste_ seluruh kode di bawah ini.

````markdown
# Simple LMS Backend (Django Ninja + Redis)

Proyek ini adalah Backend untuk **Simple Learning Management System (LMS)** yang dikembangkan sebagai Tugas Akhir Mata Kuliah **Pemrograman Sisi Server**.

Sistem ini dibangun menggunakan **Django** dan **Django Ninja** untuk arsitektur REST API modern, serta mengimplementasikan **Redis** untuk _caching_ dan _session management_.

---

## 📋 Fitur Utama

Proyek ini memenuhi seluruh kriteria fungsional yang diminta:

1.  **Authentication & Security**:
    - Register & Login menggunakan **JWT (JSON Web Token)**.
    - Password hashing (Bcrypt).
    - Rate limiting sederhana pada endpoint login.
2.  **Authorization (RBAC)**:
    - **Admin/Dosen (Role 0/1)**: Memiliki akses penuh (CRUD Course).
    - **Mahasiswa (Role 2)**: Hanya memiliki akses baca (GET Course). Akses tulis/hapus diblokir (403 Forbidden).
3.  **Course Management**:
    - CRUD (Create, Read, Update, Delete) untuk entitas Course.
4.  **High Performance (Redis Integration)**:
    - **Caching**: Menyimpan data `GET /courses` di Redis untuk mempercepat response. Cache otomatis dihapus (_invalidated_) saat ada data baru (POST/DELETE).
    - **Session Storage**: Memindahkan penyimpanan Session Backend dari database SQL ke Redis (Database Index 1).

---

## 🛠 Teknologi

- **Bahasa**: Python 3.10+
- **Framework Web**: Django 4.x
- **API Framework**: Django Ninja (FastAPI-like)
- **Database**: SQLite (Development Default)
- **Cache & NoSQL**: Redis (via Docker)
- **Containerization**: Docker (untuk Redis)

---

## 🚀 Panduan Instalasi (Setup)

Ikuti langkah-langkah berikut untuk menjalankan proyek di komputer lokal:

### 1. Clone Repository

```bash
git clone [https://github.com/username-kamu/uas-backend-lms.git](https://github.com/username-kamu/uas-backend-lms.git)
cd uas-backend-lms
```
````

### 2. Setup Virtual Environment

Disarankan menggunakan virtual environment agar dependencies terisolasi.

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate

```

**Mac/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate

```

### 3. Install Dependencies

Pastikan file `requirements.txt` tersedia.

```bash
pip install -r requirements.txt

```

### 4. Menjalankan Redis (Wajib)

Proyek ini **memerlukan Redis** agar fitur Cache dan Session berjalan. Gunakan Docker untuk menjalankannya:

```bash
docker run -d --name redis-lms -p 6379:6379 redis:alpine

```

_Pastikan aplikasi Docker Desktop sudah berjalan sebelum mengetik perintah di atas._

### 5. Migrasi Database

Siapkan database SQLite dan tabel-tabel yang dibutuhkan.

```bash
python manage.py migrate

```

---

## ▶️ Cara Menjalankan Project

Setelah setup selesai, jalankan server Django dengan perintah:

```bash
python manage.py runserver

```

Server akan berjalan di: `http://127.0.0.1:8000`

---

## 🧪 Panduan Testing (User Guide)

Pengujian API dapat dilakukan melalui **Swagger UI** yang disediakan otomatis oleh Django Ninja.

1. **Buka Dokumentasi API:**
   Akses URL: [http://127.0.0.1:8000/api/docs](https://www.google.com/search?q=http://127.0.0.1:8000/api/docs)
2. **Skenario Testing:**

- **Register User:** Gunakan endpoint `/api/auth/register`.
- Role `1` = Dosen (Bisa Create/Delete).
- Role `2` = Mahasiswa (Hanya bisa Read).

- **Login & Authorize:**
- Login di `/api/auth/login` untuk mendapatkan `access_token`.
- Klik tombol **Authorize** (ikon gembok) di kanan atas Swagger.
- Masukkan format: `Bearer <paste_token_disini>`.

- **Test RBAC:**
- Login sebagai Mahasiswa -> Coba `DELETE /api/lms/courses/{id}` -> Harusnya **Gagal (403)**.
- Login sebagai Dosen -> Coba `POST` atau `DELETE` -> Harusnya **Sukses (200)**.

- **Test Redis Session:**
- Akses endpoint `/api/lms/test-session`.
- Refresh beberapa kali, counter akan bertambah (data ini disimpan di Redis).

---

## 📸 Bukti Implementasi

Berikut adalah bukti bahwa sistem berjalan sesuai spesifikasi soal.

### 1. Tampilan Swagger UI

Seluruh endpoint telah terdokumentasi dan dikelompokkan berdasarkan Tags (Auth, Course, Session).

### 2. Bukti Redis (Cache & Session Aktif)

Tangkapan layar terminal di bawah menunjukkan bahwa data **Session** dan **Cache** benar-benar tersimpan di Redis (Database Index 1).

**Perintah Cek:**

```bash
docker exec -it redis-lms redis-cli
select 1
keys *

```

**Hasil:**

_Penjelasan:_

- Key `:1:courses_data`: Menunjukkan caching aktif untuk endpoint Course.
- Key `django.contrib.sessions...`: Menunjukkan session backend tersimpan di Redis.

---

## 📂 Struktur Project

Struktur folder disusun mengikuti standar starter project UAS:

```text
uas-backend-lms/
├── manage.py
├── requirements.txt
├── README.md
├── simple_lms/           # Project Configuration
│   ├── settings.py       # Konfigurasi Redis & Apps ada di sini
│   └── urls.py
└── lms/                  # Main Application
    ├── utils/
    │   └── rate_limit.py # Fitur Rate Limiting
    ├── api.py            # API Endpoints & Logic
    ├── models.py         # Database Models (User, Course)
    ├── schemas.py        # Pydantic Schemas
    ├── jwt_auth.py       # JWT Authentication Handler
    └── rbac.py           # Role-Based Access Control Logic

```

```

**⚠️ PENTING:**
Jangan lupa untuk meletakkan file gambar **`image_1fc512.png`** (Screenshot Swagger) dan **`image_1fc92d.png`** (Screenshot Terminal Redis yang ada isinya) di dalam folder yang sama dengan file README.md ini agar gambarnya muncul saat dibuka dosen.

```
