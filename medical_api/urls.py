from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView)
from medical.views import (
    run_analysis_api, CustomTokenObtainPairView, RFResultView,
    YProbResultView, CombinedDataView)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/run-analysis/', run_analysis_api),
    path('api/rf_result/', RFResultView.as_view()),
    path('api/y_result/', YProbResultView.as_view()),
    path('api/data/', CombinedDataView.as_view()),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
