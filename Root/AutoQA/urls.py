"""
URL configuration for AutoQA project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from AutoQA.views.execution_view import (
    BrandListView,
    EnvironmentListView,
    ExecutionTaskDetailView,
    ExecutionTaskListView,
)
from AutoQA.views.gherkin_view import FileUploadView, GherkinListView
from AutoQA.views.scheduled_view import ScheduledTaskDetailView, ScheduledTaskListView

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny, ),
)
urlpatterns = [
    # execution
    path('execution/brand/', BrandListView.as_view(), name='Get Brand List'),
    path('execution/environment/', EnvironmentListView.as_view(), name='Get Environment List'),
    path('execution/task', ExecutionTaskListView.as_view(), name='List Execution Task'),
    path('execution/task/<int:pk>/', ExecutionTaskDetailView.as_view(),
         name='ExecutionTask Detail'),

    # scheduled
    path('scheduled/task/', ScheduledTaskListView.as_view(), name='scheduled-task-list'),
    path('scheduled/task/<int:pk>/',
         ScheduledTaskDetailView.as_view(),
         name='scheduled-task-detail'),
    # gherkin
    path('gherkin/upload/', FileUploadView.as_view(), name='gherkin-upload'),
    path('gherkin/', GherkinListView.as_view(), name='Get Gherkins'),

    # swagger
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
