from django.db import models


class Supplier(models.Model):
    code = models.CharField(max_length=64, unique=True, db_index=True) # 고유 코드
    name = models.CharField(max_length=120) # 업체명
    contact_name = models.CharField(max_length=64, blank=True, null=True) # 담당자 이름
    phone = models.CharField(max_length=32, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'suppliers'
        indexes = [models.Index(fields=['code']), models.Index(fields=['name'])]
        ordering = ['name']
    
    def __str__(self):
        return f"{self.code} - {self.name}"