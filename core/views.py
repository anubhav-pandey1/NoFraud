from rest_framework.response import Response
from rest_framework.views import APIView

from core.services.fraud_detection import FraudDetection
from core.serializers import TransactionSerializer
from core.choices import TransactionStatusChoices

# Create your views here.


class AttemptTransactionView(APIView):
    """Attempt a transaction and check if it's fraudulent"""

    def post(self, request):
        params = dict(request.data)
        serializer = TransactionSerializer(params)
        if not serializer.is_valid():
            return Response(data={"message": "Invalid request paramaters"})
        return self._fraud_status(serializer)

    def _fraud_status(self, serializer):
        is_fraud = FraudDetection(dict(serializer.validated_data))
        if is_fraud:
            serializer.data["status"] = TransactionStatusChoices.TERRORIST
            serializer.save()
            return Response(data={"message": "Terrorist Spotted"})
        serializer.data["status"] = TransactionStatusChoices.NOT_TERRORIST
        serializer.save()
        return Response(data={"message": "Not A Terrorist"})
