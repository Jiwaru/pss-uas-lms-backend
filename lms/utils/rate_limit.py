import time
from ninja.errors import HttpError

# Simpan percobaan login di memori sementara
LOGIN_ATTEMPTS = {}

def check_rate_limit(ip_address: str, limit: int = 5, window: int = 60):
    """
    Cek apakah IP sudah mencoba login melebihi batas (limit) dalam waktu (window) detik.
    """
    current_time = time.time()

    # Ambil data IP ini
    attempts = LOGIN_ATTEMPTS.get(ip_address, [])

    # Bersihkan data lama yang sudah lewat waktu (expired)
    attempts = [t for t in attempts if current_time - t < window]

    if len(attempts) >= limit:
        raise HttpError(429, "Too Many Requests: Silakan coba 1 menit lagi.")

    # Simpan percobaan baru
    attempts.append(current_time)
    LOGIN_ATTEMPTS[ip_address] = attempts