import json

from django.core.cache import cache
from django.db.models.signals import post_save
from django.dispatch import receiver
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from injector import inject
from pydantic import BaseModel, ValidationError
from rest_framework import generics, serializers, status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from AutoQA.models import Brand, GherkinFeatures, GherkinScenarios, TestEnvironment
from AutoQA.services.gherkin_services import GherkinServices
from AutoQA.services.redis_key_generator_service import RedisKeyGeneratorService

API_GERKIN = 'GERKIN'


# 當Gherkins 內容有變動的時候，將redis的內容清除
@receiver(post_save, sender=GherkinFeatures)
def update_redis_cache(sender, instance, **kwargs):
    key = RedisKeyGeneratorService.get(API_GERKIN,
                                       brand=instance.brand.id,
                                       environment=instance.environment.id)
    if cache.get(key) is not None:
        cache.set(key, None, timeout=3600)

    all_gherkin_key = RedisKeyGeneratorService.get(API_GERKIN, brand=None, environment=None)
    if cache.get(all_gherkin_key) is not None:
        cache.set(all_gherkin_key, None, timeout=3600)


class GherkinData(BaseModel):
    feature_name: str
    feature_description: list
    scenarios: list


class FileUploadView(APIView):
    parser_classes = (MultiPartParser, )

    @inject
    def setup(self, request, gherkin_service: GherkinServices):
        super().setup(request)
        self._gherkin_service = gherkin_service

    def post(self, request, format=None):
        uploaded_file = request.FILES.get('file')
        brand_id = request.data.get('brand')
        environment_id = request.data.get('environment')

        if not uploaded_file:
            return Response({'error': 'No file uploaded.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            content = uploaded_file.read().decode('utf-8')
        except Exception as e:
            return Response({'error': 'Invalid file content.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            json_data = json.loads(content)
            for data in json_data:
                GherkinData(**data)
        except json.JSONDecodeError:
            return Response({'error': 'Invalid JSON format.'}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response({'error': f'Invalid data format: {e}'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            self._gherkin_service.save_into_db(brand_id=brand_id,
                                               environment_id=environment_id,
                                               gherkins=json_data)
        except (Brand.DoesNotExist, TestEnvironment.DoesNotExist):
            return Response({'error': 'Invalid brand or environment ID.'},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'File uploaded and data format is valid.'},
                        status=status.HTTP_201_CREATED)


class GherkinListView(generics.ListAPIView):

    @inject
    def setup(self, request, gherkin_service: GherkinServices):
        super().setup(request)
        self._gherkin_service = gherkin_service

    # @swagger_auto_schema(manual_parameters=[
    #     openapi.Parameter('brand',
    #                       openapi.IN_QUERY,
    #                       description="Brand",
    #                       type=openapi.TYPE_STRING,
    #                       enum=list(Brand.objects.values_list('brand', flat=True))),
    #     openapi.Parameter('environment',
    #                       openapi.IN_QUERY,
    #                       description="Environment",
    #                       type=openapi.TYPE_STRING,
    #                       enum=list(TestEnvironment.objects.values_list('environment', flat=True))),
    # ])
    def get(self, request: Request):
        brand = request.query_params.get('brand')
        env = request.query_params.get('environment')

        key = key = RedisKeyGeneratorService.get(API_GERKIN, brand=brand, environment=env)
        gherkin = cache.get(key)
        if gherkin is not None:
            return Response(gherkin)
        else:
            gherkin = self._gherkin_service.get_gherkin(brand, env)
            cache.set(key, gherkin, timeout=3600)
            return Response(gherkin)
