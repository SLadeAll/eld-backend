from django.db import migrations

DESTINATIONS = [
    {'name': 'Atotonilco, Estado de México',   'lat': 19.9207515,  'lng': -99.251266,   'company': 'WEG'},
    {'name': 'Huehuetoca, Estado de México',   'lat': 19.8539528,  'lng': -99.2380468,  'company': 'WEG Voltran'},
    {'name': 'Tizayuca, Hidalgo',              'lat': 19.8223601,  'lng': -98.975169,   'company': 'Voltran'},
    {'name': 'Santa Catarina, Nuevo León',     'lat': 25.7038605,  'lng': -100.4958117, 'company': 'Marathon'},
    {'name': 'Tecoman, Colima',                'lat': 18.9521368,  'lng': -103.8914258, 'company': 'Solarever'},
    {'name': 'Ciénega de Flores, Nuevo León',  'lat': 25.9355552,  'lng': -100.2052263, 'company': 'Volvo'},
    {'name': 'Querétaro, Querétaro',           'lat': 20.6057797,  'lng': -100.4206192, 'company': 'Clinic'},
]


def seed_destinations(apps, schema_editor):
    DefaultDestination = apps.get_model('producto', 'DefaultDestination')
    for d in DESTINATIONS:
        DefaultDestination.objects.get_or_create(
            name=d['name'],
            defaults={'lat': d['lat'], 'lng': d['lng'], 'company': d['company'], 'active': True},
        )


def remove_destinations(apps, schema_editor):
    DefaultDestination = apps.get_model('producto', 'DefaultDestination')
    names = [d['name'] for d in DESTINATIONS]
    DefaultDestination.objects.filter(name__in=names).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('producto', '0008_defaultdestination'),
    ]

    operations = [
        migrations.RunPython(seed_destinations, remove_destinations),
    ]
