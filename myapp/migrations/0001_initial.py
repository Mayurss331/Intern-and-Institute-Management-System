# Generated by Django 4.2.17 on 2025-03-04 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(max_length=255)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone_number', models.CharField(max_length=20)),
                ('resume', models.FileField(upload_to='resumes/')),
                ('source', models.CharField(max_length=255)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], max_length=10)),
                ('date_of_birth', models.DateField()),
                ('domicile_state', models.CharField(max_length=255)),
                ('current_location', models.CharField(max_length=255)),
                ('citizenship', models.CharField(max_length=255)),
                ('postgraduate_degree', models.CharField(blank=True, max_length=255, null=True)),
                ('postgraduate_stream', models.CharField(blank=True, max_length=255, null=True)),
                ('postgraduate_passing_year', models.IntegerField(blank=True, null=True)),
                ('undergraduate_degree', models.CharField(max_length=255)),
                ('undergraduate_stream', models.CharField(max_length=255)),
                ('undergraduate_passing_year', models.IntegerField()),
                ('college_name', models.CharField(max_length=255)),
                ('score_above_60', models.BooleanField(default=False)),
                ('standing_arrears', models.BooleanField(default=False)),
                ('coding_languages', models.TextField()),
                ('currently_working', models.BooleanField(default=False)),
                ('company_name', models.CharField(blank=True, max_length=255, null=True)),
                ('ctc_or_stipend', models.FloatField(blank=True, null=True)),
                ('designation', models.CharField(blank=True, max_length=255, null=True)),
                ('open_to_relocate', models.BooleanField(default=False)),
                ('passport_photo', models.ImageField(blank=True, null=True, upload_to='passport_photos/')),
            ],
        ),
    ]
