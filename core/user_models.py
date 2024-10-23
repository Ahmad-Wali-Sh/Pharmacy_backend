from django.contrib.auth.models import Group
from django.db import models
from django.contrib.auth.models import AbstractUser

Group.add_to_class(
    "description", models.CharField(max_length=180, null=True, blank=True)
)


permissions = ["view_dashboard", "edit_profile"]


class AdditionalPermission(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    @classmethod
    def get_all_permissions(cls):
        return cls.objects.all()

    @classmethod
    def create_default_permissions(cls):
        for perm in permissions:
            cls.objects.get_or_create(name=perm)

    @classmethod
    def initialize_permissions(cls):
        existing_permissions = cls.objects.filter(name__in=permissions)
        if len(existing_permissions) != len(permissions):
            return cls.create_default_permissions()
        return existing_permissions


class User(AbstractUser):
    image = models.ImageField(
        null=True, blank=True, default="", upload_to="frontend/public/dist/images/users"
    )
    additional_permissions = models.ManyToManyField(AdditionalPermission, blank=True)
    hourly_rate = models.FloatField(null=True, blank=True)
    REQUIRED_FIELDS = ["image", "email", "first_name", "last_name", "hourly_rate"]

    def get_additional_permissions(self):
        return ", ".join(str(p) for p in self.additional_permissions.all())

    get_additional_permissions.short_description = "Additional permissions"

    def __str__(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username
