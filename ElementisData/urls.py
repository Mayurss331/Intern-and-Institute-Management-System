"""
URL configuration for ElementisData project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.conf.urls.static import static
from django.conf import settings

from myapp.views import custom_404

# Force custom handler in debug mode (optional)
handler404 = custom_404

urlpatterns = [
    path('admin/', admin.site.urls),
    path('elementishead/', include('myapp.urls')),  # Include URLs from your app
    path('', include('intern.urls'))  # Include URLs from your app
    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    from django.urls import re_path
    urlpatterns += [
        re_path(r'^.*$', custom_404),  # This will match anything not matched above
    ]