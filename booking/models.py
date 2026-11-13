from django.db import models

# Create your models here.

class Organizer(models.Model):
    org_id = models.CharField(max_length=50, primary_key=True)
    full_name = models.CharField(max_length=100)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.full_name

class Mall(models.Model):
    mall_id = models.CharField(max_length=50, primary_key=True)
    mall_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)

    def __str__(self):
        return self.mall_name

class Vendor(models.Model):
    vendor_id = models.CharField(max_length=50, primary_key=True)
    full_name = models.CharField(max_length=100)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)

    def __str__(self):
        return self.full_name

class Item(models.Model):
    item_id = models.CharField(max_length=50, primary_key=True)
    item_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, db_column='vendor_id')

class Market(models.Model):
    mar_id = models.CharField(max_length=50, primary_key=True)
    title = models.CharField(max_length=100)
    start_time = models.TimeField()
    end_time = models.TimeField()
    mall_id = models.ForeignKey(Mall, on_delete=models.CASCADE, db_column='mall_id')
    org_id = models.ForeignKey(Organizer, on_delete=models.CASCADE, db_column='org_id')

class Booth(models.Model):
    booth_id = models.CharField(max_length=50, primary_key=True)
    mall_id = models.ForeignKey(Mall, on_delete=models.CASCADE, db_column='mall_id')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    booth_number = models.CharField(max_length=20)

class Booking(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]
    booking_id = models.CharField(max_length=50, primary_key=True)
    mar_id = models.ForeignKey(Market, on_delete=models.CASCADE, db_column='mar_id')
    booth_id = models.ForeignKey(Booth, on_delete=models.CASCADE, db_column='booth_id')
    vendor_id = models.ForeignKey(Vendor, on_delete=models.CASCADE, db_column='vendor_id')
    booking_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

class Invoice(models.Model):
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
