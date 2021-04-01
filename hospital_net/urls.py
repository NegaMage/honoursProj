"""hospital_net URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('logout', views.logout_request, name="logout"),
    path('', views.homepage),


    path('cleanhospinv', views.clean_hosp_inv),
    path('fillhospinv', views.fill_hosp_inv),


    path('metric_01/<hospital>/', views.metric_01_viewpage),
    path('metric_01/', views.metric_01_viewpage),

    path('metric_02/<hospital>/', views.metric_02_viewpage),
    path('metric_02/', views.metric_02_viewpage),

    path('fillsuppinv', views.fill_supp_inv),
    path('resetsuppstorage', views.reset_supp_storage),

    path('metric_03/<supplier>/', views.metric_03_viewpage),
    path('metric_03/', views.metric_03_viewpage),

    path('metric_04/<supplier>/', views.metric_04_viewpage),
    path('metric_04/', views.metric_04_viewpage),

    path('metric_05/<hospital>/', views.metric_05_viewpage),
    path('metric_05/', views.metric_05_viewpage),

    path('metric_06/<hospital>/', views.metric_06_viewpage),
    path('metric_06/', views.metric_06_viewpage),

    path('add_manuf_data/', views.fill_manuf_making),

    path('metric_07/<manuf>/', views.metric_07_viewpage),
    path('metric_07/', views.metric_07_viewpage),

    path('metric_08/<hospital>/', views.metric_08_viewpage),
    path('metric_08/', views.metric_08_viewpage),
]
