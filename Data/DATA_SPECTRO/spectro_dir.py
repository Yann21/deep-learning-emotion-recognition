import os
import wave
import pylab
import pandas as pd


def get_wav_info(wav_file):
    wav = wave.open(wav_file, 'r')
    frames = wav.readframes(-1)
    sound_info = pylab.fromstring(frames, 'int16')
    frame_rate = wav.getframerate()
    wav.close()
    return sound_info, frame_rate

### FONCTION CREATION SPECTROGRAMME ###

def graph_spectrogram(wav_file, name, path):
    sound_info, frame_rate = get_wav_info(wav_file)
    pylab.figure(num=None, figsize=(19, 12))
    pylab.subplot(111)
    pylab.title('spectrogram of %r' % wav_file)
    pylab.specgram(sound_info, Fs=frame_rate)
    pylab.savefig(path+name)
    


def create_spectro_dir(delete):
    """ Cette fonction permet de créer tous les spectrogrammes correspondants aux fichiers .wav présents dans l'arborescence
        delete : boolean indiquant si l'on supprimer ou non les fichiers .wav
    """
    for dossier in os.listdir('.') : # on parcourt tous les dossiers du répertoire courant
        if os.path.isdir(dossier): # si c'est bien un dossier 
            cpt = 0
            for wav in os.listdir('./'+dossier+'/') : # on parcours tous les fichiers .wav de ce repertoire
                if not os.path.isdir(wav) : # si c'est bien un fichier .wav
                    print("Spectrogramme du fichier :",'./'+dossier+'/'+wav,"crée") # trace d'exécution
                    graph_spectrogram('./'+dossier+'/'+wav, str(cpt) + '.png', './'+dossier+'/') # création du spectrogramme
                    
                    if delete : # on choisit de supprimer ou non les fichiers .wav
                        os.remove('./'+dossier+'/'+wav) # supprime le fichier .wav
                    cpt += 1

    print("FIN : Les fichiers sont tous traités")


def trouve_labels(num_dossier, csv_file):
	df = pd.read_csv(csv_file)
	matrice = df.as_matrix()

	arousal = 0
	valence = 0

	for ligne in matrice : 
		if str(ligne[0]) == num_dossier :
			arousal = ligne[1]
			valence = ligne[2]
			break

	return arousal, valence

def compte_data():
    """ Cette fonction permet de compter le nombre de données qu'il y'a dans l'arborescence
    """
    cpt = 0
    for dossier in os.listdir('.') : # on parcourt tous les dossiers du répertoire courant
        if os.path.isdir(dossier): # si c'est bien un dossier 
            for file in os.listdir('./'+dossier+'/') : # on parcours tous les fichiers .wav de ce repertoire
                if not os.path.isdir(file) : # si c'est bien un fichier .wav
                    cpt += 1

    print("Il y'a ::",cpt,"données")


def create_csv(csv_file):

	csv = []
	colonnes = ['fichier', 'arousal', 'valence']
	for dossier in os.listdir('.') : # on parcourt tous les dossiers du répertoire courant
		if os.path.isdir(dossier): # si c'est bien un dossier 
			arousal, valence = trouve_labels(dossier, csv_file) # à changer
			for file in os.listdir('./'+dossier+'/') : # on parcours tous les fichiers .wav de ce repertoire
				if not os.path.isdir(file) : # si c'est bien un fichier .wav
					ligne = ['DATA_SPECTRO/'+dossier+'/'+file, arousal, valence]
					csv.append(ligne)

	df = pd.DataFrame(csv, columns = colonnes)

	df.to_csv('labels_spectro.csv', encoding='utf-8')

#create_csv('labels.csv')

#DELETE = True
#create_spectro_dir(DELETE)
#compte_data()dossier

#df = pd.read_csv('labels_spectro.csv')
#matrice = df.as_matrix()
#print(df)

