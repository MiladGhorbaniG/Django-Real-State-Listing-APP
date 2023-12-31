from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Listing, Reservation
from .serializers import ReservationSerializer

class ReservationCreateView(APIView):
    def post(self, request, listing_id):
        listing = Listing.objects.get(id=listing_id)
        serializer = ReservationSerializer(data=request.data)
        if serializer.is_valid():
            reservation = serializer.save(listing=listing)
            return Response({'reservation_id': reservation.id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
