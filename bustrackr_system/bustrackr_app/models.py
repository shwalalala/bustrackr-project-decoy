from django.db import models

# Create your models here.
class Staff(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    role = models.CharField(max_length=50, default='staff')  # optional: admin, driver, etc.

    def __str__(self):
        return f"{self.first_name} {self.last_name}"