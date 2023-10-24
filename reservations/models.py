from django.db import models

class Listing(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(default='')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
 

       return self.name
class Reservation(models.Model):
    name = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} ({self.start_time} - {self.end_time})'
