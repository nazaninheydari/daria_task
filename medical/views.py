import pandas as pd
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from medical.ml.utils import get_combined_data
from medical.ml.pipeline import run_analysis


class RFResultView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        result = (run_analysis)()
        return Response(result["rf_result"])

class YProbResultView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        result = (run_analysis)()
        return Response({"y_prob": result["y_prob"]})

class CombinedDataView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        df = (get_combined_data)()
        df = df.where(pd.notnull(df), None)
        df = df.fillna('')
        data_json = df.to_dict(orient="records")
        return Response(data_json)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def run_analysis_api(request):
    result = run_analysis()
    return Response(result)

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        username = attrs.get("username")
        User = get_user_model()

        allowed_usernames = ['myuser']
        allowed_emails = ['admin@example.com']

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise self.fail("no_active_account")

        if user.username not in allowed_usernames and user.email not in allowed_emails:
            raise self.fail("no_active_account")

        return super().validate(attrs)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
