from CarDetector.entity.config_entity import DataIngestionConfig, ModelTrainerConfig, EvaluationConfig
from CarDetector.constants import CONFIG_FILE_PATH, PARAMS_FILE_PATH
from CarDetector.utils.common import read_yaml, create_directories
from pathlib import Path

class ConfigurationManager:
    def __init__(self):
        config_filepath = CONFIG_FILE_PATH
        params_filepath = PARAMS_FILE_PATH

        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)

        create_directories([self.config.artifacts_root])

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion

        create_directories([config.root_dir])

        data_ingestion_config = DataIngestionConfig(
            root_dir=config.root_dir,
            source_path=config.source_path,
            local_data_file=config.local_data_file,
            unzip_dir=config.unzip_dir,
            train_split_ratio=self.params.TRAIN_SPLIT_RATIO,
            test_split_ratio=self.params.TEST_SPLIT_RATIO,
            valid_split_ratio=self.params.VALID_SPLIT_RATIO
        )

        return data_ingestion_config
    
    def get_training_config(self) -> ModelTrainerConfig:
        training = self.config.training
        create_directories([Path(training.root_dir)])

        training_config = ModelTrainerConfig(
            root_dir=Path(training.root_dir),
            trained_model_path=Path(training.trained_model_path),
            params_epochs=self.params.EPOCHS,
            params_image_size=self.params.IMAGE_SIZE,
            data_dir=self.config.training.data_dir,
            data_config_path=self.config.training.data_config_path,
        )

        return training_config
    
    def get_validation_config(self) -> EvaluationConfig:
        eval_config = EvaluationConfig(
            path_of_model=Path("yolov5/runs/train/exp/weights/best.pt"),
            training_data=Path("artifacts/data_ingestion/test"),
            all_params=self.params,
            params_image_size=self.params.IMAGE_SIZE,
            params_batch_size=self.params.BATCH_SIZE
        )
        return eval_config

    

