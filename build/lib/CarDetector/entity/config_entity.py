from dataclasses import dataclass

@dataclass
class DataIngestionConfig:
    train_file_path: str 
    test_file_path: str
    valid_file_path: str
    train_split_ratio: float
    test_split_ratio: float
    valid_split_ratio: float