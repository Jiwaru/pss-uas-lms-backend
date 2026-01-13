# lms/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    # Definisi Role sesuai soal (0=Admin, 1=Dosen, 2=Mahasiswa)
    # Kita pakai IntegerChoices agar hemat memori & mudah di validasi
    class Roles(models.IntegerChoices):
        ADMIN = 0, 'Admin'
        DOSEN = 1, 'Dosen'
        MAHASISWA = 2, 'Mahasiswa'

    role = models.SmallIntegerField(choices=Roles.choices, default=Roles.MAHASISWA)

    # Tambahan: AbstractUser sudah punya field: username, password, email, first_name, last_name
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    # Instructor merujuk ke User (biasanya Dosen)
    # on_delete=models.CASCADE artinya jika Dosen dihapus, Course-nya ikut hilang
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='courses')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title