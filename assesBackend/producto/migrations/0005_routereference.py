from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('producto', '0004_userprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='RouteReference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lat', models.FloatField()),
                ('lon', models.FloatField()),
                ('type', models.CharField(
                    max_length=20,
                    choices=[
                        ('caseta',     'Caseta de Cobro'),
                        ('paradero',   'Paradero / Área de Descanso'),
                        ('gasolinera', 'Gasolinera'),
                        ('rampa',      'Rampa de Emergencia'),
                    ],
                )),
                ('name', models.CharField(max_length=200)),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['type', 'name'],
            },
        ),
    ]
