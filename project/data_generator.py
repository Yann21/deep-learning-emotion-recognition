from tensorflow.python.keras.utils.data_utils import Sequence

from index import *
from db_operations import *

import pandas as pd
import numpy as np
from numpy.random import permutation

from os import listdir
import re


############## PREPROCESSING FUNCTIONS ##############
def sliding_window(signal, window_size, function):
  ma = []
  for i in range(len(signal)):
    w = 0
    local_average = []
    while w < window_size and 0 <= i-w:
      local_average.append(signal[i-w])
      w += 1
    ma.append(sum(local_average) / len(local_average))
  return ma

def moving_average(signal, window_size):
  average_fun = lambda tab: sum(tab) / float(window_size)
  return sliding_window(signal, window_size, average_fun)



class DataGenerator(Sequence):
    """ Custom data generator
    
    Taskes with ordering, processing and generating data batches for
    the whole spectrum of available data.
    Middle.wo.man between database extraction and the ML architecture.
    
    * Single batch generation from DB for training
    * Handles permutation of batch order
    * Feature selection
    # Data fusion
    # Data augmentation
    
    @ training     = 20 epochs / cycles
    @ epoch        = 9 samples / interviews
    @ batch        = 8 sequences
    @ sequence     = 128 frames (5.12s)
    @ feature dim  = At the discretion of the user, £[1, 941]
    
    """
    
    def __init__(self, data_size, sequence_size, batch_size, 
                     features, application='train', metric='arousal',
                     toggle_preproces=False, toggle_auto_training=False, *args):
        'User variables                      # ------------------------------------------- '
        self.data_size      = data_size      #  Number of rows per interview      (int)
        self.batch_size     = batch_size     #  Number of sequences per batch     (int)
        self.sequence_size  = sequence_size  #  Number of frames per sequence     (int)
        self.features       = features       #  List of features to be imported   (*string)
        self.application    = application    #  Toggle validation set             (bool)
        self.metric         = metric
        self.toggle_auto_training  = toggle_auto_training
        self.toggle_preproces= toggle_preproces
        
        'Data generation variables           # ------------------------------------------- '
        self._training_step = 0              #  Training progress per sample
        self._sample_data   = None           #  Data in memory (raw)
        self._sample_labels = None           #  Labels in memory
        self._samples_queue = None           #  Waiting queue
        
        'Sonder-variable'
        self.sonder_switch  = 0
        self.sonder_var     = 8              # Number of interviews in the set
        
        'Intialization functions             # ------------------------------------------- '
        self._create_queue()                 #  Random exploration of samples
        self._load_next_sample()             #  Load first sample
    
    
    def __len__(self):
        'Total iterations per epoch'
        return int(np.floor(float(self.data_size) / self.batch_size / self.sequence_size)) * self.sonder_var
    
    
    def _create_queue(self):
        'Generate a random order of interview exploration'
        path = "{}{}/".format(tag_to_path['ECG'], self.metric)
        re_matches = [re.findall(self.application + '_\d', p) for p in listdir(path)]
        self._samples_queue = list(permutation([e[0] for e in re_matches if e != []]))
        
        
    def _load_next_sample(self):
        'Returns MultiIndex table with the selected data'
        # Grab next in line
        sample = self._samples_queue.pop(0)
        
        # Load data and labels
        labels = extract_labels_arff(tag_to_path['Gold Standard'], sample).iloc[:, self.sonder_switch]
        
        if self.toggle_preproces:
        	print('DEBUG whats in the box: ', self.preprocessing(labels)
            self._sample_labels = self.preprocessing(labels)
        else:
            self._sample_labels = labels
        
        if self.toggle_auto_training:
          self._sample_data = _sample_labels
        else:
          self._sample_data = multiindex_from_tag(self.features, self.metric, sample)
    
    
    def __getitem__(self, idx):
        'Generate current batch'
        # Load next interview if you run out of data
        if self._training_step >= np.floor(float(self.data_size) / self.batch_size / self.sequence_size):
            self._training_step = 0
            self._load_next_sample()
        
        # Batches with LSTM-friendly dimensions
        batch_x = np.empty((self.batch_size, self.sequence_size, self._sample_data.shape[1]))
        batch_y = np.empty((self.batch_size, 1))
        
        ## Sequence slicing and dicing
        slice_data_sequence = lambda n: pd.IndexSlice[
            self.sequence_size * (self._training_step * self.batch_size + n):
            self.sequence_size * (self._training_step * self.batch_size + n + 1) - 1] # Pandas indexing is like a closed interval        
        # Labels slicing
        slice_labels = lambda n: pd.IndexSlice[
            self.sequence_size * (self._training_step * self.batch_size + n + 1)] # Predict next value
        
	  print('QUICK IMPORT DEBUG:', self._sample_data)
        
        # Setting up sequences for this batch
        for n in range(self.batch_size):
            # Verify there's no corrupted data
            concatenated = self._sample_data.loc[slice_data_sequence(n), :]
            # Apply our custom fusion
            batch_x[n] = self._custom_fusion(concatenated.to_numpy())
            batch_y[n] = self._sample_labels[slice_labels(n)]
            
            if concatenated.isnull().values.any():
                print("Missing data NaN values, aborting..")
                sys.exit()
        
        self._training_step += 1
        return batch_x, batch_y
    
    
    def debug(self):
        return 0
    
    
    def _custom_fusion(self, df):
        'Fusion of different types of data'
        return df
    
    
    def on_epoch_end(self):
        'Reset training variables and shuffle the deck'
        self._training_step = 0
        self._create_queue()
        self._load_next_sample()
        
        
    def preprocessing(self, labels):
        'Moving average'
        WINDOW_SIZE = 150
        print('DEBUG types:', type(labels), type(moving_average(labels, 150))
        return moving_average(labels, WINDOW_SIZE)

