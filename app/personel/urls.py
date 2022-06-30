"""
URL mappings for the recipe app.
"""

from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from personel import views

router =DefaultRouter()
router.register('personel', views.PersonelViewSet)

app_name = 'personel'

urlpatterns = [
    path('', include(router.urls)),
]
