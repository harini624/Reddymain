from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .forms import RegisterForm
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
from .models import Properties,PropertyImage,SavedProperty
from decimal import Decimal, InvalidOperation
from django.db import transaction



def home(request):
    received_properties = Properties.objects.filter(
        source_property_id__isnull=False,
        published=True,
        available=True
    ).order_by('-id')

    # Show featured received properties first.
    featured_properties = received_properties.filter(
        is_featured=True
    )[:6]

    # If no properties are marked featured, show the latest
    # received properties instead.
    if not featured_properties.exists():
        featured_properties = received_properties[:6]

    latest_properties = received_properties[:6]

    return render(
        request,
        'home.html',
        {
            'featured_properties': featured_properties,
            'latest_properties': latest_properties,
        }
)

def register_view(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':

        form = RegisterForm(request.POST)

        if form.is_valid():

            user = form.save()

            login(request, user)

            messages.success(
                request,
                'Account created successfully!'
            )

            send_mail(
            'Registration',
            'Hi {},\n\nRegistration done successfully. Thank you for registering.'.format(user.username),
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False
             )

            return redirect('home')

    else:

        form = RegisterForm()

    return render(
        request,
        'register.html',
        {
            'form': form
        }
    )


def login_view(request):

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect('home')

        messages.error(
            request,
            'Invalid username or password.'
        )

    return render(
        request,
        'login.html'
    )


@login_required
def logout_view(request):

    logout(request)

    return redirect('home')



def properties(request):
    property_list = Properties.objects.filter(
        published=True,
        available=True
    )

    query = request.GET.get('q', '')
    purpose = request.GET.get('purpose', '')
    property_type = request.GET.get('type', '')

    if query:
        property_list = property_list.filter(
            Q(title__icontains=query) |
            Q(location__icontains=query) |
            Q(city__icontains=query)
        )

    if purpose:
        property_list = property_list.filter(
            purpose=purpose
        )

    if property_type:
        property_list = property_list.filter(
            property_type=property_type
        )

    return render(
        request,
        'properties.html',
        {
            'properties': property_list,
            'query': query,
            'purpose': purpose,
            'property_type': property_type
        }
    )

def property_detail(request, pk):
    property_obj = get_object_or_404(
        Properties,
        pk=pk,
        source_property_id__isnull=False,
        published=True,
        available=True
    )

    print("Property ID:", property_obj.id)
    print("Source Property ID:", property_obj.source_property_id)
    print("Gallery image count:", property_obj.images.count())

    for image in property_obj.images.all():
        print(
            "Image type:", image.image_type,
            "| Image URL:", image.image.url if image.image else "No image"
        )

    return render(
        request,
        'properties_detail.html',
        {
            'property': property_obj,
            'is_saved': False,
        }
    )

@login_required
def post_property(request):

    if request.method == 'POST':

        form = PropertyForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            property_obj = form.save(
                commit=False
            )

            property_obj.owner = request.user

            property_obj.save()

            messages.success(
                request,
                'Property posted successfully!'
            )

            return redirect(
                'property_detail',
                pk=property_obj.pk
            )

    else:

        form = PropertyForm()

    return render(
        request,
        'post_property.html',
        {
            'form': form
        }
    )


@login_required
def save_property(request, pk):

    property_obj = get_object_or_404(
        Properties,
        pk=pk
    )

    saved, created = SavedProperty.objects.get_or_create(
        user=request.user,
        property=property_obj
    )

    if not created:

        saved.delete()

        messages.info(
            request,
            'Property removed from saved properties.'
        )

    else:

        messages.success(
            request,
            'Property saved successfully.'
        )

    return redirect(
        'property_detail',
        pk=pk
    )


@login_required
def dashboard(request):
    saved_properties = SavedProperty.objects.filter(
        user=request.user
    ).select_related('property')

    return render(
        request,
        'dashboard.html',
        {
            'saved_properties': saved_properties,
        }
    )

def contact(request):

    if request.method == "POST":

        name = request.POST.get("name","")
        email = request.POST.get("email","")
        user_message = request.POST.get("message","")

        email_message = (
            "New message from your website\n\n"
            "Name: " + name + "\n"
            "Email: " + email + "\n"
            "Message:\n" + user_message
        )   
        send_mail(
            "New Contact Message",
            email_message,
            settings.DEFAULT_FROM_EMAIL,
            settings.CONTACT_EMAILS,
            fail_silently=False,
        )
        messages.success(
            request,
            "Your message has been sent successfully!"
        )

        return redirect("contact")

    return render(request, "contact.html")

@csrf_exempt
def receive_property(request):
    if request.method != "POST":
        return JsonResponse(
            {"error": "POST method required"}, status=405
        )

    token = getattr(settings, "RECEIVE_PROPERTY_API_TOKEN", "")
    if not token or request.headers.get("Authorization") != f"Bearer {token}":
        return JsonResponse({"error": "Unauthorized"}, status=401)

    try:
        source_id = int(request.POST.get("source_property_id", ""))
        title = request.POST.get("furnished", "").strip()
        location = request.POST.get("location", "").strip()
        price = Decimal(request.POST.get("price", ""))
        bhk = int(request.POST.get("bhk", "0"))

        if source_id <= 0 or not title or not location:
            return JsonResponse(
                {"error": "Property ID, title and location are required"},
                status=400
            )

        if not price.is_finite() or price < 0 or bhk < 0:
            return JsonResponse(
                {"error": "Invalid price or BHK value"}, status=400
            )

        with transaction.atomic():
            prop, created = Properties.objects.update_or_create(
                source_property_id=source_id,
                defaults={
                    "furnished": title,
                    "title": title,
                    "location": location,
                    "price": price,
                    "bhk": bhk,
                    "contact": request.POST.get("contact", ""),
                    "published": request.POST.get("published", "false").lower() == "true",
                    "available": request.POST.get("available", "true").lower() == "true",
                    "purpose": "",
                    "property_type": "",
                    "city": "",
                    "description": "",
                }
            )

            for field_name in ("house_image", "hall_image"):
                uploaded = request.FILES.get(field_name)
                if uploaded:
                    getattr(prop, field_name).save(
                        uploaded.name, uploaded, save=True
                    )

            # Replace the receiver gallery with the sender's current gallery.
            # Main images are kept in their separate fields.
            PropertyImage.objects.filter(property=prop).delete()

            gallery_indexes = sorted({
                int(key.split("_")[1])
                for key in request.FILES
                if key.startswith("gallery_")
                and key.split("_")[1].isdigit()
            })

            for index in gallery_indexes:
                uploaded = request.FILES.get(f"gallery_{index}")
                if uploaded:
                    image_type = request.POST.get(
                        f"gallery_type_{index}", "gallery"
                    )[:20]

                    gallery_image = PropertyImage(
                        property=prop,
                        image_type=image_type,
                    )
                    gallery_image.image.save(
                        uploaded.name, uploaded, save=True
                    )

        return JsonResponse({
            "success": True,
            "created": created,
            "property_id": prop.pk,
            "message": "Property and images synchronized",
        })

    except (ValueError, TypeError, InvalidOperation):
        return JsonResponse(
            {"error": "Invalid property data"}, status=400
        )
    except Exception:
        # Details are intentionally not exposed to the remote sender.
        return JsonResponse(
            {"error": "Property synchronization failed"}, status=500
        )
@csrf_exempt
def update_property_status(request):
    if request.method != "POST":
        return JsonResponse(
            {"error": "POST method required"},
            status=405
        )

    token = getattr(settings, "RECEIVE_PROPERTY_API_TOKEN", "")

    if (
        not token
        or request.headers.get("Authorization")
        != "Bearer " + token
    ):
        return JsonResponse(
            {"error": "Unauthorized"},
            status=401
        )

    try:
        source_id = int(request.POST.get("source_property_id", ""))

        available_value = request.POST.get("available", "").lower()
        published_value = request.POST.get("published", "").lower()

        if available_value not in ("true", "false"):
            return JsonResponse(
                {"error": "Invalid availability status"},
                status=400
            )

        if published_value not in ("true", "false"):
            return JsonResponse(
                {"error": "Invalid publishing status"},
                status=400
            )

        property_obj = get_object_or_404(
            Properties,
            source_property_id=source_id
        )

        property_obj.available = available_value == "true"
        property_obj.published = published_value == "true"

        property_obj.save(
            update_fields=["available", "published"]
        )

        return JsonResponse({
            "success": True,
            "property_id": property_obj.id,
            "available": property_obj.available,
            "published": property_obj.published
        })

    except (ValueError, TypeError):
        return JsonResponse(
            {"error": "Invalid property ID"},
            status=400
        )