from rest_framework import serializers
from .models import Vendor, Item, Organizer, Mall, Market, Booth, Booking, Invoice

#The serializer file and error checking function

class VendorSerializer(serializers.ModelSerializer):
    """Convert a Vendor object to json format, received request and return responce, also have validation checking logic."""
    class Meta:
        model = Vendor
        fields = '__all__'

    def validate_phone(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Phone number must contain only digits.")
        if len(value) < 10 or len(value) > 11:
            raise serializers.ValidationError("Phone number must be between 10 and 11 digits.")
        return value

    def check_exists(self, data):
        email = data.get('email')
        if Vendor.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email already exists.")
        return data

class ItemSerializer(serializers.ModelSerializer):
    """Convert an Item object to json format, received request and return responce, also have validation checking logic."""
    class Meta:
        model = Item
        fields = '__all__'

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be a positive number.")
        return value

    def validate_item_from_vendor(self, data):
        ven_id = data.get('ven_id')
        if hasattr(ven_id, 'pk'):
            ven_id = ven_id.pk
        if not Vendor.objects.filter(ven_id=ven_id).exists():
            raise serializers.ValidationError("Vendor does not exist.")
        return data

class OrganizerSerializer(serializers.ModelSerializer):
    """Convert an Organizer object to json format, received request and return responce, also have validation checking logic."""
    class Meta:
        model = Organizer
        fields = '__all__'

    def validate_phone(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Phone number must contain only digits.")
        if len(value) < 10 or len(value) > 11:
            raise serializers.ValidationError("Phone number must be between 10 and 11 digits.")
        return value

class MallSerializer(serializers.ModelSerializer):
    """Convert a Mall object to json format, received request and return responce, also have validation checking logic."""
    class Meta:
        model = Mall
        fields = '__all__'

    def check_empty(self, data):
        if not data.get('mall_name'):
            raise serializers.ValidationError("Mall name cannot be empty.")
        if not data.get('address'):
            raise serializers.ValidationError("Address cannot be empty.")
        if not data.get('city'):
            raise serializers.ValidationError("City cannot be empty.")
        return data

    def check_exists(self, data):
        mall_name = data.get('mall_name')
        address = data.get('address')
        city = data.get('city')
        if Mall.objects.filter(mall_name=mall_name, address=address, city=city).exists():
            raise serializers.ValidationError("Mall with this name, address, and city already exists.")
        return data   

class MarketSerializer(serializers.ModelSerializer):
    """Convert a Market object to json format, received request and return responce, also have validation checking logic."""
    class Meta:
        model = Market
        fields = '__all__'

    def check_empty(self, data):
        if not data.get('title'):
            raise serializers.ValidationError("Title cannot be empty.")
        if not data.get('start_time'):
            raise serializers.ValidationError("Start date cannot be empty.")
        if not data.get('end_time'):
            raise serializers.ValidationError("End date cannot be empty.")
        return data

    def check_exists(self, data):
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        if Market.objects.filter(start_time=start_time, end_time=end_time).exists():
            raise serializers.ValidationError("Market with this start date and end date already exists.")
        return data

class BoothSerializer(serializers.ModelSerializer):
    """Convert a Booth object to json format, received request and return responce, also have validation checking logic."""
    class Meta:
        model = Booth
        fields = '__all__'

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be a positive number.")
        return value

    def validate_booth_number(self, value):
        if not value.isdigit() and len(value) > 0:
            raise serializers.ValidationError("Booth number must contain only digits.")
        return value

    def check_empty(self, data):
        if not data.get('booth_number'):
            raise serializers.ValidationError("Booth number cannot be empty.")
        if not data.get('price'):
            raise serializers.ValidationError("Price cannot be empty.")
        return data

class BookingSerializer(serializers.ModelSerializer):
    """Convert a Booking object to json format, received request and return responce, also have validation checking logic."""
    class Meta:
        model = Booking
        fields = '__all__'

    def validate_booking_status(self, value):
        if value not in ['Pending', 'Approved', 'Rejected']:
            raise serializers.ValidationError("Booking status must be either 'Pending', 'Approved', or 'Rejected'.")
        return value

    def check_exists(self, data):
        booking_id = data.get('booking_id')
        if Booking.objects.filter(booking_id=booking_id).exists():
            raise serializers.ValidationError("Booking with this ID already exists.")
        return data

    def check_empty(self, data):
        if not data.get('mar_id'):
            raise serializers.ValidationError("Market ID cannot be empty.")
        if not data.get('booth_id'):
            raise serializers.ValidationError("Booth ID cannot be empty.")
        if not data.get('ven_id'):
            raise serializers.ValidationError("Vendor ID cannot be empty.")
        return data

class InvoiceSerializer(serializers.ModelSerializer):
    """Convert an Invoice object to json format, received request and return responce, also have validation checking logic."""
    class Meta:
        model = Invoice
        fields = '__all__'

    def check_exists(self, data):
        inv_id = data.get('inv_id')
        if Invoice.objects.filter(inv_id=inv_id).exists():
            raise serializers.ValidationError("Invoice with this ID already exists.")
        return data

    def check_empty(self, data):
        if not data.get('booking_id'):
            raise serializers.ValidationError("Booking ID cannot be empty.")
        if not data.get('amount'):
            raise serializers.ValidationError("Amount cannot be empty.")
        return data

    def validate_amount(self, value):
        if value < 0:
            raise serializers.ValidationError("Amount must be a positive number.")
        return value

    def validate(self, attrs):
        amount = attrs.get('amount')
        status_value = attrs.get('status')
        if amount is not None and amount < 0:
            raise serializers.ValidationError("Amount must be a positive number.")
        if status_value not in ['Unpaid', 'Paid']:
            raise serializers.ValidationError("Status must be either 'Unpaid' or 'Paid'.")
        return attrs