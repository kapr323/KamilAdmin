from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('viewer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='internaldirectives',
            name='type',
            field=models.CharField(choices=[('Řád', 'Regulations'), ('Směrnice', 'Directives'), ('Nařízení', 'Rules')], default='Řád', max_length=50),
        ),
    ]
