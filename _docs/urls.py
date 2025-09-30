from rest_framework.routers import DefaultRouter
from .views import DocsViewSet

router = DefaultRouter()
router.register(r'documents', DocsViewSet, basename='document')

urlpatterns = router.urls