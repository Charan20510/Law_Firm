from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='advocateprofile',
            options={'verbose_name': 'Advocate Profile', 'verbose_name_plural': 'Advocate Profiles'},
        ),
        migrations.AlterModelOptions(
            name='clientprofile',
            options={'verbose_name': 'Client Profile', 'verbose_name_plural': 'Client Profiles'},
        ),
        migrations.RemoveField(
            model_name='user',
            name='username',
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(blank=True, choices=[('client', 'Client'), ('advocate', 'Advocate')], max_length=20, null=True),
        ),
    ]
