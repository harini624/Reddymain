from django.urls import path

from . import views


urlpatterns = [

    path(
        '',
        views.home,
        name='home'
    ),

    path(
        'register/',
        views.register_view,
        name='register'
    ),

    path(
        'login/',
        views.login_view,
        name='login'
    ),

    path(
        'logout/',
        views.logout_view,
        name='logout'
    ),

    path(
        'properties/',
        views.properties,
        name='properties'
    ),

    path(
        'property/<int:pk>/',
        views.property_detail,
        name='property_detail'
    ),
    path(
        'save-property/<int:pk>/',
        views.save_property,
        name='save_property'
    ),

    path(
        'dashboard/',
        views.dashboard,
        name='dashboard'
    ),

    path(
        'contact/',
        views.contact,
        name='contact'
    ),
    path(
        "api/receive-property/",
        views.receive_property,
        name="receive_property"
    ),
    
]

