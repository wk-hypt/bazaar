from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group, User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from api.models import Booking, Booth, Market, Organizer, Vendor


def next_code(prefix, model, field):
    """Return the next id such as V002 or BK003 for a string primary key."""
    numbers = []
    for value in model.objects.values_list(field, flat=True):
        suffix = value[len(prefix):]
        if value.startswith(prefix) and suffix.isdigit():
            numbers.append(int(suffix))
    return f"{prefix}{max(numbers, default=0) + 1:03d}"


def next_booth_number(mall):
    """Return the next booth number for this mall, starting at 1."""
    numbers = []
    for value in Booth.objects.filter(mall_id=mall).values_list('booth_number', flat=True):
        if str(value).isdigit():
            numbers.append(int(value))
    return str(max(numbers, default=0) + 1)


ROLES = ('organizer', 'vendor')


def account_role(user):
    """Return organizer or vendor when that group is on the user."""
    names = set(user.groups.values_list('name', flat=True))
    if 'organizer' in names:
        return 'organizer'
    if 'vendor' in names:
        return 'vendor'
    return None


def assign_role(user, role):
    """Attach the organizer or vendor group to this user."""
    group, _ = Group.objects.get_or_create(name=role)
    user.groups.add(group)


def login_page(request):
    """Show organizer and vendor on the login form, then start a session."""
    if request.user.is_authenticated and account_role(request.user):
        return redirect('home')

    error = None
    username = ''
    role = ''
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        role = request.POST.get('role', '')
        user = authenticate(request, username=username, password=password)
        if role not in ROLES:
            error = 'Choose organizer or vendor.'
        elif user is None:
            error = 'Invalid username or password.'
        else:
            current = account_role(user)
            if current is None:
                assign_role(user, role)
            elif current != role:
                error = f'This account is registered as {current}.'
            if error is None:
                login(request, user)
                return redirect('home')

    return render(request, 'login.html', {'error': error, 'username': username, 'role': role})


def register_page(request):
    """Create a user, store the hashed password, and save the chosen role."""
    if request.user.is_authenticated and account_role(request.user):
        return redirect('home')

    error = None
    username = ''
    role = ''
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        confirm = request.POST.get('confirm_password', '')
        role = request.POST.get('role', '')
        full_name = request.POST.get('full_name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        if role not in ROLES:
            error = 'Choose organizer or vendor.'
        elif not username:
            error = 'Username is required.'
        elif not full_name or not email:
            error = 'Name and email are required.'
        elif not phone.isdigit() or len(phone) not in (10, 11):
            error = 'Phone number must be 10 or 11 digits.'
        elif password != confirm:
            error = 'Passwords do not match.'
        elif User.objects.filter(username=username).exists():
            error = 'That username is already taken.'
        elif role == 'vendor' and Vendor.objects.filter(email=email).exists():
            error = 'Email already exists.'
        elif role == 'organizer' and Organizer.objects.filter(email=email).exists():
            error = 'Email already exists.'
        else:
            try:
                validate_password(password, User(username=username))
            except ValidationError as exc:
                error = ' '.join(exc.messages)
            else:
                user = User.objects.create_user(username=username, password=password)
                assign_role(user, role)
                if role == 'vendor':
                    Vendor.objects.create(
                        ven_id=next_code('V', Vendor, 'ven_id'),
                        user=user,
                        full_name=full_name,
                        email=email,
                        phone=phone,
                    )
                else:
                    Organizer.objects.create(
                        org_id=next_code('O', Organizer, 'org_id'),
                        user=user,
                        full_name=full_name,
                        email=email,
                        phone=phone,
                    )
                login(request, user)
                return redirect('home')

    return render(request, 'register.html', {
        'error': error,
        'username': username,
        'role': role,
        'full_name': request.POST.get('full_name', ''),
        'email': request.POST.get('email', ''),
        'phone': request.POST.get('phone', ''),
    })


@require_POST
def logout_page(request):
    """End the current session and return to the login page."""
    logout(request)
    return redirect('login')


@login_required
def home_page(request):
    """Show GET and POST forms for the logged-in organizer or vendor."""
    role = account_role(request.user)
    if role is None:
        logout(request)
        return redirect('login')
    organizer = Organizer.objects.filter(user=request.user).first()
    vendor = Vendor.objects.filter(user=request.user).first()
    return render(request, 'home.html', {
        'role': role,
        'org_id': organizer.org_id if organizer else '',
        'ven_id': vendor.ven_id if vendor else '',
    })


def profile_fields(request):
    """Read the name, email, and phone submitted for an organizer or vendor row."""
    return (
        request.POST.get('full_name', '').strip(),
        request.POST.get('email', '').strip(),
        request.POST.get('phone', '').strip(),
    )


@login_required
@require_POST
def save_profile(request):
    """Save the organizer or vendor row for an account that does not have one yet."""
    role = account_role(request.user)
    full_name, email, phone = profile_fields(request)
    if not full_name or not email:
        messages.error(request, 'Name and email are required.')
        return redirect('home')
    if not phone.isdigit() or len(phone) not in (10, 11):
        messages.error(request, 'Phone number must be 10 or 11 digits.')
        return redirect('home')
    if role == 'vendor':
        if Vendor.objects.filter(user=request.user).exists():
            messages.error(request, 'Your vendor record already exists.')
            return redirect('home')
        if Vendor.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('home')
        Vendor.objects.create(
            ven_id=next_code('V', Vendor, 'ven_id'),
            user=request.user,
            full_name=full_name,
            email=email,
            phone=phone,
        )
    elif role == 'organizer':
        if Organizer.objects.filter(user=request.user).exists():
            messages.error(request, 'Your organizer record already exists.')
            return redirect('home')
        if Organizer.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists.')
            return redirect('home')
        Organizer.objects.create(
            org_id=next_code('O', Organizer, 'org_id'),
            user=request.user,
            full_name=full_name,
            email=email,
            phone=phone,
        )
    messages.success(request, 'Your details are saved.')
    return redirect('home')


@login_required
@require_POST
def become_vendor(request):
    """Turn the logged-in user into a vendor row linked by user_id."""
    if Vendor.objects.filter(user=request.user).exists():
        messages.error(request, 'You are already a vendor.')
        return redirect('home')

    full_name = request.POST.get('full_name', '').strip()
    email = request.POST.get('email', '').strip()
    phone = request.POST.get('phone', '').strip()
    if not full_name or not email:
        messages.error(request, 'Name and email are required.')
        return redirect('home')
    if not phone.isdigit() or len(phone) not in (10, 11):
        messages.error(request, 'Phone number must be 10 or 11 digits.')
        return redirect('home')
    if Vendor.objects.filter(email=email).exists():
        messages.error(request, 'Email already exists.')
        return redirect('home')

    Vendor.objects.create(
        ven_id=next_code('V', Vendor, 'ven_id'),
        user=request.user,
        full_name=full_name,
        email=email,
        phone=phone,
    )
    messages.success(request, 'You are now a vendor. You can book a booth.')
    return redirect('home')


@login_required
@require_POST
def create_booking(request):
    """Create a Pending booking for the logged-in user's vendor."""
    vendor = Vendor.objects.filter(user=request.user).first()
    if vendor is None:
        messages.error(request, 'Become a vendor before booking.')
        return redirect('home')

    market = Market.objects.filter(pk=request.POST.get('mar_id')).first()
    booth = Booth.objects.filter(pk=request.POST.get('booth_id')).first()
    if market is None or booth is None:
        messages.error(request, 'Choose a market and a booth.')
        return redirect('home')
    if Booking.objects.filter(booth_id=booth, booking_status='Approved').exists():
        messages.error(request, 'That booth is already booked.')
        return redirect('home')

    Booking.objects.create(
        booking_id=next_code('BK', Booking, 'booking_id'),
        mar_id=market,
        booth_id=booth,
        ven_id=vendor,
        booking_status='Pending',
    )
    messages.success(request, 'Booking submitted and waiting for approval.')
    return redirect('home')
