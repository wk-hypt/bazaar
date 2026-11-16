from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from decimal import Decimal, InvalidOperation
from .models import Vendor, Item, Organizer, Mall, Market, Booth, Booking, Invoice
from .pages import next_booth_number, next_code
from .serializer import VendorSerializer, ItemSerializer, OrganizerSerializer, MallSerializer, MarketSerializer, BoothSerializer, BookingSerializer, InvoiceSerializer
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

#=================// Vendor API //==================
@api_view(['GET', 'POST'])
def vendors_create(request):
    """Get all vendors data, or create one vendor."""
    if request.method == 'GET':
        vendors = Vendor.objects.all()
        serializer = VendorSerializer(vendors, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = VendorSerializer(data = request.data)
        if serializer.is_valid() and serializer.check_exists(serializer.validated_data) and serializer.validate_phone(serializer.validated_data.get('phone')):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def vendor_detail(request, pk):
    """Get, update, or delete one vendor."""
    try:
        vendors = Vendor.objects.get(pk=pk)
    except Vendor.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = VendorSerializer(vendors)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = VendorSerializer(vendors, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return(Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST))

    elif request.method == 'DELETE':
        vendors.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#=================// Item API //==================
@api_view(['GET', 'POST'])
def items_create(request):
    """Get all items, or create one item and assign the next id."""
    if request.method == 'GET':
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = request.data.copy()
        if not data.get('item_id'):
            data['item_id'] = next_code('I', Item, 'item_id')
        serializer = ItemSerializer(data=data)
        if serializer.is_valid() and serializer.validate_price(serializer.validated_data.get('price')) and serializer.validate_item_from_vendor(serializer.validated_data):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT', 'DELETE'])
def item_detail(request, pk):
    """Get, update, or delete one item."""
    try:
        items = Item.objects.get(pk=pk)
    except Item.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ItemSerializer(items)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = ItemSerializer(items, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return(Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST))

    elif request.method == 'DELETE':
        items.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#=================// Organizer API //==================
@api_view(['GET', 'POST'])
def organizers_create(request):
    """Get all organizers data, or create one organizer."""
    if request.method == 'GET':
        organizers = Organizer.objects.all()
        serializer = OrganizerSerializer(organizers, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = OrganizerSerializer(data = request.data)
        if serializer.is_valid() and serializer.validate_phone(serializer.validated_data.get('phone')):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT', 'DELETE'])
def organizer_detail(request, pk):
    """Get, update, or delete one organizer."""
    try:
        organizers = Organizer.objects.get(pk=pk)
    except Organizer.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = OrganizerSerializer(organizers)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = OrganizerSerializer(organizers, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return(Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST))

    elif request.method == 'DELETE':
        organizers.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#=================// Mall API //==================
@api_view(['GET', 'POST'])
def malls_create(request):
    """Get all malls data, or create one mall."""
    if request.method == 'GET':
        malls = Mall.objects.all()
        serializer = MallSerializer(malls, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = MallSerializer(data = request.data)
        if serializer.is_valid() and serializer.check_empty(serializer.validated_data) and serializer.check_exists(serializer.validated_data):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT', 'DELETE'])
def mall_detail(request, pk):
    """Get, update, or delete one mall."""
    try:
        malls = Mall.objects.get(pk=pk)
    except Mall.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MallSerializer(malls)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = MallSerializer(malls, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return(Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST))

    elif request.method == 'DELETE':
        malls.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#=================// Market API //==================
@api_view(['GET', 'POST'])
def markets_create(request):
    """Get all markets data, or create one market."""
    if request.method == 'GET':
        markets = Market.objects.all()
        serializer = MarketSerializer(markets, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = MarketSerializer(data = request.data)
        if serializer.is_valid() and serializer.check_empty(serializer.validated_data) and serializer.check_exists(serializer.validated_data):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT', 'DELETE'])
def market_detail(request, pk):
    """Get, update, or delete one market."""
    try:
        markets = Market.objects.get(pk=pk)
    except Market.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = MarketSerializer(markets)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = MarketSerializer(markets, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return(Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST))

    elif request.method == 'DELETE':
        markets.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#=================// Booth API //==================
@api_view(['GET', 'POST'])
def booths_create(request):
    """Get all booths, or create several booths from a quantity."""
    if request.method == 'GET':
        booths = Booth.objects.all()
        serializer = BoothSerializer(booths, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        mall = Mall.objects.filter(pk=request.data.get('mall_id')).first()
        if mall is None:
            return Response({"mall_id": ["Choose a mall."]}, status=status.HTTP_400_BAD_REQUEST)
        raw_quantity = request.data.get('quantity')
        if isinstance(raw_quantity, bool) or not (isinstance(raw_quantity, int) or (isinstance(raw_quantity, str) and raw_quantity.isdigit())):
            return Response({"quantity": ["Enter how many booths to create."]}, status=status.HTTP_400_BAD_REQUEST)
        quantity = int(raw_quantity)
        if quantity < 1 or quantity > 100:
            return Response({"quantity": ["Enter a quantity from 1 to 100."]}, status=status.HTTP_400_BAD_REQUEST)
        try:
            price = Decimal(str(request.data.get('price')))
        except (InvalidOperation, TypeError):
            return Response({"price": ["Price must be a positive number."]}, status=status.HTTP_400_BAD_REQUEST)
        if price <= 0:
            return Response({"price": ["Price must be a positive number."]}, status=status.HTTP_400_BAD_REQUEST)
        created = []
        for _ in range(quantity):
            booth = Booth.objects.create(
                booth_id=next_code('B', Booth, 'booth_id'),
                mall_id=mall,
                price=price,
                booth_number=next_booth_number(mall),
            )
            created.append(booth)
        return Response(BoothSerializer(created, many=True).data, status=status.HTTP_201_CREATED)
    
@api_view(['GET', 'PUT', 'DELETE'])
def booth_detail(request, pk):
    """Get, update, or delete one booth."""
    try:
        booths = Booth.objects.get(pk=pk)
    except Booth.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BoothSerializer(booths)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = BoothSerializer(booths, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return(Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST))

    elif request.method == 'DELETE':
        booths.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#=================// Booking API //==================
@api_view(['GET', 'POST'])
def bookings_create(request):
    """Get all bookings, or create one booking and assign the next id."""
    if request.method == 'GET':
        items = Booking.objects.all()
        serializer = BookingSerializer(items, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        data = request.data.copy()
        if not data.get('booking_id'):
            data['booking_id'] = next_code('BK', Booking, 'booking_id')
        serializer = BookingSerializer(data=data)
        if serializer.is_valid() and serializer.validate_booking_status(serializer.validated_data.get('booking_status', 'Pending')) and serializer.check_empty(serializer.validated_data) and serializer.check_exists(serializer.validated_data):
            booth = serializer.validated_data.get('booth_id')
            if Booking.objects.filter(booth_id=booth, booking_status='Approved').exists():
                return Response(
                    {"booth_id": ["This booth is already booked."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT', 'DELETE'])
def booking_detail(request, pk):
    """Get, update, or delete one booking."""
    try:
        bookings = Booking.objects.get(pk=pk)
    except Booking.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BookingSerializer(bookings)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = BookingSerializer(bookings, data=request.data)
        if serializer.is_valid():
            saved = serializer.save()
            if saved.booking_status == 'Approved':
                Booking.objects.filter(booth_id=saved.booth_id).exclude(pk=saved.pk).exclude(
                    booking_status='Rejected'
                ).update(booking_status='Rejected')
            return Response(BookingSerializer(saved).data)
        return(Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST))

    elif request.method == 'DELETE':
        bookings.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#=================// Invoice API //==================
@api_view(['GET', 'POST'])
def invoices_create(request):
    """Get all invoices data, or create one invoice."""
    if request.method == 'GET':
        invoices = Invoice.objects.all()
        serializer = InvoiceSerializer(invoices, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = InvoiceSerializer(data = request.data)
        if serializer.is_valid() and serializer.check_empty(serializer.validated_data) and serializer.check_exists(serializer.validated_data) and serializer.validate_amount(serializer.validated_data.get('amount')):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT', 'DELETE'])
def invoice_detail(request, pk):
    """Get, update, or delete one invoice."""
    try:
        invoices = Invoice.objects.get(pk=pk)
    except Invoice.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = InvoiceSerializer(invoices)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = InvoiceSerializer(invoices, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return(Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST))

    elif request.method == 'DELETE':
        invoices.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class LoginView(APIView):
    """Check the username and password, then start a session."""
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)

            return Response({
                "message": "Login successful",
                "username": user.username
            })

        return Response(
            {"error": "Invalid username or password"},
            status=status.HTTP_401_UNAUTHORIZED
        )

class LogoutView(APIView):
    """End the current session."""

    def post(self, request):
        logout(request)

        return Response({
            "message": "Logout successful"
        })