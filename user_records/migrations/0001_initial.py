# Generated by Django 4.2.21 on 2025-05-29 15:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('workout', '0004_plan_data'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserPlan',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('start_date', models.DateField(auto_now=True)),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='workout.plan')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='WorkoutRecord',
            fields=[
                ('uuid', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('datetime', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('duration', models.PositiveIntegerField(null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('workout', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='workout.workout')),
            ],
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
        migrations.CreateModel(
            name='ExerciseRecord',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('weight', models.PositiveSmallIntegerField(null=True)),
                ('reps', models.PositiveSmallIntegerField(null=True)),
                ('duration', models.PositiveIntegerField(null=True)),
                ('rest', models.PositiveIntegerField(null=True)),
                ('notes', models.TextField(blank=True)),
                ('pre', models.PositiveSmallIntegerField(null=True)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('exercise', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='workout.exercise')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('workout_record', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='user_records.workoutrecord')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='userplan',
            unique_together={('plan', 'user')},
        ),
        migrations.AddConstraint(
            model_name='exerciserecord',
            constraint=models.CheckConstraint(check=models.Q(('pre__lte', 10)), name='pre_lte_10'),
        ),
        migrations.AddConstraint(
            model_name='exerciserecord',
            constraint=models.CheckConstraint(check=models.Q(('duration__isnull', False), ('reps__isnull', False), _connector='OR'), name='either_duration_or_reps_notnull', violation_error_message='Either duration or reps must be provided'),
        ),
    ]
