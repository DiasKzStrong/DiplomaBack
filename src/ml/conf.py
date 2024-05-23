from pydantic_settings import BaseSettings
from functools import cache


class MlConfig(BaseSettings):
    dictionary_path: str = "ml/datasets/my_dictionary.txt"
    transformer_name: str = "bert-base-multilingual-uncased"


@cache
def get_ml_config() -> MlConfig:
    return MlConfig()


ml_config = get_ml_config()
