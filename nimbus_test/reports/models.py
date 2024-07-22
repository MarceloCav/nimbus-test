from django.db import models

# Create your models here.

class Report(models.Model):
    phone = models.CharField(max_length=20)
    report_date = models.DateTimeField()
    raw_data_path = models.CharField(max_length=255)
    pdf_path = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)