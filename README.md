# Auth Service – Django

Auth Service adalah service autentikasi berbasis **Django REST Framework** yang berfungsi sebagai **authentication & token provider** dalam sistem Inventory Management System.

Service ini berfokus pada:
- Registrasi pengguna
- Login pengguna
- JWT Access Token & Refresh Token
- Middleware autentikasi
- Manajemen refresh token (termasuk cleanup otomatis)

---

## Fitur yang Tersedia

- ✅ Register user
- ✅ Login user
- ✅ Generate JWT Access Token
- ✅ Generate & refresh Refresh Token
- ✅ Middleware autentikasi
- ✅ Scheduled cleanup refresh token (management command)

---

## Keterbatasan Implementasi (Known Limitations)

Project ini **belum mengimplementasikan secara penuh** beberapa logic lanjutan pada fitur autentikasi, antara lain:

- ❌ **Update user profile**
- ❌ **Logout user (revokasi token secara eksplisit)**
- ❌ **Delete user account**

Logic lanjutan seperti update, logout, dan delete direncanakan sebagai **pengembangan tahap selanjutnya**.

---

## Catatan Teknis

- Logout saat ini **belum menghapus refresh token secara manual**
- Token akan dianggap tidak valid setelah:
  - Expired
  - Dihapus melalui proses cleanup berkala
- Endpoint protected menggunakan middleware autentikasi berbasis JWT

---

SILAHKAN BERTANYA JIKA ADA YANG DI BINGUNG KAN.
## Struktur Project

