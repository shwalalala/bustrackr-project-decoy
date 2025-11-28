from django.db import models
import random
from datetime import datetime

class AdminAccount(models.Model):
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.username


class StaffAccount(models.Model):
    staff_id = models.CharField(max_length=20, unique=True, blank=True)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def generate_staff_id():
        year = datetime.now().year % 100  # '25' for 2025
        rand1 = random.randint(1000, 9999)
        rand2 = random.randint(100, 999)
        return f"{year}-{rand1}-{rand2}"

    def save(self, *args, **kwargs):
        if not self.staff_id:
            self.staff_id = self.generate_staff_id()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.staff_id})"
