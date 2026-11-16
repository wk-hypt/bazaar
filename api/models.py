from django import db
from django.db import models
from django.contrib.auth.models import User

class Organizer(models.Model):
    """Organizer model, matching the field with the sql database."""
    org_id = models.CharField(max_length=50, primary_key=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    full_name = models.CharField(max_length=100)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.full_name

    class Meta:
            db_table = 'organizer'

class Mall(models.Model):
    """Mall model, matching the field with the sql database."""
    mall_id = models.CharField(max_length=50, primary_key=True)
    mall_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)

    def __str__(self):
        return self.mall_name

    class Meta:
        db_table = 'mall'

class Vendor(models.Model):
    """Vendor model, matching the field with the sql database."""
    ven_id = models.CharField(max_length=50, primary_key=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    full_name = models.CharField(max_length=100)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.full_name

    class Meta:
        db_table = 'vendor'

class Item(models.Model):
    """Item model, matching the field with the sql database."""
    item_id = models.CharField(max_length=50, primary_key=True)
    item_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    ven_id = models.ForeignKey(Vendor, on_delete=models.CASCADE, db_column='ven_id')

    class Meta:
        db_table = 'item'

class Market(models.Model):
    """Market model, matching the field with the sql database."""
    mar_id = models.CharField(max_length=50, primary_key=True)
    title = models.CharField(max_length=100)
    start_time = models.DateField()
    end_time = models.DateField()
    mall_id = models.ForeignKey(Mall, on_delete=models.CASCADE, db_column='mall_id')
    org_id = models.ForeignKey(Organizer, on_delete=models.CASCADE, db_column='org_id')

    class Meta:
        db_table = 'market'

class Booth(models.Model):
    """Booth model, matching the field with the sql database."""
    booth_id = models.CharField(max_length=50, primary_key=True)
    mall_id = models.ForeignKey(Mall, on_delete=models.CASCADE, db_column='mall_id')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    booth_number = models.CharField(max_length=20)

    class Meta:
        db_table = 'booth'

class Booking(models.Model):
    """Booking model, matching the field with the sql database."""
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    booking_id = models.CharField(max_length=50, primary_key=True)
    mar_id = models.ForeignKey(Market, on_delete=models.CASCADE, db_column='mar_id')
    booth_id = models.ForeignKey(Booth, on_delete=models.CASCADE, db_column='booth_id')
    ven_id = models.ForeignKey(Vendor, on_delete=models.CASCADE, db_column='ven_id')
    booking_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'booking'

class Invoice(models.Model):
    """Invoice model, matching the field with the sql database."""
    STATUS_CHOICES = [
        ('Unpaid', 'Unpaid'),
        ('Paid', 'Paid'),
    ]
    inv_id = models.CharField(max_length=50, primary_key=True)
    booking_id = models.ForeignKey(Booking, on_delete=models.CASCADE, db_column='booking_id')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Unpaid')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    issued_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'invoice'
