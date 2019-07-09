DRIVE = True

drive = '/content/drive/My Drive/Data/RECOLA 2016/'
root  = '../../Data/RECOLA 2016/'

tag_to_path = {
    'Gold Standard'   : 'ratings/ratings_gold_standard/',
    'AUDIO'           : 'features/features_audio/',
    'ECG'             : 'features/features_ECG/',
    'EDA'             : 'features/features_EDA/',
    'HRHRV'           : 'features/features_HRHRV/',
    'SCL'             : 'features/features_SCL/',
    'SCR'             : 'features/features_SCR/',
    'Video Appearance': 'features/features_video_appearance/',
    'Geometric'       : 'features/features_video_geometric/'
  }

## Support Drive import in Google Colab
if DRIVE:
  for p in tag_to_path:
    tag_to_path[p] = drive + tag_to_path[p]
  tag_to_path['root'] = drive
else:
  for p in tag_to_path:
    tag_to_path[p] = root + tag_to_path[p]
  tag_to_path['root'] = root
  
# Dictionary {('Human readable' => 'Path name')}
tag_to_descriptor = {
    'AUDIO'           : 'features_audio',            # 4s arousal / 6s valence / 88d
    'ECG'             : 'features_ECG',              # 19d
    'EDA'             : 'features_EDA',              # 8d
    'HRHRV'           : 'features_HRHRV',            # 10d
    'SCL'             : 'features_SCL',              # 8d
    'SCR'             : 'features_SCR',              # 8d
    'Video Appearance': 'features_video_appearance', # 168d
    'Geometric'       : 'features_video_geometric',  # 632
}

descriptor_to_tag = {
    'features_audio'           : 'AUDIO',
    'features_ECG'             : 'ECG',
    'features_EDA'             : 'EDA',
    'features_HRHRV'           : 'HRHRV',
    'features_SCL'             : 'SCL',
    'features_SCR'             : 'SCR',
    'features_video_appearance': 'Video Appearance',
    'features_video_geometric' : 'Geometric'
}


tag_to_dim = {
    'AUDIO'           : 88,
    'ECG'             : 19,
    'EDA'             : 8,
    'HRHRV'           : 10,
    'SCL'             : 8,
    'SCR'             : 8,
    'Video Appearance': 168,
    'Geometric'       : 632
}

facial_localisation = {
    'Face Bounding Box': 'features_video_face_bounding_box',   # 4d Bounding box of the face at all time / Attention here
    'Facial Landmarks' : 'features_video_facial_landmarks',    # 98
}

if __name__ == __main__.py:
	print('INDEX FILE FOR PATHS')
