import io
from django.template.loader import render_to_string
from django.http import HttpResponse, JsonResponse, FileResponse
from django.views import View
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import Table, TableStyle
from rest_framework import filters, generics
from .models import Listing, Reservation
from .serializers import ReservationSerializer, ListingSerializer


class ReservationCreateView(APIView):
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['start_time', 'end_time']

    def post(self, request, listing_id):
        listing = get_object_or_404(Listing, id=listing_id)

        serializer = ReservationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        reservation = serializer.save(listing_id=listing_id)

        return Response({'reservation_id': reservation.id})

    def get(self, request, listing_id):
        listing = get_object_or_404(Listing, id=listing_id)
        reservations = Reservation.objects.filter(listing=listing)

        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data)

class AvailabilityCheckView(APIView):
    def post(self, request, listing_id):
        listing = get_object_or_404(Listing, id=listing_id)
        print('Request data:', request.data)

        start_time = request.data.get('start_time', None)
        end_time = request.data.get('end_time', None)
        print('Start time:', start_time)
        print('End time:', end_time)

        reservations = Reservation.objects.filter(listing=listing, start_time__lte=end_time, end_time__gte=start_time)
        print('Reservations:', reservations)

        available = reservations.count() == 0
        return Response({'available': available})

class ListingCreateView(APIView):
    def post(self, request, format=None):
        serializer = ListingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def get(self, request, format=None):
        listings = Listing.objects.all()
        serializer = ListingSerializer(listings, many=True)
        return Response(serializer.data)

class ListingView(APIView):
    def get(self, request, pk):
        listing = get_object_or_404(Listing, pk=pk)
        serializer = ListingSerializer(listing)
        return Response(serializer.data)

    def post(self, request):
        serializer = ListingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

class ReservationReportView(APIView):

    def get(self, request, **kwargs):
        format = kwargs.get('report_format')
        print("ReservationReportView.get() called")

        listings = Listing.objects.all()
        reservations = Reservation.objects.all()

        response = []
        for listing in listings:
            listing_reservations = reservations.filter(listing=listing)
            listing_data = {
                'name': listing.name,
                'reservations': []
            }
            for reservation in listing_reservations:
                reservation_data = {
                    'name': reservation.name,
                    'start_time': reservation.start_time,
                    'end_time': reservation.end_time
                }
                listing_data['reservations'].append(reservation_data)
            response.append(listing_data)

        if format == 'html':
            if response:
                html = render_to_string('reservation_report.html', {'listings': response})
                return HttpResponse(html)
            else:
                return HttpResponse('There are no reservations in the database.')
        elif format == 'pdf':
            buffer = io.BytesIO()
            p = canvas.Canvas(buffer, pagesize=letter)

            # Add title and date to the report
            p.setFont('Helvetica-Bold', 16)
            p.drawString(0.5 * inch, 10 * inch, "Reservation Report")
            p.setFont('Helvetica', 12)
            p.drawString(0.5 * inch, 9.75 * inch, "Date: May 13, 2023")

            y = 9 * inch
            for listing_data in response:
                # Add listing name to the report
                p.setFont('Helvetica-Bold', 12)
                p.drawString(0.5 * inch, y, listing_data['name'])
                y -= 0.5 * inch

                # Add reservations table to the report
                data = [['Guest Name', 'Start Date', 'End Date']]
                for reservation_data in listing_data['reservations']:
                    data.append([reservation_data['name'], reservation_data['start_time'], reservation_data['end_time']])
                table = Table(data)
                table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                    ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 1), (-1, -1), 10),
                    ('RIGHTPADDING', (0, 1), (-1, -1), 5),
                    ('LEFTPADDING', (0, 1), (-1, -1), 5),
                    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.whitesmoke, colors.white]),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ]))
                table.wrapOn(p, 7.5 * inch, 9 * inch)
                table.drawOn(p, 0.5 * inch, y - table._height)

                y -= table._height + 0.5 * inch

            p.showPage()
            p.save()
            buffer.seek(0)
            return FileResponse(buffer, as_attachment=True, filename='reservation_report.pdf')
        else:
            return JsonResponse(response, safe=False)
        
