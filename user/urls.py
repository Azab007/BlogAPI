from django.urls import include, path
from rest_framework_simplejwt import views as jwt_views
from .views import UserViewSet
from rest_framework.routers import DefaultRouter



router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include(router.urls)),
]