from rest_framework import serializers

from AutoQA.models import Brand, ExecutionTask, ScheduledTask, TestEnvironment


class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = '__all__'


class EnvironmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = TestEnvironment
        fields = '__all__'


class ExecutionTaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = ExecutionTask
        fields = '__all__'


class ScheduledTaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = ScheduledTask
        fields = '__all__'
