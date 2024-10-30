from CarDetector.config.configuration import ConfigurationManager
from CarDetector.utils.common import get_size
from CarDetector.entity.config_entity import DataIngestionConfig
from CarDetector import logger
from pathlib import Path

import pandas as pd
import cv2
import numpy as np

import os
import shutil
import zipfile
import random

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config

        # Create directories if they don't exist
        os.makedirs(f'{self.config.root_dir}/train/images', exist_ok=True)
        os.makedirs(f'{self.config.root_dir}/test/images', exist_ok=True)
        os.makedirs(f'{self.config.root_dir}/val/images', exist_ok=True)

        os.makedirs(f'{self.config.root_dir}/train/labels', exist_ok=True)
        os.makedirs(f'{self.config.root_dir}/test/labels', exist_ok=True)
        os.makedirs(f'{self.config.root_dir}/val/labels', exist_ok=True)

    def get_file(self):
        if not os.path.exists(self.config.local_data_file):
            shutil.copy(self.config.source_path, self.config.local_data_file)
        else:
           logger.info(f"File already exists of size: {get_size(Path(self.config.local_data_file))}")   

    def extract_zip_file(self):
        """
        zip_file_path: str
        Extracts the zip file into the data directory
        Function returns None
        """
        unzip_path = self.config.unzip_dir
        os.makedirs(unzip_path, exist_ok=True)
        with zipfile.ZipFile(self.config.local_data_file, 'r') as zip_ref:
            zip_ref.extractall(unzip_path)

    def convert_bbox_yolo(self, size, bbox):
        """
            Function to convert bbox to YOLO format
        """
        dw = 1. / size[0]
        dh = 1. / size[1]
        x = (bbox[0] + bbox[1]) / 2.0 - 1
        y = (bbox[2] + bbox[3]) / 2.0 - 1
        w = bbox[1] - bbox[0]
        h = bbox[3] - bbox[2]
        x = x * dw
        w = w * dw
        y = y * dh
        h = h * dh
        return (x, y, w, h)
    
    def process_bbox(self):
        # Collect all image files
        list_of_images = []
        for root, _, files in os.walk(os.path.join(self.config.root_dir, 'data')):
            for file in files:
                if file.endswith(('jpg', 'jpeg', 'png')):
                    list_of_images.append(file)
        print(list_of_images)

        bbox_csv = pd.read_csv(os.path.join(self.config.root_dir, 'data/train_solution_bounding_boxes.csv'))
        for idx, data in bbox_csv.groupby('image'):
            image_path = os.path.join(self.config.root_dir, 'data', idx)
            try:
                img = cv2.imread(image_path)
                if img is None:
                    print(f"Warning: Unable to read image {image_path}")
                    continue
                else:
                    print('gffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffg')
                    height, width, _ = img.shape
                    data = data[['xmin', 'xmax', 'ymin', 'ymax']].values
                    yolo_bboxes = [self.convert_bbox_yolo((width, height), bbox) for bbox in data]
                    yolo_bboxes = np.array(yolo_bboxes).astype(str)

                    if idx in list_of_images:
                        with open(os.path.join(self.config.root_dir, 'data', f'{idx.replace(".jpg", "")}.txt'), 'w+') as f:
                            for bbox in yolo_bboxes:
                                text = '0 ' + ' '.join(bbox)
                                f.write(text + '\n')
                    
            except Exception as e:
                print(f"Error processing image {image_path}: {e}")    

    # def split_data(self):
    #     train_split = self.config.train_split_ratio
    #     test_split = self.config.test_split_ratio
    #     val_split = self.config.val_split_ratio

    #     # Collect all image files
    #     images = []
    #     for root, _, files in os.walk(self.config.root_dir):
    #         for file in files:
    #             if file.endswith(('jpg', 'jpeg', 'png')):
    #                 images.append(os.path.join(root, file))

    #     # Shuffle and split data
    #     random.shuffle(images)
    #     data_size = len(images)
    #     train_size = int(data_size * train_split)
    #     val_size = int(data_size * val_split)
    #     test_size = data_size - train_size - val_size

    #     # Move files to respective directories
    #     for img in images[:train_size]:
    #         shutil.move(img, f'{self.config.root_dir}/train/images')

    #     for img in images[train_size:train_size + val_size]:
    #         shutil.move(img, f'{self.config.root_dir}/val/images')

    #     for img in images[train_size + val_size:]:
    #         shutil.move(img, f'{self.config.root_dir}/test/images')


    
    def split_data(self):
        # Define split sizes based on configuration ratios
        train_split = self.config.train_split_ratio
        val_split = self.config.valid_split_ratio
        test_split = self.config.test_split_ratio

        # Collect all image files
        images = [img for img in Path(self.config.root_dir).rglob("*.[jp][pn]g")]

        # Shuffle and split data
        random.shuffle(images)
        data_size = len(images)
        train_size = int(data_size * train_split)
        val_size = int(data_size * val_split)

        # Calculate the start indices for each split
        train_images = images[:train_size]
        val_images = images[train_size:train_size + val_size]
        test_images = images[train_size + val_size:]

        # Function to move images and their associated .txt files
        def move_files(image_list, split_name):
            for img_path in image_list:
                # Move the image
                img_dest = os.path.join(self.config.root_dir, split_name, 'images', img_path.name)
                shutil.move(str(img_path), img_dest)

                # Move the corresponding label file if it exists
                label_path = img_path.with_suffix('.txt')
                if label_path.exists():
                    label_dest = os.path.join(self.config.root_dir, split_name, 'labels', label_path.name)
                    shutil.move(str(label_path), label_dest)

        # Move files for each split
        move_files(train_images, 'train')
        move_files(val_images, 'val')
        move_files(test_images, 'test')