from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, name=None, role="user"):
        if not email:
            raise ValueError("Email wajib diisi")

        email = self.normalize_email(email)
        user = self.model(
            email=email,
            name=name,
            role=role,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
