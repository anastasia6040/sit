import csv
from environment.models import Country, Region, City, EnvironmentalData

with open('data/environment.csv', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        if not row['Region']:
            continue

        country, _ = Country.objects.get_or_create(
            name=row['Country']
        )

        region, _ = Region.objects.get_or_create(
            name=row['Region'],
            country=country
        )

        city, _ = City.objects.get_or_create(
            name=row['City'],
            region=region
        )

        EnvironmentalData.objects.create(
            city=city,
            air_quality=float(row['AirQuality']),
            water_pollution=float(row['WaterPollution'])
        )
