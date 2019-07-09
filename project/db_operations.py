from index import *
import pandas as pd
import arff
from numpy.random import randint

# Extaction of data in ARFF format
def extract_arff(path):
    """ extract_arff(str)
    
    @return: DataFrame with the arff
    @require: liac-arff module
    """
    df = None
    with open(path) as f:
        dataset = arff.load(f)
        df = pd.DataFrame(dataset['data'])
    
    return df

def extract_labels_arff(path, individual):
    """ extract_av_arff(str, str)
    
    @return: DataFrame with valence and arousal side by side
    And as a bonus the columns are formatted 
    """
    
    # Extracts arff
    arousal_arff = extract_arff(path + "arousal/" + individual + '.arff')
    valence_arff = extract_arff(path + "valence/" + individual + '.arff')
    
    # Rename the axes and stack both df into the first
    arousal_arff.columns = ['id', 'time_step', 'arousal']
    arousal_arff['valence'] = valence_arff[2] # 3rd column contains the data
    
    # Return onyl Arousal and Valence
    return arousal_arff.loc[:, 'arousal':'valence']


def extract_labels(individual):
    'Extracts the arousal labels for an individual'
    arousal_arff = extract_arff(tag_to_path['Gold Standard'] + "arousal/" + individual + '.arff')
    valence_arff = extract_arff(tag_to_path['Gold Standard'] + "valence/" + individual + '.arff')
    arousal_arff.columns = ['id', 'time_step', 'arousal']
    arousal_arff['valence'] = valence_arff[2] # 3rd column contains the data
    labels = arousal_arff.loc[:, 'arousal':'valence']
    
    return labels.iloc[:, 0]

    
def multiindex_from_tag(tags, metric, sample):
    # Pandas dataframe rejig: set starting column index at 0
    def reorder_columns(dataframe):
        dataframe.columns = [i for i in range(len(dataframe.columns))]
        return dataframe
    
     # List of the full paths to data
    data_paths = ["{}{}/{}.arff".format(tag_to_path[t], metric, sample) for t in tags]
    # List of DataFrames, strip off the first column (timestamp) and reorder the rest
    data_array = [reorder_columns(extract_arff(p).iloc[:, 1:]) for p in data_paths]
    # Create MultiIndex container ordered by tags
    multiindex_data = pd.concat(data_array, axis=1, keys=tags)
    
    return multiindex_data


def choose_random_patient(application='train'):
    return application+ '_' + str(randint(1,10))

