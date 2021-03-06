# Generated by Django 2.0.6 on 2018-07-31 10:37

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('login', '0003_auto_20180728_1210'),
    ]

    operations = [
        migrations.CreateModel(
            name='Holiday',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('description', models.TextField()),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='section',
            unique_together={('section_name',)},
        ),
        migrations.AlterUniqueTogether(
            name='semester',
            unique_together={('semester',)},
        ),
        migrations.AlterUniqueTogether(
            name='student',
            unique_together={('rollno',)},
        ),
        migrations.AlterUniqueTogether(
            name='subject',
            unique_together={('subject_name',)},
        ),
        migrations.AlterUniqueTogether(
            name='teacher',
            unique_together={('user',)},
        ),
        migrations.AlterUniqueTogether(
            name='timetable',
            unique_together={('user',)},
        ),
    ]
