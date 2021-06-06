from users import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'users', views.UserViewSet, basename='users')

urlpatterns = router.urls