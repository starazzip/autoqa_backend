class RedisKeyGeneratorService:

    @staticmethod
    def get(api: str, **kwargs):
        cache_key = f'{api}'
        for key, value in kwargs.items():
            if value is None:
                cache_key += f'_{key}_None'
            else:
                cache_key += f'_{key}_{value}'
        return cache_key
