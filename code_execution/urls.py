from django.urls import path
from .views import ExecuteCode

urlpatterns = [
    path('execute/', ExecuteCode.as_view(), name='execute_code'),
]