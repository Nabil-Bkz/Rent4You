from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class CodePromo(models.Model):
    """Code promo model - Promo Code"""
    code = models.CharField(max_length=50, unique=True)
    discount_percentage = models.DecimalField(
        max_digits=5, 
        decimal_places=2, 
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    max_uses = models.PositiveIntegerField(null=True, blank=True)  # None = unlimited
    current_uses = models.PositiveIntegerField(default=0)
    valid_from = models.DateTimeField()
    valid_until = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    
    agence = models.ForeignKey('agencies.Agence', on_delete=models.CASCADE, related_name='codes_promo')
    created_by = models.ForeignKey('accounts.AdminAgence', on_delete=models.SET_NULL, null=True, related_name='codes_promo_crees')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'codes_promo'
        verbose_name = 'Code Promo'
        verbose_name_plural = 'Codes Promo'
    
    def __str__(self):
        return f"{self.code} ({self.discount_percentage}%)"
    
    def is_valid(self):
        """Check if promo code is valid"""
        now = timezone.now()
        if not self.is_active:
            return False
        if now < self.valid_from or now > self.valid_until:
            return False
        if self.max_uses and self.current_uses >= self.max_uses:
            return False
        return True
    
    def use(self):
        """Increment usage count"""
        if self.is_valid():
            self.current_uses += 1
            self.save()
            return True
        return False

