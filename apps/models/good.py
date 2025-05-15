from django.db import models
from django.db.models import Q, F, CheckConstraint


class Good(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, db_index=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock = models.PositiveIntegerField(default=0, help_text="库存数量")
    reserved = models.PositiveIntegerField(default=0, help_text="已预订数量")
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self._old_name = self.name

    def __str__(self):
        return f"【{self.id}】{self.name} ({self.price}) [{self.reserved}/{self.stock}]"

    # def save(self, *args, **kwargs):
    #     if self.id:
    #         old_obj = Good.objects.get(id=self.id)
    #         self._old_name = old_obj.name
    #     super().save(*args, **kwargs)

    # 计算可用库存的property
    @property
    def available_stock(self):
        """计算可用库存"""
        return self.stock - self.reserved

    class Meta:
        verbose_name = "good"
        indexes = [models.Index(fields=['name'], name='good_name_idx')]
        ordering = ['id']
        constraints = [CheckConstraint(check=Q(reserved__lte=F('stock')), name='reserved_le_stock')]
