from django.db import migrations

# New reference entries added in the second round of data enrichment.
# All existing entries from 0006 are omitted — get_or_create handles any
# accidental duplicates safely by matching on the name field.
NEW_REFERENCES = [
    # ── MEX-54D/110: Manzanillo → Guadalajara (additional waypoints) ──────────
    {"lat": 18.906, "lon": -103.878, "type": "caseta",     "name": "Caseta Tecoman"},
    {"lat": 18.908, "lon": -103.874, "type": "paradero",   "name": "Paradero Tecoman"},
    {"lat": 19.295, "lon": -103.718, "type": "paradero",   "name": "Paradero Colima Norte"},
    {"lat": 19.533, "lon": -103.383, "type": "paradero",   "name": "Paradero Tuxpan Jalisco"},
    {"lat": 19.683, "lon": -103.317, "type": "paradero",   "name": "Paradero Tamazula"},
    {"lat": 19.955, "lon": -103.755, "type": "paradero",   "name": "Paradero Tapalpa Km 215"},
    {"lat": 20.478, "lon": -103.445, "type": "paradero",   "name": "Paradero Tlajomulco"},
    {"lat": 18.945, "lon": -103.966, "type": "gasolinera", "name": "Pemex Armeria Norte"},
    {"lat": 18.908, "lon": -103.872, "type": "gasolinera", "name": "Pemex Tecoman"},
    {"lat": 19.295, "lon": -103.723, "type": "gasolinera", "name": "Pemex Colima Norte"},
    {"lat": 19.535, "lon": -103.385, "type": "gasolinera", "name": "Pemex Tuxpan Jalisco"},
    {"lat": 20.148, "lon": -103.571, "type": "gasolinera", "name": "Pemex Acatlan de Juarez"},
    {"lat": 20.480, "lon": -103.442, "type": "gasolinera", "name": "Pemex Tlajomulco"},
    {"lat": 19.580, "lon": -103.530, "type": "rampa",      "name": "Rampa Cumbres Colima Norte Km 118"},
    {"lat": 19.880, "lon": -103.607, "type": "rampa",      "name": "Rampa Sayula Norte Km 175"},
    # ── MEX-200/80: Manzanillo → Autlan (additional) ─────────────────────────
    {"lat": 19.922, "lon": -104.296, "type": "caseta",     "name": "Caseta Union de Tula"},
    {"lat": 19.790, "lon": -104.370, "type": "paradero",   "name": "Paradero Autlan Norte"},
    {"lat": 19.932, "lon": -104.282, "type": "paradero",   "name": "Paradero El Grullo"},
    {"lat": 19.926, "lon": -104.285, "type": "gasolinera", "name": "Pemex Union de Tula"},
    {"lat": 19.850, "lon": -104.330, "type": "rampa",      "name": "Rampa Sierra Jalisco Km 162"},
    # ── MEX-45D: Guadalajara → Zapotlanejo → Los Altos → Aguascalientes ──────
    {"lat": 20.628, "lon": -102.973, "type": "caseta",     "name": "Caseta Zapotlanejo"},
    {"lat": 21.780, "lon": -102.298, "type": "caseta",     "name": "Caseta Aguascalientes Sur"},
    {"lat": 20.635, "lon": -102.975, "type": "paradero",   "name": "Paradero Zapotlanejo"},
    {"lat": 20.817, "lon": -102.733, "type": "paradero",   "name": "Paradero Tepatitlan Sur"},
    {"lat": 21.005, "lon": -102.398, "type": "paradero",   "name": "Paradero San Miguel el Alto"},
    {"lat": 21.163, "lon": -102.462, "type": "paradero",   "name": "Paradero Jalostotitlan"},
    {"lat": 21.510, "lon": -102.226, "type": "paradero",   "name": "Paradero Encarnacion de Diaz AGS"},
    {"lat": 21.877, "lon": -102.305, "type": "paradero",   "name": "Paradero Aguascalientes Norte"},
    {"lat": 20.632, "lon": -102.970, "type": "gasolinera", "name": "Pemex Zapotlanejo"},
    {"lat": 20.817, "lon": -102.730, "type": "gasolinera", "name": "Pemex Tepatitlan Los Altos"},
    {"lat": 21.006, "lon": -102.397, "type": "gasolinera", "name": "Pemex San Miguel el Alto"},
    {"lat": 21.785, "lon": -102.302, "type": "gasolinera", "name": "Pemex Aguascalientes Sur"},
    {"lat": 21.882, "lon": -102.308, "type": "gasolinera", "name": "Pemex Aguascalientes Norte"},
    {"lat": 20.730, "lon": -102.942, "type": "rampa",      "name": "Rampa Los Altos GDL Km 58"},
    {"lat": 21.180, "lon": -102.280, "type": "rampa",      "name": "Rampa Los Altos de Jalisco Km 120"},
    # ── MEX-45: Aguascalientes → Zacatecas ───────────────────────────────────
    {"lat": 21.898, "lon": -102.302, "type": "caseta",     "name": "Caseta Aguascalientes Norte"},
    {"lat": 22.562, "lon": -102.547, "type": "caseta",     "name": "Caseta Zacatecas Sur"},
    {"lat": 22.072, "lon": -102.268, "type": "paradero",   "name": "Paradero San Francisco de los Romo"},
    {"lat": 22.232, "lon": -102.342, "type": "paradero",   "name": "Paradero Rincon de Romos"},
    {"lat": 22.398, "lon": -102.421, "type": "paradero",   "name": "Paradero Trancoso"},
    {"lat": 22.074, "lon": -102.265, "type": "gasolinera", "name": "Pemex San Francisco de los Romo"},
    {"lat": 22.400, "lon": -102.418, "type": "gasolinera", "name": "Pemex Trancoso"},
    {"lat": 22.798, "lon": -102.582, "type": "gasolinera", "name": "Pemex Zacatecas Norte"},
    # ── MEX-54D: Zacatecas → Concepcion del Oro → Saltillo ───────────────────
    {"lat": 22.895, "lon": -102.508, "type": "caseta",     "name": "Caseta Zacatecas Norte"},
    {"lat": 24.614, "lon": -101.412, "type": "caseta",     "name": "Caseta Concepcion del Oro"},
    {"lat": 25.488, "lon": -101.038, "type": "caseta",     "name": "Caseta Saltillo Norte MEX-54"},
    {"lat": 23.088, "lon": -102.308, "type": "paradero",   "name": "Paradero Fresnillo Norte"},
    {"lat": 23.508, "lon": -102.095, "type": "paradero",   "name": "Paradero Villa Gonzalez Ortega"},
    {"lat": 24.048, "lon": -101.735, "type": "paradero",   "name": "Paradero Mazapil"},
    {"lat": 24.618, "lon": -101.415, "type": "paradero",   "name": "Paradero Concepcion del Oro"},
    {"lat": 25.102, "lon": -101.160, "type": "paradero",   "name": "Paradero Cedros"},
    {"lat": 23.090, "lon": -102.305, "type": "gasolinera", "name": "Pemex Fresnillo Norte"},
    {"lat": 23.510, "lon": -102.092, "type": "gasolinera", "name": "Pemex Villa Gonzalez Ortega"},
    {"lat": 24.050, "lon": -101.732, "type": "gasolinera", "name": "Pemex Mazapil"},
    {"lat": 24.620, "lon": -101.410, "type": "gasolinera", "name": "Pemex Concepcion del Oro"},
    {"lat": 25.104, "lon": -101.158, "type": "gasolinera", "name": "Pemex Cedros"},
    {"lat": 23.900, "lon": -101.920, "type": "rampa",      "name": "Rampa Sierra Zacatecas-SLP Km 285"},
    {"lat": 25.300, "lon": -101.098, "type": "rampa",      "name": "Rampa Descenso Saltillo Km 405"},
    # ── MEX-40D: Saltillo → Monterrey ────────────────────────────────────────
    {"lat": 25.437, "lon": -101.128, "type": "caseta",     "name": "Caseta Saltillo Poniente"},
    {"lat": 25.490, "lon": -100.468, "type": "caseta",     "name": "Caseta El Mamey"},
    {"lat": 25.548, "lon": -100.945, "type": "paradero",   "name": "Paradero Ramos Arizpe"},
    {"lat": 25.498, "lon": -100.702, "type": "paradero",   "name": "Paradero La Cienega"},
    {"lat": 25.488, "lon": -100.552, "type": "paradero",   "name": "Paradero Monterrey Poniente"},
    {"lat": 25.550, "lon": -100.948, "type": "gasolinera", "name": "Pemex Ramos Arizpe"},
    {"lat": 25.500, "lon": -100.705, "type": "gasolinera", "name": "Pemex La Cienega"},
    {"lat": 25.692, "lon": -100.348, "type": "gasolinera", "name": "Pemex Monterrey Oriente"},
    {"lat": 25.502, "lon": -100.782, "type": "rampa",      "name": "Rampa Cumbres Saltillo-MTY Km 45"},
    {"lat": 25.496, "lon": -100.682, "type": "rampa",      "name": "Rampa Cumbres Saltillo-MTY Km 55"},
    # ── MEX-45D: Bajio corridor (additional) ─────────────────────────────────
    {"lat": 20.930, "lon": -101.363, "type": "caseta",     "name": "Caseta Irapuato"},
    {"lat": 20.578, "lon": -100.445, "type": "caseta",     "name": "Caseta Queretaro El Pueblito"},
    {"lat": 21.148, "lon": -101.682, "type": "paradero",   "name": "Paradero Leon Sur"},
    {"lat": 21.678, "lon": -101.352, "type": "paradero",   "name": "Paradero Irapuato Norte"},
    {"lat": 20.582, "lon": -101.180, "type": "paradero",   "name": "Paradero Salamanca"},
    {"lat": 21.145, "lon": -101.678, "type": "gasolinera", "name": "Pemex Leon Sur"},
    {"lat": 20.932, "lon": -101.360, "type": "gasolinera", "name": "Pemex Irapuato Sur"},
    {"lat": 20.582, "lon": -101.178, "type": "gasolinera", "name": "Pemex Salamanca"},
    # ── MEX-57D: Queretaro → CDMX (additional) ───────────────────────────────
    {"lat": 20.285, "lon": -99.885,  "type": "paradero",   "name": "Paradero Palmillas Norte"},
    {"lat": 20.082, "lon": -99.680,  "type": "paradero",   "name": "Paradero Tula"},
    {"lat": 20.287, "lon": -99.888,  "type": "gasolinera", "name": "Pemex Palmillas"},
    {"lat": 20.083, "lon": -99.675,  "type": "gasolinera", "name": "Pemex Tula"},
    {"lat": 20.125, "lon": -99.590,  "type": "rampa",      "name": "Rampa Tula Km 122"},
    # ── MEX-150D: CDMX → Veracruz (additional) ───────────────────────────────
    {"lat": 19.038, "lon": -98.190,  "type": "paradero",   "name": "Paradero Puebla Oriente"},
    {"lat": 18.948, "lon": -97.758,  "type": "paradero",   "name": "Paradero Tehuacan Norte"},
    {"lat": 19.040, "lon": -98.193,  "type": "gasolinera", "name": "Pemex Puebla Oriente"},
    {"lat": 18.867, "lon": -97.252,  "type": "rampa",      "name": "Rampa Cumbres Orizaba Km 282"},
    # ── MEX-180D: Veracruz → Monterrey (additional) ──────────────────────────
    {"lat": 21.658, "lon": -97.840,  "type": "paradero",   "name": "Paradero Tuxpam Sur"},
    {"lat": 23.420, "lon": -99.060,  "type": "paradero",   "name": "Paradero Jaumave"},
    {"lat": 24.862, "lon": -99.558,  "type": "paradero",   "name": "Paradero Linares Norte"},
    {"lat": 21.660, "lon": -97.842,  "type": "gasolinera", "name": "Pemex Tuxpam Norte"},
    {"lat": 23.422, "lon": -99.058,  "type": "gasolinera", "name": "Pemex Jaumave"},
    {"lat": 23.420, "lon": -99.162,  "type": "rampa",      "name": "Rampa Canon Jaumave Km 358"},
]


def seed_references(apps, schema_editor):
    RouteReference = apps.get_model('producto', 'RouteReference')
    for ref in NEW_REFERENCES:
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
        name__in=[r['name'] for r in NEW_REFERENCES]
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('producto', '0006_seed_route_references'),
    ]

    operations = [
        migrations.RunPython(seed_references, remove_references),
    ]
