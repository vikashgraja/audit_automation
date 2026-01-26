from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, employee_id, email=None, password=None, **extra_fields):
        if not email:
            # We can now auto-generate or require it.
            # If the user model saves it automatically, we might pass None.
            # But BaseUserManager usually expects it.
            # Let's rely on the model save for auto-generation if not provided.
            email = f"{employee_id}@hmil.net"

        email = self.normalize_email(email)
        user = self.model(employee_id=employee_id, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, employee_id, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")

        return self.create_user(employee_id, email, password, **extra_fields)


class Unit(models.Model):
    UNIT_TYPES = (
        ("VERTICAL", "Vertical"),
        ("DOMAIN", "Domain"),  # Plant, HO & RO
        ("SUB_DOMAIN", "Sub Domain"),  # Operations, Risk & Analytics, Functions
    )

    name = models.CharField(max_length=100)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True, related_name="children")
    unit_type = models.CharField(max_length=20, choices=UNIT_TYPES)

    def __str__(self):
        return self.name


class UserExactRoles(models.TextChoices):
    VERTICAL_HEAD = "Vertical Head", "Vertical Head"
    DOMAIN_HEAD = "Domain Head", "Domain Head"
    SUB_DOMAIN_HEAD = "Sub Domain Head", "Sub Domain Head"
    AUDITOR = "Auditor", "Auditor"


class User(AbstractBaseUser, PermissionsMixin):
    employee_id = models.IntegerField(unique=True)
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    password_change_required = models.BooleanField(default=True)

    # New fields
    role = models.CharField(max_length=20, choices=UserExactRoles.choices, null=True, blank=True)
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True, blank=True, related_name="members")

    USERNAME_FIELD = "employee_id"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = ["email", "first_name", "last_name"]

    objects = UserManager()

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def save(self, *args, **kwargs):
        if not self.email and self.employee_id:
            self.email = f"{self.employee_id}@hmil.net"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.employee_id} {self.first_name} {self.last_name}"
