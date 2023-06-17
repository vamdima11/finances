from django.db import models
from django.contrib.auth.models import User


class Portfolio(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    goal = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    approach = models.CharField(max_length=20, choices=(('Aggressive', 'Aggressive'), ('Balanced', 'Balanced'), ('Conservative', 'Conservative')))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Portfolio"

    class Meta:
        app_label = 'finances'


class Investment(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='investments')
    symbol = models.CharField(max_length=10)
    quantity = models.PositiveIntegerField(default=0)
    purchase_price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    current_market_value = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.symbol} ({self.quantity})"

    class Meta:
        app_label = 'finances'


class Goal(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='goals')
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"${self.amount}"

    class Meta:
        app_label = 'finances'


class History(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='history')
    change = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.change}"

    class Meta:
        app_label = 'finances'
