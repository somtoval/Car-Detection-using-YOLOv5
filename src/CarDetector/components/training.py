from CarDetector.config.configuration import ConfigurationManager
from CarDetector.entity.config_entity import ModelTrainerConfig

import os
import subprocess
from pathlib import Path
import shutil

class Training:
    def __init__(self, config: ModelTrainerConfig):
        self.config = config

    def setup_data_config(self):
        # Create YAML file for YOLO training
        with open(os.path.join(self.config.root_dir, 'data.yaml'), 'w') as f:
            # We do .. so if we run "python yolov5/train.py" it does not assume that our data path is yolov5/artifcats/data_ingestion so we are leaving yolov5 directory
            f.write(f'path: ../{self.config.data_dir}\n')
            f.write('train: train/images\n')
            f.write('val: val/images\n\n')
            f.write('names:\n')
            f.write('  0: car\n')

    # def train(self):
    #     # Train the YOLO model
    #     os.system(f'python train.py --img 640 --batch 16 --epochs 30 --data {self.config.root_dir}/data.yaml --weights yolov5s.pt --cache')

    def train(self):
        # Clone yolo
        # os.system(f'git clone https://github.com/ultralytics/yolov5.git')

        # Install yolo requirements
        os.system('pip install -r yolov5/requirements.txt')

        # Train the YOLO model
        os.system(f'python yolov5/train.py --img 640 --batch 16 --epochs 30 --data {self.config.root_dir}/data.yaml --weights yolov5s.pt --cache')

        # # Train the YOLO model
        # command = [
        #     'python', 'yolov5/train.py',
        #     '--img', '640',
        #     '--batch', '16',
        #     '--epochs', '30',
        #     '--data', f'{self.config.root_dir}/data.yaml',
        #     '--weights', 'yolov5s.pt',
        #     '--cache'
        # ]
        
        # result = subprocess.run(command, capture_output=True, text=True)
        # print(result.stdout)  # Output of the training command
        # print(result.stderr)  # Error output, if any
