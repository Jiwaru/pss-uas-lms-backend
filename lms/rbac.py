from ninja.errors import HttpError

def assert_is_dosen_or_admin(request):
    """
    Fungsi helper untuk memblokir akses jika user adalah Mahasiswa (Role 2).
    Melempar error 403 jika tidak berhak.
    """
    if request.user.role == 2:  # 2 = Mahasiswa
        raise HttpError(403, "Forbidden: Akses khusus Dosen/Admin.")