# Generated by Django 5.0.3 on 2024-03-27 23:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codingChallenge', '0002_exerciseresult'),
    ]

    operations = [
        migrations.AddField(
            model_name='exerciseresult',
            name='correct',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='exerciseresult',
            name='selected_answer',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
