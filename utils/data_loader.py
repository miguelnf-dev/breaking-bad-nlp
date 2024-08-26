import pandas as pd
from glob import glob
import re

def load_subtitles(folder_path):
    subtitles_path = glob(folder_path + '/*/*.srt')
    
    scripts = []
    episode_number_list = []
    season_number_list = []
    
    print(f'Processing {len(subtitles_path)} subtitles files.')
    
    for file in subtitles_path:
        with open(file, 'r', encoding='utf-8', errors='replace') as f:
            lines = f.readlines()
            dialogues = [line.strip() for line in lines if not line.strip().isdigit() and '-->' not in line and line.strip()][1:]
            
        script = ' '.join(dialogues)
        match = re.search(r'[sS](\d{2})[eE](\d{2})', file)
        
        if match:
            season_number = int(match.group(1))
            episode_number = int(match.group(2))
            
        scripts.append(script)
        season_number_list.append(season_number)
        episode_number_list.append(episode_number)
    
    print('Subtitles loaded successfully. Appending the data to a DataFrame.')
    df = pd.DataFrame.from_dict({
        "Season": season_number_list,
        "Episode": episode_number_list,
        "Script": scripts
    })
    return df