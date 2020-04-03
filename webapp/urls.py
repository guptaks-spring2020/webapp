"""webapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from bills.api.views import manage_user_bill_by_id, get_bills_view, create_bill_view, FileView, BillDueView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('v1/', include('account.api.urls', 'account_api')),
    path('v1/bills', get_bills_view, name="get_bills" ),
    path('v1/bill/<uuid:id>', manage_user_bill_by_id, name="bill_id_operations"),
    path('v1/bill/', create_bill_view, name="post_bill"),
    path('v1/bill/<uuid:id>/file', FileView.as_view()),
    path('v1/bill/<uuid:id>/file/<uuid:bill_file_id>', FileView.as_view()),
    path('v1/bills/due/<int:days>', BillDueView.as_view())
]