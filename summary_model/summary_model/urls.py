"""
URL configuration for summary_model project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from summary.views import *

urlpatterns = [
    path('api/v1/meetings/<int:meeting_id>/summary/', Summary.as_view(), name='summary'),
    path('api/v1/meetings/<int:meeting_id>/update_summary/', SummaryUpdateView.as_view(), name='summary_update'),
]