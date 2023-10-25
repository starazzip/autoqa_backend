from typing import List

from django.db.models import Q

from ..models import Brand, GherkinFeatures, GherkinScenarios, TestEnvironment


class GherkinServices:

    def save_into_db(self, brand_id: int, environment_id: int, gherkins: dict):
        brand = Brand.objects.get(pk=brand_id)
        environment = TestEnvironment.objects.get(pk=environment_id)

        features_to_update = [
            GherkinFeatures(feature=f['feature_name'], brand=brand, environment=environment)
            for f in gherkins
        ]
        # 更新存在的 GherkinFeatures

        for feature in features_to_update:
            GherkinFeatures.objects.get_or_create(brand=brand,
                                                  environment=environment,
                                                  feature=feature.feature,
                                                  defaults={
                                                      'brand_id': int(brand_id),
                                                      'environment_id': int(environment_id),
                                                      'feature': feature.feature,
                                                  })

        # 删除不需要保留的 GherkinFeatures
        GherkinFeatures.objects.filter(brand=brand, environment=environment).exclude(
            feature__in=[feature.feature for feature in features_to_update]).delete()

        scenarios_to_update: List[GherkinScenarios] = []
        for f in gherkins:
            feature = GherkinFeatures.objects.filter(feature=f['feature_name']).get()
            for s in f['scenarios']:
                scenarios_to_update.append(
                    GherkinScenarios(scenario=s['scenario_name'],
                                     brand=brand,
                                     feature=feature,
                                     environment=environment))
        # 更新存在的 GherkinScenarios
        for scenario in scenarios_to_update:
            GherkinScenarios.objects.get_or_create(brand=brand,
                                                   environment=environment,
                                                   scenario=scenario.scenario,
                                                   defaults={
                                                       'brand_id': int(brand_id),
                                                       'environment_id': int(environment_id),
                                                       'feature': scenario.feature,
                                                       'scenario': scenario.scenario,
                                                   })
        # 删除不需要保留的 GherkinScenarios
        GherkinScenarios.objects.filter(brand=brand, environment=environment).exclude(
            scenario__in=[scenario.scenario for scenario in scenarios_to_update]).delete()

    def get_gherkin(self, brand_str: str, environment_str: str):
        brand = None if brand_str is None else Brand.objects.filter(brand=brand_str).first()
        environment = None if environment_str is None else TestEnvironment.objects.filter(
            environment=environment_str).first()

        filter_condition = Q()
        if brand is not None:
            filter_condition &= Q(brand=brand)
        if environment is not None:
            filter_condition &= Q(environment=environment)
        features = GherkinFeatures.objects.filter(filter_condition)

        result = []
        for feature in features:
            is_exist = any(item['environment'] == feature.environment.environment
                           and item['brand'] == feature.brand.brand for item in result)
            if is_exist is False:
                result.append({
                    "environment": feature.environment.environment,
                    "brand": feature.brand.brand,
                    "features": []
                })
            feature_data = {"id": feature.id, "title": feature.feature, "scenarios": []}

            scenarios = GherkinScenarios.objects.filter(brand_id=feature.brand,
                                                        environment_id=feature.environment,
                                                        feature=feature)

            for scenario in scenarios:
                feature_data["scenarios"].append({"id": scenario.id, "title": scenario.scenario})

            matching_objects = [
                item for item in result if item['environment'] == feature.environment.environment
                and item['brand'] == feature.brand.brand
            ]
            assert len(matching_objects) > 0
            matching_objects[0]["features"].append(feature_data)
        return result
