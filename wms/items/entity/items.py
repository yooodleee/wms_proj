from django.db import models


class Item(models.Model):
    sku = models.CharField(max_length=54, unique=True)
    name = models.CharField(max_length=120)
    category = models.CharField(max_length=64, blank=True, null=True, db_index=True)
    unit_of_measure = models.CharField(max_length=16, default='EA') # DA, BOX, CASE ...
    size = models.CharField(max_length=64, blank=True, null=True)
    weight = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    barcode = models.CharField(max_length=64, blank=True, null=True, db_index=True)

    # suppliers 도메인 생성 이후 활성화
    supplier = models.ForeignKey(
        'suppliers.Supplier',
        on_delete=models.SET_NULL,
        null=True, blank=True, related_name='items'
    )

    attributes = models.JSONField(default=dict, blank=True) # 색상, 소재 등
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'items'
        
        indexes = [
            models.Index(fields=['sku']),
            models.Index(fields=['barcode']),
            models.Index(fields=['category']),
        ]
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.sku} - {self.name}"