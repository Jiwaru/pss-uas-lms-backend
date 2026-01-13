import jwt
import datetime
from django.conf import settings
from ninja.security import HttpBearer
from django.shortcuts import get_object_or_404
from .models import User

# Setup dasar
ALGORITHM = "HS256"
EXPIRATION_MINUTES = 60  # Token berlaku 1 jam

def create_token(user_id: int):
    """Membuat JWT Token baru"""
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=EXPIRATION_MINUTES),
        "iat": datetime.datetime.utcnow(),
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=ALGORITHM)
    return token

class AuthBearer(HttpBearer):
    """Class untuk memproteksi endpoint (Decorator)"""
    def authenticate(self, request, token):
        try:
            # Decode token
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
            user_id = payload.get("user_id")
            
            # Cek apakah user ada di DB
            user = User.objects.get(id=user_id)
            
            # Tempel object user ke request agar bisa diakses di view
            request.user = user 
            return user
        except jwt.ExpiredSignatureError:
            return None # Token kadaluarsa
        except (jwt.DecodeError, User.DoesNotExist):
            return None # Token palsu atau user dihapus