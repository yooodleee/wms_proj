from django.db import models


class Warehouse(models.Model):
    """
    창고(Entity). 여러 개의 창고를 관리
    """
    code = models.CharField(max_length=64, unique=True, db_index=True) # 창고 코드
    name = models.CharField(max_length=120) # 창고 이름
    location = models.CharField(max_length=255, blank=True, null=True) # 위치
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'warehouse'
        ordering = ['name']
    
    def __str__(self):
        return f"{self.code} - {self.name}"