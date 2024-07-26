from django.urls import path

from . import views

app_name = "survey"

urlpatterns = [
    path(
        "",
        view=views.NationalParkSatisfactionBehaviorView.as_view(),
    ),
    path(
        "park/survey",
        view=views.NationalParkSatisfactionBehaviorView.as_view(),
        name="national_park",
    ),
]
