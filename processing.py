'''
This script reads an export of a WhatsApp group chat
and counts the amount of specific emojis per person
'''

from datetime import datetime
from typing import Tuple
import pandas as pd

EMOJIS_TO_TRACK = ['🗄️', '💩']
VALID_USERS = {
    "Tomas Contreras": "Tom",
    "Javier Graell": "Xavi",
    "El Sancho": "Sancho",
    "Juano": "Juanito",
    "El Che": "Che",
    "Doble Peli": "Peli"
}
EMOJIS_TO_TEXT = {'💩': "caca", '🗄️': "caca laboral"}

def extract_user_and_datetime(message: str) -> Tuple[datetime, str]:
    datetime_str, _, rest = message.partition(' - ')
    datetime_str = datetime_str.strip().replace(' p. m.', ' PM').replace(' a. m.', ' AM')
    parts = datetime_str.split('/')
    parts[0], parts[1] = parts[0].zfill(2), parts[1].zfill(2)  # Zero-padding for day and month
    datetime_str = '/'.join(parts)
    datetime_obj = datetime.strptime(datetime_str, '%d/%m/%Y, %I:%M %p')

    user, _, _ = rest.partition(':')
    return datetime_obj, user.strip()

def count_user_emojis(filename: str) -> pd.DataFrame:
    user_emoji_data = []

    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            # HARCODED: replace 💩🗄️ with only 🗄️ to avoid colissions.
            line = line.replace('💩🗄️', '🗄️')
            if ' - ' in line:
                datetime_obj, username = extract_user_and_datetime(line)

                if username not in VALID_USERS:
                    continue

                for emoji in EMOJIS_TO_TRACK:
                    emoji_count = line.count(emoji) if emoji in line else 0

                    if emoji_count > 0:
                        user_emoji_data.append({
                            'datetime': datetime_obj.strftime('%Y-%m-%d %H:%M:%S'),
                            'user': VALID_USERS[username],
                            'emoji': EMOJIS_TO_TEXT[emoji],
                            'count': emoji_count
                        })

    df = pd.DataFrame(user_emoji_data)
    return df

if __name__ == '__main__':
    filename = 'cacas_latest.txt'
    user_emoji_counts = count_user_emojis(filename)
    user_emoji_counts.to_csv('data/cacas_latest.csv')