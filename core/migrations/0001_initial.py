import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('role', models.CharField(choices=[('client', 'Client'), ('advocate', 'Advocate')], max_length=20)),
                ('phone', models.CharField(max_length=20)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='AdvocateProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enrollment_number', models.CharField(max_length=100)),
                ('bar_council', models.CharField(max_length=255)),
                ('specialization', models.CharField(max_length=255)),
                ('experience_years', models.PositiveIntegerField()),
                ('office_address', models.TextField()),
                ('photo', models.ImageField(upload_to='advocate_photos/')),
                ('signature', models.ImageField(upload_to='advocate_signatures/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ClientProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('father_name', models.CharField(max_length=255)),
                ('dob', models.DateField()),
                ('gender', models.CharField(max_length=20)),
                ('address', models.TextField()),
                ('aadhaar', models.CharField(max_length=20)),
                ('pan', models.CharField(max_length=20)),
                ('photo', models.ImageField(upload_to='client_photos/')),
                ('id_proof', models.FileField(upload_to='client_id_proofs/')),
                ('signature', models.ImageField(upload_to='client_signatures/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Case',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('case_number', models.CharField(max_length=100)),
                ('case_type', models.CharField(choices=[('civil', 'Civil'), ('criminal', 'Criminal'), ('arbitration', 'Arbitration')], max_length=20)),
                ('court_name', models.CharField(max_length=255)),
                ('opponent_details', models.TextField()),
                ('filing_date', models.DateField()),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('closed', 'Closed')], max_length=20)),
                ('stage', models.CharField(choices=[('filing', 'Filing'), ('evidence', 'Evidence'), ('argument', 'Argument'), ('judgment', 'Judgment')], max_length=20)),
                ('description', models.TextField()),
                ('advocate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.advocateprofile')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.clientprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='case_documents/')),
                ('document_type', models.CharField(choices=[('evidence', 'Evidence'), ('id', 'ID'), ('other', 'Other')], max_length=20)),
                ('notes', models.TextField()),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.case')),
            ],
        ),
        migrations.CreateModel(
            name='Hearing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hearing_date', models.DateField()),
                ('next_hearing_date', models.DateField(blank=True, null=True)),
                ('notes', models.TextField()),
                ('judge_remarks', models.TextField()),
                ('status', models.CharField(choices=[('scheduled', 'Scheduled'), ('completed', 'Completed'), ('adjourned', 'Adjourned')], max_length=20)),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.case')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('due_date', models.DateField()),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('done', 'Done')], max_length=20)),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.case')),
            ],
        ),
    ]
