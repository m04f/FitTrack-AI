# Generated by Django 4.2.21 on 2025-05-17 15:40

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('workout', '0007_alter_planuser_unique_together_remove_planuser_plan_and_more'),
        ('user_records', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workoutrecord',
            name='plan',
        ),
        migrations.RemoveField(
            model_name='workoutrecord',
            name='planday',
        ),
        migrations.AlterField(
            model_name='userplan',
            name='plan',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='workout.plan'),
        ),
        migrations.CreateModel(
            name='UserPlanWorkout',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('date', models.DateField()),
                ('record', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user_records.workoutrecord')),
                ('userplan', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='user_records.userplan')),
                ('workout', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='workout.workout')),
            ],
        ),
        migrations.AddField(
            model_name='userplan',
            name='workouts',
            field=models.ManyToManyField(through='user_records.UserPlanWorkout', to='user_records.workoutrecord'),
        ),
    ]
