from dataclasses import dataclass
from pathlib import Path

@dataclass
class DataIngestionConfig:
    root_dir: Path
    source_path: str
    local_data_file: Path
    unzip_dir: Path
    train_split_ratio: float
    test_split_ratio: float
    valid_split_ratio: float

@dataclass
class ModelTrainerConfig:
    root_dir: Path
    trained_model_path: Path
    params_epochs: int
    params_image_size: list
    data_dir: Path
    data_config_path: Path

@dataclass(frozen=True)
class EvaluationConfig:
    path_of_model: Path
    training_data: Path
    all_params: dict
    params_image_size: list
    params_batch_size: int