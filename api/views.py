from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Vendor, Item, Organizer, Mall, Market, Booth, Booking, Invoice
from .serializer import VendorSerializer, ItemSerializer, OrganizerSerializer, MallSerializer, MarketSerializer, BoothSerializer, BookingSerializer, InvoiceSerializer
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

#=================// Vendor API //==================
@api_view(['GET', 'POST'])
def vendors_create(request):
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
    if request.method == 'GET':
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = ItemSerializer(data = request.data)
        if serializer.is_valid() and serializer.validate_price(serializer.validated_data.get('price')) and serializer.validate_item_from_vendor(serializer.validated_data):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT', 'DELETE'])
def item_detail(request, pk):
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
    if request.method == 'GET':
        booths = Booth.objects.all()
        serializer = BoothSerializer(booths, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = BoothSerializer(data = request.data)
        if serializer.is_valid() and serializer.validate_price(serializer.validated_data.get('price')) and serializer.validate_booth_number(serializer.validated_data.get('booth_number')) and serializer.check_empty(serializer.validated_data):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT', 'DELETE'])
def booth_detail(request, pk):
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

    #=================// Booth API //==================

#=================// Booking API //==================
@api_view(['GET', 'POST'])
def bookings_create(request):
    if request.method == 'GET':
        items = Booking.objects.all()
        serializer = BookingSerializer(items, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = BookingSerializer(data = request.data)
        if serializer.is_valid() and serializer.validate_booking_status(serializer.validated_data.get('booking_status')) and serializer.check_empty(serializer.validated_data) and serializer.check_exists(serializer.validated_data):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET', 'PUT', 'DELETE'])
def booking_detail(request, pk):
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
            serializer.save()
            return Response(serializer.data)
        return(Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST))

    elif request.method == 'DELETE':
        bookings.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#=================// Invoice API //==================
@api_view(['GET', 'POST'])
def invoices_create(request):
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

# Create your views here.
class LoginView(APIView):
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

    def post(self, request):
        logout(request)

        return Response({
            "message": "Logout successful"
        })