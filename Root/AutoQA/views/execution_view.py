from rest_framework import generics

from AutoQA.serializer import (
    BrandSerializer,
    EnvironmentSerializer,
    ExecutionTaskSerializer,
)

from ..models import Brand, ExecutionTask, TestEnvironment


class BrandListView(generics.ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class EnvironmentListView(generics.ListAPIView):
    queryset = TestEnvironment.objects.all()
    serializer_class = EnvironmentSerializer


class ExecutionTaskListView(generics.ListCreateAPIView):
    queryset = ExecutionTask.objects.all()
    serializer_class = ExecutionTaskSerializer


class ExecutionTaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ExecutionTask.objects.all()
    serializer_class = ExecutionTaskSerializer
