# Generated by Django 3.2.6 on 2022-05-25 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('isay', '0011_auto_20220526_0145'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='who_accepted',
            field=models.CharField(blank=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='gender',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], max_length=100),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='phone',
            field=models.CharField(max_length=12),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='services',
            field=models.CharField(choices=[('Counseling', 'Counseling'), ('Psychological Testing', 'Psychological Testing'), ('Career Guidance, Graduate Placement and Follow-up', 'Career Guidance, Graduate Placement and Follow-up'), ('Human Development Services', 'Human Development Services'), ('Peer Facilitating Program', 'Peer Facilitating Program')], max_length=100),
        ),
    ]