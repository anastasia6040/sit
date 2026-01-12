from django.db import models

class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Region(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.country})"


class City(models.Model):
    name = models.CharField(max_length=100)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class EnvironmentalData(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    air_quality = models.FloatField()
    water_pollution = models.FloatField()

    def __str__(self):
        return f"{self.city}"
