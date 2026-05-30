from django.db import migrations

REFERENCES = [
    # ── MEX-85D/57D: Nuevo Laredo → Monterrey → Saltillo ────────────────────
    {"lat": 27.160, "lon": -99.520,  "type": "caseta",     "name": "Caseta Colombia Solidaridad"},
    {"lat": 26.490, "lon": -100.200, "type": "caseta",     "name": "Caseta Sabinas Hidalgo"},
    {"lat": 25.700, "lon": -100.370, "type": "caseta",     "name": "Caseta Monterrey Norte"},
    {"lat": 25.490, "lon": -100.870, "type": "caseta",     "name": "Caseta Saltillo Oriente"},
    {"lat": 27.090, "lon": -99.528,  "type": "paradero",   "name": "Paradero Vallecillo"},
    {"lat": 26.260, "lon": -100.248, "type": "paradero",   "name": "Paradero Mamulique"},
    {"lat": 25.920, "lon": -100.271, "type": "paradero",   "name": "Paradero Escobedo"},
    {"lat": 25.555, "lon": -100.610, "type": "paradero",   "name": "Paradero Cumbres Monterrey"},
    {"lat": 27.200, "lon": -99.514,  "type": "gasolinera", "name": "Pemex Nuevo Laredo Sur"},
    {"lat": 26.700, "lon": -99.810,  "type": "gasolinera", "name": "Pemex Anahuac"},
    {"lat": 26.050, "lon": -100.270, "type": "gasolinera", "name": "Pemex Cienega de Flores"},
    {"lat": 25.540, "lon": -100.330, "type": "gasolinera", "name": "Pemex Monterrey Tecnologico"},
    {"lat": 25.350, "lon": -101.050, "type": "gasolinera", "name": "Pemex Saltillo Oriente"},
    {"lat": 26.200, "lon": -100.252, "type": "rampa",      "name": "Rampa Paso Mamulique Km 165"},
    {"lat": 25.565, "lon": -100.605, "type": "rampa",      "name": "Rampa Cumbres Monterrey Km 286"},
    {"lat": 25.515, "lon": -100.755, "type": "rampa",      "name": "Rampa Cumbres Monterrey Km 301"},
    {"lat": 25.475, "lon": -100.840, "type": "rampa",      "name": "Rampa Cumbres Monterrey Km 312"},
    # ── MEX-57D: Saltillo → Matehuala → San Luis Potosi ─────────────────────
    {"lat": 23.650, "lon": -100.630, "type": "caseta",     "name": "Caseta Matehuala"},
    {"lat": 22.210, "lon": -100.970, "type": "caseta",     "name": "Caseta San Luis Potosi Sur"},
    {"lat": 25.200, "lon": -101.095, "type": "paradero",   "name": "Paradero Arteaga"},
    {"lat": 24.820, "lon": -101.050, "type": "paradero",   "name": "Paradero Carneros"},
    {"lat": 24.100, "lon": -100.890, "type": "paradero",   "name": "Paradero Cedral"},
    {"lat": 23.660, "lon": -100.625, "type": "paradero",   "name": "Paradero Matehuala Norte"},
    {"lat": 22.900, "lon": -100.715, "type": "paradero",   "name": "Paradero Villa de Reyes"},
    {"lat": 24.600, "lon": -100.985, "type": "gasolinera", "name": "Pemex General Cepeda"},
    {"lat": 23.660, "lon": -100.635, "type": "gasolinera", "name": "Pemex Matehuala Norte"},
    {"lat": 23.400, "lon": -100.680, "type": "gasolinera", "name": "Pemex Charcas"},
    {"lat": 22.400, "lon": -100.930, "type": "gasolinera", "name": "Pemex Soledad de G.S."},
    # ── MEX-57D/45D: San Luis Potosi → Queretaro → Guadalajara ──────────────
    {"lat": 20.720, "lon": -100.405, "type": "caseta",     "name": "Caseta Queretaro Palmillas"},
    {"lat": 21.040, "lon": -101.415, "type": "caseta",     "name": "Caseta El Gallo"},
    {"lat": 20.672, "lon": -103.285, "type": "caseta",     "name": "Caseta Guadalajara Tonala"},
    {"lat": 21.650, "lon": -100.750, "type": "paradero",   "name": "Paradero San Felipe"},
    {"lat": 21.550, "lon": -100.510, "type": "paradero",   "name": "Paradero Lagunillas"},
    {"lat": 21.365, "lon": -101.925, "type": "paradero",   "name": "Paradero Lagos de Moreno"},
    {"lat": 20.900, "lon": -102.400, "type": "paradero",   "name": "Paradero Tepatitlan Norte"},
    {"lat": 20.390, "lon": -101.390, "type": "paradero",   "name": "Paradero Irapuato"},
    {"lat": 21.500, "lon": -100.612, "type": "gasolinera", "name": "Pemex San Juan del Rio SLP"},
    {"lat": 20.980, "lon": -101.380, "type": "gasolinera", "name": "Pemex San Diego de la Union"},
    {"lat": 21.360, "lon": -101.920, "type": "gasolinera", "name": "Pemex Lagos de Moreno Norte"},
    {"lat": 21.280, "lon": -102.100, "type": "gasolinera", "name": "Pemex Encarnacion de Diaz"},
    {"lat": 20.930, "lon": -101.390, "type": "gasolinera", "name": "Pemex Irapuato Sur"},
    {"lat": 20.740, "lon": -103.080, "type": "gasolinera", "name": "Pemex Tlaquepaque"},
    {"lat": 21.180, "lon": -102.280, "type": "rampa",      "name": "Rampa Los Altos de Jalisco Km 1118"},
    {"lat": 20.850, "lon": -102.700, "type": "rampa",      "name": "Rampa Tepatitlan Km 1152"},
    # ── MEX-57D: Queretaro → Mexico City ────────────────────────────────────
    {"lat": 19.972, "lon": -99.376,  "type": "caseta",     "name": "Caseta San Martin Obispo"},
    {"lat": 19.716, "lon": -99.258,  "type": "caseta",     "name": "Caseta Tepotzotlan"},
    {"lat": 20.390, "lon": -100.005, "type": "paradero",   "name": "Paradero San Juan del Rio"},
    {"lat": 19.975, "lon": -99.535,  "type": "paradero",   "name": "Paradero Jilotepec"},
    {"lat": 19.718, "lon": -99.223,  "type": "paradero",   "name": "Paradero Tepotzotlan"},
    {"lat": 20.378, "lon": -100.002, "type": "gasolinera", "name": "Pemex San Juan del Rio Oriente"},
    {"lat": 19.970, "lon": -99.530,  "type": "gasolinera", "name": "Pemex Jilotepec"},
    {"lat": 19.714, "lon": -99.220,  "type": "gasolinera", "name": "Pemex Tepotzotlan"},
    # ── MEX-150D: Mexico City → Puebla → Orizaba → Veracruz ─────────────────
    {"lat": 19.395, "lon": -98.615,  "type": "caseta",     "name": "Caseta Rio Frio"},
    {"lat": 19.070, "lon": -98.025,  "type": "caseta",     "name": "Caseta Amozoc"},
    {"lat": 18.855, "lon": -97.145,  "type": "caseta",     "name": "Caseta Orizaba"},
    {"lat": 18.830, "lon": -96.615,  "type": "caseta",     "name": "Caseta La Tinaja"},
    {"lat": 19.150, "lon": -98.300,  "type": "paradero",   "name": "Paradero Tlaxcala Norte"},
    {"lat": 18.870, "lon": -96.940,  "type": "paradero",   "name": "Paradero Cordoba"},
    {"lat": 19.230, "lon": -96.200,  "type": "paradero",   "name": "Paradero Veracruz Norte"},
    {"lat": 19.390, "lon": -98.610,  "type": "gasolinera", "name": "Pemex Rio Frio"},
    {"lat": 19.068, "lon": -98.022,  "type": "gasolinera", "name": "Pemex Amozoc"},
    {"lat": 18.878, "lon": -97.138,  "type": "gasolinera", "name": "Pemex Orizaba Norte"},
    {"lat": 18.868, "lon": -96.940,  "type": "gasolinera", "name": "Pemex Cordoba Oriente"},
    {"lat": 19.228, "lon": -96.192,  "type": "gasolinera", "name": "Pemex Veracruz Norte"},
    {"lat": 19.397, "lon": -98.613,  "type": "rampa",      "name": "Rampa Rio Frio Km 53"},
    {"lat": 18.857, "lon": -97.147,  "type": "rampa",      "name": "Rampa Cumbres Orizaba Km 292"},
    # ── MEX-15D: Guadalajara → Tepic → Mazatlan ─────────────────────────────
    {"lat": 21.155, "lon": -104.243, "type": "caseta",     "name": "Caseta Chapalilla"},
    {"lat": 21.500, "lon": -104.895, "type": "caseta",     "name": "Caseta Tepic"},
    {"lat": 23.190, "lon": -106.230, "type": "caseta",     "name": "Caseta Villa Union"},
    {"lat": 21.182, "lon": -104.240, "type": "paradero",   "name": "Paradero La Quemada"},
    {"lat": 21.790, "lon": -105.260, "type": "paradero",   "name": "Paradero Nayarit Norte"},
    {"lat": 23.050, "lon": -106.060, "type": "paradero",   "name": "Paradero La Noria"},
    {"lat": 21.505, "lon": -104.890, "type": "gasolinera", "name": "Pemex Tepic Oriente"},
    {"lat": 21.790, "lon": -105.258, "type": "gasolinera", "name": "Pemex Nayarit Norte"},
    {"lat": 23.225, "lon": -106.440, "type": "gasolinera", "name": "Pemex Mazatlan Sur"},
    {"lat": 21.170, "lon": -104.237, "type": "rampa",      "name": "Rampa La Quemada Km 98"},
    {"lat": 21.792, "lon": -105.263, "type": "rampa",      "name": "Rampa Nayarit Km 145"},
    # ── MEX-110/54D: Manzanillo → Colima → Guadalajara ──────────────────────
    {"lat": 19.062, "lon": -104.298, "type": "caseta",     "name": "Caseta Manzanillo"},
    {"lat": 19.255, "lon": -103.712, "type": "caseta",     "name": "Caseta Colima Coquimatlan"},
    {"lat": 19.871, "lon": -103.604, "type": "caseta",     "name": "Caseta Sayula"},
    {"lat": 20.272, "lon": -103.585, "type": "caseta",     "name": "Caseta La Venta"},
    {"lat": 18.943, "lon": -103.970, "type": "paradero",   "name": "Paradero Armeria"},
    {"lat": 19.238, "lon": -103.722, "type": "paradero",   "name": "Paradero Colima Sur"},
    {"lat": 19.703, "lon": -103.465, "type": "paradero",   "name": "Paradero Ciudad Guzman"},
    {"lat": 20.142, "lon": -103.577, "type": "paradero",   "name": "Paradero Acatlan de Juarez"},
    {"lat": 19.080, "lon": -104.262, "type": "gasolinera", "name": "Pemex Manzanillo Este"},
    {"lat": 19.235, "lon": -103.728, "type": "gasolinera", "name": "Pemex Colima Sur"},
    {"lat": 19.706, "lon": -103.460, "type": "gasolinera", "name": "Pemex Ciudad Guzman Norte"},
    {"lat": 20.268, "lon": -103.582, "type": "gasolinera", "name": "Pemex La Venta"},
    {"lat": 19.635, "lon": -103.500, "type": "rampa",      "name": "Rampa Cumbres Colima Km 78"},
    # ── MEX-200/80: Manzanillo → Barra de Navidad → Guadalajara ─────────────
    {"lat": 19.225, "lon": -104.567, "type": "caseta",     "name": "Caseta Cihuatlan"},
    {"lat": 19.775, "lon": -104.375, "type": "caseta",     "name": "Caseta Autlan"},
    {"lat": 19.195, "lon": -104.688, "type": "paradero",   "name": "Paradero Barra de Navidad"},
    {"lat": 19.225, "lon": -104.717, "type": "paradero",   "name": "Paradero San Patricio Melaque"},
    {"lat": 19.222, "lon": -104.570, "type": "gasolinera", "name": "Pemex Cihuatlan"},
    {"lat": 19.778, "lon": -104.370, "type": "gasolinera", "name": "Pemex Autlan Norte"},
    {"lat": 19.687, "lon": -104.207, "type": "rampa",      "name": "Rampa Sierra Autlan Km 145"},
    # ── MEX-180D/85: Veracruz → Tampico → Monterrey ─────────────────────────
    {"lat": 19.381, "lon": -96.374,  "type": "caseta",     "name": "Caseta Cardel"},
    {"lat": 20.966, "lon": -97.408,  "type": "caseta",     "name": "Caseta Tuxpan"},
    {"lat": 22.279, "lon": -97.867,  "type": "caseta",     "name": "Caseta Tampico"},
    {"lat": 23.736, "lon": -99.125,  "type": "caseta",     "name": "Caseta Ciudad Victoria"},
    {"lat": 24.860, "lon": -99.565,  "type": "caseta",     "name": "Caseta Linares"},
    {"lat": 20.530, "lon": -97.450,  "type": "paradero",   "name": "Paradero Poza Rica"},
    {"lat": 22.298, "lon": -97.860,  "type": "paradero",   "name": "Paradero Tampico Norte"},
    {"lat": 23.740, "lon": -99.120,  "type": "paradero",   "name": "Paradero Ciudad Victoria Norte"},
    {"lat": 19.385, "lon": -96.371,  "type": "gasolinera", "name": "Pemex Cardel Norte"},
    {"lat": 20.533, "lon": -97.445,  "type": "gasolinera", "name": "Pemex Poza Rica Norte"},
    {"lat": 20.960, "lon": -97.412,  "type": "gasolinera", "name": "Pemex Tuxpan Sur"},
    {"lat": 22.267, "lon": -97.874,  "type": "gasolinera", "name": "Pemex Tampico Sur"},
    {"lat": 23.730, "lon": -99.130,  "type": "gasolinera", "name": "Pemex Ciudad Victoria Sur"},
    {"lat": 24.862, "lon": -99.560,  "type": "gasolinera", "name": "Pemex Linares Norte"},
    {"lat": 23.560, "lon": -99.230,  "type": "rampa",      "name": "Rampa Sierra Tamaulipas Km 380"},
]


def seed_references(apps, schema_editor):
    RouteReference = apps.get_model('producto', 'RouteReference')
    for ref in REFERENCES:
        RouteReference.objects.get_or_create(
            name=ref['name'],
            defaults={
                'lat':    ref['lat'],
                'lon':    ref['lon'],
                'type':   ref['type'],
                'active': True,
            },
        )


def remove_references(apps, schema_editor):
    RouteReference = apps.get_model('producto', 'RouteReference')
    RouteReference.objects.filter(
        name__in=[r['name'] for r in REFERENCES]
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('producto', '0005_routereference'),
    ]

    operations = [
        migrations.RunPython(seed_references, remove_references),
    ]
