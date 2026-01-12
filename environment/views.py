from django.template.response import TemplateResponse
from django.db.models import Avg, Min, Max

from .models import Country, Region, City, EnvironmentalData


def home(request):
    countries = Country.objects.all()
    regions = Region.objects.select_related('country').all()
    cities = City.objects.select_related('region__country').all()
    data = EnvironmentalData.objects.select_related(
        'city__region__country'
    ).all()

    avg_stats = (
        EnvironmentalData.objects
        .values('city__region__country__name')
        .annotate(
            avg_air=Avg('air_quality'),
            avg_water=Avg('water_pollution')
        )
    )

    min_stats = (
        EnvironmentalData.objects
        .values('city__region__country__name')
        .annotate(
            min_air=Min('air_quality'),
            min_water=Min('water_pollution')
        )
    )

    max_stats = (
        EnvironmentalData.objects
        .values('city__region__country__name')
        .annotate(
            max_air=Max('air_quality'),
            max_water=Max('water_pollution')
        )
    )

    context = {
        # Страны
        'country_headers': ['Country'],
        'country_rows': [
            [c.name] for c in countries
        ],

        # Регионы
        'region_headers': ['Region', 'Country'],
        'region_rows': [
            [r.name, r.country.name] for r in regions
        ],

        # Города
        'city_headers': ['City', 'Region', 'Country'],
        'city_rows': [
            [c.name, c.region.name, c.region.country.name]
            for c in cities
        ],

        # Данные
        'data_headers': [
            'City', 'Region', 'Country',
            'Air quality', 'Water pollution'
        ],
        'data_rows': [
            [
                d.city.name,
                d.city.region.name,
                d.city.region.country.name,
                round(d.air_quality, 2),
                round(d.water_pollution, 2),
            ]
            for d in data
        ],

        # Средние
        'avg_headers': ['Country', 'Avg air quality', 'Avg water pollution'],
        'avg_rows': [
            [
                s['city__region__country__name'],
                round(s['avg_air'], 2),
                round(s['avg_water'], 2),
            ]
            for s in avg_stats
        ],

        # Минимум
        'min_headers': ['Country', 'Min air quality', 'Min water pollution'],
        'min_rows': [
            [
                s['city__region__country__name'],
                round(s['min_air'], 2),
                round(s['min_water'], 2),
            ]
            for s in min_stats
        ],

        # Максимум
        'max_headers': ['Country', 'Max air quality', 'Max water pollution'],
        'max_rows': [
            [
                s['city__region__country__name'],
                round(s['max_air'], 2),
                round(s['max_water'], 2),
            ]
            for s in max_stats
        ],
    }

    return TemplateResponse(
        request,
        'home.jinja',
        context,
        using='jinja2'
    )
