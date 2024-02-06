'''
This script reads an export of a WhatsApp group chat
and counts the amount of specific emojis per person
'''

## COUNTING
from datetime import datetime
from typing import Tuple
import pandas as pd

EMOJIS_TO_TRACK = ['💩🗄️', '💩']

VALID_USERS = set(
    [
        "Tomas Contreras",
        "Javier Graell",
        "El Sancho",
        "Juano",
        "El Che",
        "Doble Peli"
    ]
)

EMOJIS_TO_TEXT = {
    '💩': "caca",
    '💩🗄️': "caca en el trabajo"
}

NAMES_TO_NICKS = {
    "Tomas Contreras": "Tom",
    "Javier Graell": "Xavi",
    "El Sancho": "Sancho",
    "Juano": "Juanito",
    "El Che": "Che",
    "Doble Peli": "Peli"
}

def extract_user_and_datetime(message: str) -> Tuple[datetime, str]:
    datetime_str, _, rest = message.partition(' - ')
    datetime_str = datetime_str.strip()
    datetime_str = datetime_str.replace(' p. m.', ' PM').replace(' a. m.', ' AM')
    parts = datetime_str.split('/')
    parts[0] = parts[0].zfill(2)  # Day
    parts[1] = parts[1].zfill(2)  # Month
    datetime_str = '/'.join(parts)
    datetime_obj = datetime.strptime(datetime_str, '%d/%m/%Y, %I:%M %p')

    user, _, _ = rest.partition(':')

    return datetime_obj, user.strip()

def count_user_emojis(filename: str) -> pd.DataFrame:
    user_emoji_data = []

    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            if ' - ' in line:
                datetime_obj, username = extract_user_and_datetime(line)

                if username not in VALID_USERS:
                    continue

                for emoji in EMOJIS_TO_TRACK:
                    # Check for an exact match of the emoji in the line
                    emoji_count = line.count(emoji) if emoji in line else 0

                    if emoji_count > 0:
                        user_emoji_data.append({
                            'date': datetime_obj.strftime('%Y-%m-%d'),
                            'user': NAMES_TO_NICKS[username],
                            'emoji': EMOJIS_TO_TEXT[emoji],
                            'count': emoji_count
                        })

    df = pd.DataFrame(user_emoji_data)
    df = df.pivot_table(index=['date', 'user'], columns='emoji', values='count', fill_value=0, aggfunc='sum')
    return df


if __name__ == '__main__':
    # Use the function
    filename = 'cacas_latest.txt'
    user_emoji_counts = count_user_emojis(filename)
    # save to csv
    user_emoji_counts.to_csv('data/cacas_latest.csv')