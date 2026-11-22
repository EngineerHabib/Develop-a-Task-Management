from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    PRIORITY_CHOICES = [
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
    ]
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_task',
        null=True,
    )
    title = models.CharField(max_length=200, null=True)
    description = models.TextField(null=True)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, null=True)
    due_date = models.DateField(null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f'{self.title}'
