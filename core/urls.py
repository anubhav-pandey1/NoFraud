from django.urls import path

from core.views import AttemptTransactionView

urlpatterns = [
    path("check-fraud/", AttemptTransactionView.as_view(), name="check-fraud"),
]
