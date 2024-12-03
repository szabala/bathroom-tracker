'''
This script reads an export of a WhatsApp group chat
and counts the amount of specific emojis per person
'''

from datetime import datetime
from typing import Tuple
import pandas as pd
import re

VALID_USERS = {
    "Tomas Contreras": "Tom",
    "Javier Graell": "Xavi",
    "El Sancho": "Sancho",
    "Juano": "Juanito",
    "El Che": "Che",
    "Doble Peli": "Peli",
    "Jorge Valeze": "Valeze"
}

EMOJIS_TO_TRACK = ['🗄️', '💩', '🤢', '🪠']

EMOJIS_TO_TEXT = {
    '💩': "caca", 
    '🗄️': "laboral",
    '🤢': "maloliente",
    '🪠': "tapadon",
    }

def extract_user_and_datetime(message: str) -> Tuple[datetime, str]:
    datetime_str, _, rest = message.partition(' - ')
    datetime_str = datetime_str.strip()
    parts = datetime_str.split('/')
    parts[0], parts[1] = parts[0].zfill(2), parts[1].zfill(2)  # Zero-padding for day and month
    datetime_str = '/'.join(parts)
    datetime_str = datetime_str.replace('\u202f', ' ')
    # Might need to debug date string due to whatsapp export format changes
    # print(datetime_str)
    datetime_obj = datetime.strptime(datetime_str, '%m/%d/%y, %H:%M')
    user, _, _ = rest.partition(':')
    return datetime_obj, user.strip()

def find_first_number(s: str) -> int:
    match = re.search(r'\d+', s)
    if match:
        return int(match.group())
    else:
        return None

def count_user_emojis(filename: str) -> pd.DataFrame:
    user_emoji_data = []

    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            if ' - ' in line:
                datetime_obj, username = extract_user_and_datetime(line)

                if username not in VALID_USERS:
                    continue

                emoji_count = {EMOJIS_TO_TEXT[emoji]: 0 for emoji in EMOJIS_TO_TRACK}
                is_shit = False
                for emoji in EMOJIS_TO_TRACK:
                    emoji_line_count = line.count(emoji)
                    if emoji_line_count > 0:
                        emoji_count[EMOJIS_TO_TEXT[emoji]] = emoji_line_count
                        is_shit = True
                
                if is_shit:
                    split_line = line.split('💩')
                    bristol = find_first_number(split_line[1]) if len(split_line) > 1 else None

                if is_shit:
                    data = {
                        'datetime': datetime_obj.strftime('%Y-%m-%d %H:%M:%S'),
                        'user': VALID_USERS[username],   
                        'bristol': bristol
                    }

                    # join emoji_count and data dictionaries
                    data.update(emoji_count)
                    user_emoji_data.append(data)

    df = pd.DataFrame(user_emoji_data)
    return df

if __name__ == '__main__':

    filename = 'cacas_latest.txt'
    user_emoji_counts = count_user_emojis(filename)
    user_emoji_counts.to_csv('data/cacas_latest.csv')