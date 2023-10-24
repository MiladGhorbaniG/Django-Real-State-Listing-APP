from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import ReservationCreateView, AvailabilityCheckView, ListingCreateView, ListingView, ReservationReportView

urlpatterns = [
    path('listings/', ListingCreateView.as_view(), name='listing-create'),
    path('listings/<int:pk>/', ListingView.as_view(), name='listing-list'),
    path('listings/<int:listing_id>/reservations/', ReservationCreateView.as_view(), name='reservation-create'),
    path('listings/<int:listing_id>/availability/', AvailabilityCheckView.as_view(), name='availability-check'),
    path('report/', ReservationReportView.as_view(), name='reservation_report'),
    path('report/<str:report_format>/', ReservationReportView.as_view(), name='reservation_report_format'),
]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html', 'pdf'])
