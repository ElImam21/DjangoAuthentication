import pymysql

# === KODE ASLI TEMAN ANDA ===
pymysql.version_info = (2, 2, 7, "final", 0)
pymysql.install_as_MySQLdb()

# === TAMBAHAN "PENGAMAN" (Agar Support Laragon/MySQL 5.7) ===
# Kode ini memaksa Django untuk TIDAK mengecek versi database.
# Sangat berguna jika masih ada sisa-sisa "hantu" Django 5.0 di sistem Anda.
try:
    from django.db.backends.mysql.base import DatabaseWrapper
    DatabaseWrapper.check_database_version_supported = lambda self: None
except ImportError:
    pass