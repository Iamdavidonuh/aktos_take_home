from rest_framework import routers

from collector import viewsets

app_name = "collector"  # pylint: disable=invalid-name


router = routers.DefaultRouter()


router.register("consumers", viewsets.ConsumersViewset, basename="consumers")

router.register(
    "upload-consumers",
    viewsets.ConsumerBalanceCSVUploadViewset,
    basename="upload-consumers",
)


urlpatterns = []


urlpatterns += router.urls
