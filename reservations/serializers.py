from rest_framework import serializers
from .models import Reservation, Listing


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['id', 'name', 'start_time', 'end_time']

    def validate(self, data):
        if data['start_time'] >= data['end_time']:
            raise serializers.ValidationError('End time must be after start time')
        return data


class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listing
        fields = '__all__'
