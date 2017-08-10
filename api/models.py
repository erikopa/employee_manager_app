from django.db import models


class Employee(models.Model):
    """This class represents the employees model"""
    name = models.CharField(max_length=255, blank=False)
    email = models.EmailField(max_length=255, blank=False, unique=True)
    department = models.CharField(max_length=255, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'employees'
        verbose_name = 'employee'
        ordering = ('-created_at',)

    def __str__(self):
        return self.name