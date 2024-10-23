from django.contrib.auth.models import Group
from django.db import models
from django.contrib.auth.models import AbstractUser

Group.add_to_class(
    "description", models.CharField(max_length=180, null=True, blank=True)
)

class AdditionalPermission(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class User(AbstractUser):
    image = models.ImageField(
        null=True, blank=True, default="", upload_to="frontend/public/dist/images/users"
    )
    additional_permissions = models.ManyToManyField(AdditionalPermission, blank=True)
    REQUIRED_FIELDS = ["image", "email", "first_name", "last_name", "hourly_rate"]
    hourly_rate = models.FloatField(null=True, blank=True)

    def get_additional_permissions(self):
        return ", ".join(str(p) for p in self.additional_permissions.all())

    get_additional_permissions.short_description = "Additional permissions"

    def __str__(self):
        if self.first_name and self.last_name:
            return self.first_name + " " + self.last_name
        elif self.first_name:
            return self.first_name
        else:
            return self.username