from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('producto', '0007_seed_more_route_references'),
    ]

    operations = [
        migrations.CreateModel(
            name='DefaultDestination',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('lat', models.FloatField()),
                ('lng', models.FloatField()),
                ('company', models.CharField(max_length=200)),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['name'],
            },
        ),
    ]
