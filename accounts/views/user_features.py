import jwt
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, exceptions, authentication, permissions
from rest_framework.parsers import FormParser, MultiPartParser
from accounts.models import User, RefreshToken

# === 1. ALAT BACA TOKEN (Custom Authentication) ===
# Menyesuaikan dengan logic teman Anda yang menggunakan 'sub' sebagai User ID
class TemanJWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return None

        try:
            # Format header: "Bearer <token>"
            token = auth_header.split(' ')[1]
            
            # Decode token menggunakan Secret Key dari settings.py
            payload = jwt.decode(token, settings.ACCESS_TOKEN_SECRET, algorithms=["HS256"])
            
            # Mengambil User ID dari key 'sub' sesuai file jwt.py teman Anda
            user_id = payload['sub']
            user = User.objects.get(id=user_id)
            
            return (user, token)
            
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Token sudah kadaluarsa.')
        except (jwt.DecodeError, User.DoesNotExist, IndexError, KeyError):
            raise exceptions.AuthenticationFailed('Token tidak valid.')

# === 2. VIEW PROFILE (READ & UPDATE) ===
class UpdateProfileView(APIView):
    authentication_classes = [TemanJWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    # Menggunakan parser yang sama dengan file login.py teman Anda
    parser_classes = (FormParser, MultiPartParser) 

    # --- FUNGSI READ (Melihat Data Profil) ---
    def get(self, request):
        user = request.user # Didapat otomatis dari token yang valid
        return Response({
            "status": "success",
            "message": "Data profil berhasil diambil",
            "data": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role,
                "last_login": user.last_login
            }
        }, status=status.HTTP_200_OK)

    # --- FUNGSI UPDATE (Mengubah Data Profil) ---
    def patch(self, request):
        user = request.user
        data = request.data

        # Update Nama jika dikirim lewat form
        if 'name' in data:
            user.name = data['name']
        
        # Update Email dengan pengecekan duplikasi
        if 'email' in data:
            if User.objects.filter(email=data['email']).exclude(id=user.id).exists():
                return Response({"error": "Email sudah dipakai orang lain"}, status=400)
            user.email = data['email']
            
        user.save()

        return Response({
            "status": "success",
            "message": "Profile berhasil diupdate",
            "data": {
                "id": user.id,
                "name": user.name,
                "email": user.email
            }
        }, status=status.HTTP_200_OK)

# === 3. LOGOUT (Menghapus Refresh Token) ===
class LogoutView(APIView):
    authentication_classes = [TemanJWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (FormParser, MultiPartParser)

    def post(self, request):
        # Mengambil refresh_token dari body form-data
        refresh_token = request.data.get('refresh_token')
        
        if not refresh_token:
            return Response({"error": "Wajib mengirimkan refresh_token"}, status=400)

        # Menghapus token dari tabel RefreshToken milik teman Anda
        deleted_count, _ = RefreshToken.objects.filter(token=refresh_token).delete()

        if deleted_count > 0:
            return Response({"message": "Logout berhasil."}, status=200)
        else:
            return Response({"error": "Token tidak ditemukan atau sudah tidak berlaku."}, status=400)