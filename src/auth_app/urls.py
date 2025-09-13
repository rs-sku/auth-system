from rest_framework.routers import DefaultRouter

from auth_app.views import RightViewSet, StatusViewSet, UserViewSet

router = DefaultRouter()
router.register("users", UserViewSet, basename="users")
router.register("statuses", StatusViewSet, basename="statuses")
router.register("rights", RightViewSet, basename="rights")

urlpatterns = router.urls
