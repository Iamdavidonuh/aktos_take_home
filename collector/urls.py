from rest_framework import routers

from collector import viewsets

app_name = "collector"

router = routers.DefaultRouter()


router.register("consumers", viewsets.ConsumersViewset, basename="consumers")


urlpatterns = []


urlpatterns += router.urls
