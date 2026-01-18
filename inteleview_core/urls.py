from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('landing.urls', namespace='landing')),  # your landing/home page
    path('users/', include('users.urls', namespace='users')),  # <--- important!
    path('admin-panel/', include('admin_panel.urls')),
    path('testsystem/', include('testsystem.urls')),
    path('dashboard/', include('dashboard.urls', namespace='dashboard')),
    path('aptitude/', include('aptitude.urls', namespace='aptitude')),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('technical/', include('technical.urls' , namespace='technical')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('chatbot/', include('chatbot.urls')),
    path('GD/', include('GD.urls')), 
]

# Media serving during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)