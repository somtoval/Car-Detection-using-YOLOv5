from CarDetector.entity.config_entity import DataIngestionConfig
from CarDetector.constants import CONFIG_FILE_PATH, PARAMS_FILE_PATH
from CarDetector.utils.common import read_yaml, create_directories

class ConfigurationManager:
    def __init__(self):
        config_filepath = CONFIG_FILE_PATH
        params_filepath = PARAMS_FILE_PATH

        self.config = read_yaml(config_filepath)
        self.params = read_yaml(params_filepath)

        create_directories([self.config.artifact_root])

    def get_data_ingestion(self) -> DataIngestionConfig:
        config = self.config.data_ingestion

        create_directories([config.root_dir])

        data_ingestion_config = DataIngestionConfig(
            root_dir=config.root_dir,
            source_dir=config.source_path,
            local_data_file=config.local_data_file,
            unzip_dir=config.unzip_dir
            train_split_ratio=params.TRAIN_SPLIT_RATIO
            test_split_ratio=params.TEST_SPLIT_RATIO
            valid_split_ratio=params.VALID_SPLIT_RATIO
        )

        return data_ingestion_config
    

