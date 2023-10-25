# Generated by Django 4.1 on 2023-10-24 09:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='ExecutionTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scenario_id', models.PositiveIntegerField()),
                ('start_timestamp', models.PositiveBigIntegerField()),
                ('end_timestamp', models.PositiveBigIntegerField(blank=True, null=True)),
                ('status', models.CharField(max_length=20)),
                ('report_url', models.URLField(blank=True)),
                ('brand_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AutoQA.brand')),
            ],
        ),
        migrations.CreateModel(
            name='GherkinFeatures',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feature', models.TextField()),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AutoQA.brand')),
            ],
        ),
        migrations.CreateModel(
            name='TestEnvironment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('environment', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='ScheduledTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scenario_id', models.PositiveIntegerField()),
                ('cron', models.CharField(max_length=20)),
                ('status', models.CharField(max_length=20)),
                ('brand_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AutoQA.brand')),
                ('environment_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AutoQA.testenvironment')),
                ('execution_task_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AutoQA.executiontask')),
            ],
        ),
        migrations.CreateModel(
            name='GherkinScenarios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('scenario', models.TextField()),
                ('brand', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AutoQA.brand')),
                ('environment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AutoQA.testenvironment')),
                ('feature', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AutoQA.gherkinfeatures')),
            ],
        ),
        migrations.AddField(
            model_name='gherkinfeatures',
            name='environment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AutoQA.testenvironment'),
        ),
        migrations.AddField(
            model_name='executiontask',
            name='environment_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AutoQA.testenvironment'),
        ),
    ]
