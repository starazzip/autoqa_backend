from django.db import models
from django.db.models.signals import post_migrate
from django.dispatch import receiver


@receiver(post_migrate)
def initialize_data(sender, **kwargs):
    if sender.name == 'AutoQA':
        brands = [{'brand': 'm6s'}]

        for brand_data in brands:
            Brand.objects.get_or_create(brand=brand_data['brand'])

        envs = [{'environment': 'test'}]
        for env_data in envs:
            TestEnvironment.objects.get_or_create(environment=env_data['environment'])


class Brand(models.Model):
    brand = models.CharField(max_length=50, null=False)


class TestEnvironment(models.Model):
    environment = models.CharField(max_length=50, null=False)


class GherkinFeatures(models.Model):
    feature = models.TextField()
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    environment = models.ForeignKey(TestEnvironment, on_delete=models.CASCADE)


class GherkinScenarios(models.Model):
    scenario = models.TextField()
    feature = models.ForeignKey(GherkinFeatures, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    environment = models.ForeignKey(TestEnvironment, on_delete=models.CASCADE)


class ExecutionTask(models.Model):
    environment_id = models.ForeignKey(TestEnvironment, on_delete=models.CASCADE)
    brand_id = models.ForeignKey(Brand, on_delete=models.CASCADE)
    scenario_id = models.PositiveIntegerField()
    start_timestamp = models.PositiveBigIntegerField()
    end_timestamp = models.PositiveBigIntegerField(null=True, blank=True)
    status = models.CharField(max_length=20)
    report_url = models.URLField(blank=True)


class ScheduledTask(models.Model):
    execution_task_id = models.ForeignKey(ExecutionTask, on_delete=models.CASCADE)
    environment_id = models.ForeignKey(TestEnvironment, on_delete=models.CASCADE)
    brand_id = models.ForeignKey(Brand, on_delete=models.CASCADE)
    scenario_id = models.PositiveIntegerField()
    cron = models.CharField(max_length=20)
    status = models.CharField(max_length=20)
