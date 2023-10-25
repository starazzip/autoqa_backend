from croniter import croniter
from rest_framework import generics, status
from rest_framework.response import Response

from AutoQA.models import ScheduledTask
from AutoQA.serializer import ScheduledTaskSerializer


class ScheduledTaskListView(generics.ListCreateAPIView):
    queryset = ScheduledTask.objects.all()
    serializer_class = ScheduledTaskSerializer

    def create(self, request, *args, **kwargs):
        cron_expression = request.data.get('cron', None)

        if not cron_expression:
            return Response({'error': 'Cron expression is required.'},
                            status=status.HTTP_400_BAD_REQUEST)

        if not self.is_valid_cron_expression(cron_expression):
            return Response({'error': 'Invalid Cron expression.'},
                            status=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)

    def is_valid_cron_expression(self, cron_expression):
        try:
            croniter(cron_expression)
            return True
        except:
            return False


class ScheduledTaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ScheduledTask.objects.all()
    serializer_class = ScheduledTaskSerializer

    def update(self, request, *args, **kwargs):
        cron_expression = request.data.get('cron', None)

        if not cron_expression:
            return Response({'error': 'Cron expression is required.'},
                            status=status.HTTP_400_BAD_REQUEST)

        if not self.is_valid_cron_expression(cron_expression):
            return Response({'error': 'Invalid Cron expression.'},
                            status=status.HTTP_400_BAD_REQUEST)

        return super().update(request, *args, **kwargs)

    def is_valid_cron_expression(self, cron_expression):
        try:
            croniter(cron_expression)
            return True
        except:
            return False
