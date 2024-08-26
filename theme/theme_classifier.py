import torch
from transformers import pipeline
import nltk
import pandas as pd
import os
import sys
import pathlib

folder_path = pathlib.Path(__file__).parent.resolve()
sys.path.append(os.path.join(folder_path,'../'))
from utils import load_subtitles

nltk.download('punkt')

class ThemeClassifier():
    def __init__(self, themes_list):
        self.model_id ='facebook/bart-large-mnli'
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.themes_list = themes_list
        self.model = self.load_model(self.device)
        
    def load_model(self,device):
        model = pipeline(
            'zero-shot-classification', 
            model=self.model_id,
            device=device
        )
        
        return model
    
    def get_theme_scores(self,script):
        script_sentences = nltk.sent_tokenize(script)
        
        #batch sentence to avoid memory error
        sentence_batch_size = 20
        script_batches = []
        for i in range(0, len(script_sentences), sentence_batch_size):
            sentence = " ".join(script_sentences[i:i+sentence_batch_size])
            script_batches.append(sentence)
        
        # run model    
        theme_scores = self.model(
            script_batches[:2], 
            self.themes_list,
            multi_label=True)
        
        # average the scores across the batches  
        themes= {}
        for output in theme_scores:
            for label, score in zip(output['labels'], output['scores']):
                if label not in themes:
                    themes[label] = []
                themes[label].append(score)
        
        themes = {k: sum(v)/len(v) for k, v in themes.items()}
        
        return themes
    
    def get_themes(self, folder_path, output_path=None):
            # Load data if already exists
            if output_path is not None and os.path.exists(output_path):
                dataframe = pd.read_csv(output_path)
                return dataframe
            else:
                print('No existing data found. Loading subtitles and inferring themes.')
                
            dataframe = load_subtitles(folder_path)
            dataframe = dataframe.head(2)
            
            # Infer themes
            output_themes = dataframe['Script'].apply(self.get_theme_scores)
            theme_dataframe = pd.DataFrame(output_themes.tolist())
            dataframe = pd.concat([dataframe, theme_dataframe], axis=1)
            
            # Save the dataframe
            if output_path is not None:
                dataframe.to_csv(output_path, index=False)
            
            return dataframe