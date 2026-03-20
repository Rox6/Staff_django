from django.urls import path
from staff.views import staff_create, staff_list, staff_update, staff_delete

urlpatterns = [
    path('', staff_list, name='staff_list'),
    path('neu/', staff_create, name='staff_create'),
    path('bearbeiten/<int:pk>/', staff_update, name='staff_update'),
    path('loeschen/<int:pk>/', staff_delete, name='staff_delete'),
]