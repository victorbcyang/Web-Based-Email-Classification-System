import os
import random
import shutil
import tarfile
import numpy as np

class DataPrepare:
    def __init__(self):
        self.data_path = "data" # directory of data
        
    def extract(self, name, path):
        filename = os.path.join(self.data_path, name)
        file = tarfile.open(filename)
        file.extractall(path)
        msg = "Extracted file stored at: " + path
        print(msg)
        
        train_path = os.path.join(path, 'data/train')
        test_path = os.path.join(path, 'data/test')
        
        return train_path, test_path
        
    def subsample(self, train_path, target_path):
        if not os.path.isdir(target_path):
            os.mkdir(target_path)
        
        folders_train = [f for f in os.listdir(train_path)]
        
        for folder in folders_train:
            if not os.path.isdir(os.path.join(target_path, folder)):
                os.mkdir(os.path.join(target_path, folder))
                
        num_file = []
        for c in folders_train:
            _, _, num = next(os.walk(os.path.join(train_path, c)))
            num_file.append(len(num))
            
        file_name = {}
        for folder in folders_train:
            file_name[folder] = []
            for file in os.listdir(os.path.join(train_path, folder)):
                file_name[folder].append(str(file))
            file_name[folder] = random.sample(file_name[folder], min(num_file))
            
        for folder in folders_train:
            org_pth = os.path.join(train_path, folder)
            tar_pth = os.path.join(target_path, folder)
            
            for name in file_name[folder]:
                shutil.copy(os.path.join(org_pth, name), os.path.join(tar_pth, name))
        msg = "Subsampled file stored at: " + target_path
        return target_path
                
        
        