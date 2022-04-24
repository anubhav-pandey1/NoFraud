from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from core.services.fraud_detection import FraudDetection
from core.serializers import TransactionSerializer
from core.choices import TransactionStatusChoices

# Create your views here.


class AttemptTransactionView(APIView):
    """Attempt a transaction and check if it's fraudulent"""

    def post(self, request):
        params = dict(request.data)
        serializer = TransactionSerializer(data=params)
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return self._fraud_status(serializer)

    def _fraud_status(self, serializer):
        is_fraud = FraudDetection(serializer.validated_data)()
        if is_fraud:
            serializer.validated_data["status"] = TransactionStatusChoices.TERRORIST
            serializer.save()
            return Response(
                data={"message": "Terrorist Spotted"}, status=status.HTTP_403_FORBIDDEN
            )
        serializer.validated_data["status"] = TransactionStatusChoices.NOT_TERRORIST
        serializer.save()
        return Response(
            data={"message": "Not A Terrorist"}, status=status.HTTP_202_ACCEPTED
        )
