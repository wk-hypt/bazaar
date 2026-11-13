from rest_framework import serializers
from .models import Vendor, Item, Organizer, Mall, Market, Booth, Booking, Invoice

class VendorSerializer(serializers.ModelSerializer):
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
    class Meta:
        model = Item
        fields = '__all__'

        def validate_price(self, value):
            if value <= 0:
                raise serializers.ValidationError("Price must be a positive number.")
            return value

        def validate_item_from_vendor(self, data):
            ven_id = data.get('ven_id')
            if not Vendor.objects.filter(ven_id=ven_id).exists():
                raise serializers.ValidationError("Vendor does not exist.")
            return data

class OrganizerSerializer(serializers.ModelSerializer):
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
    class Meta:
        model = Market
        fields = '__all__'

    def check_empty(self, data):
        if not data.get('title'):
            raise serializers.ValidationError("Title cannot be empty.")
        if not data.get('start_time'):
            raise serializers.ValidationError("Start time cannot be empty.")
        if not data.get('end_time'):
            raise serializers.ValidationError("End time cannot be empty.")
        return data

    def check_exists(self, data):
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        if Market.objects.filter(start_time=start_time, end_time=end_time).exists():
            raise serializers.ValidationError("Market with this start time and end time already exists.")
        return data

class BoothSerializer(serializers.ModelSerializer):
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
    class Meta:
        model = Invoice
        fields = '__all__'

    def check_exists(self, data):
        invoice_id = data.get('invoice_id')
        if Invoice.objects.filter(invoice_id=invoice_id).exists():
            raise serializers.ValidationError("Invoice with this ID already exists.")
        return data

    def check_empty(self, data):
        if not data.get('booking_id'):
            raise serializers.ValidationError("Booking ID cannot be empty.")
        if not data.get('amount'):
            raise serializers.ValidationError("Amount cannot be empty.")
        return data

    def validate(self):
        if self.instance.amount < 0:
            raise serializers.ValidationError("Amount must be a positive number.")
        elif self.instance.status not in ['Unpaid', 'Paid']:
            raise serializers.ValidationError("Status must be either 'Unpaid' or 'Paid'.")