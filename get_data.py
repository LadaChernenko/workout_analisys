import requests
import time
from fire import Fire
import json
from pathlib import Path
from tqdm import tqdm
from constants import ACCESS_TOKEN, GROUP_IG


def get_posts_by_hashtag_year(access_token, group_id, year, count=100):

    # Определяем начало и конец годового диапазона в UNIX timestamp
    start_date = int(time.mktime(time.strptime(f"01.01.{year}", "%d.%m.%Y")))  # Начало 2023 года
    end_date = int(time.mktime(time.strptime(f"31.12.{year} 23:59:59", "%d.%m.%Y %H:%M:%S")))  # Конец 2023 года

    all_posts = []
    offset = 0
    
    while True:
        url = "https://api.vk.com/method/wall.get"
        params = {
            "access_token": access_token,
            "owner_id": group_id,
            # "query": hashtag,
            "count": count,
            "offset": offset,
            "v": "5.131"  # Версия API
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            # Проверяем, есть ли посты в ответе
            if "response" in data and data["response"]["items"]:
                posts = data["response"]["items"]
                
                # Фильтруем посты по дате
                for post in posts:
                    post_date = post['date']
                    if start_date <= post_date <= end_date:
                        # Форматируем дату, день недели и сохраняем только нужные данные
                        all_posts.append({
                            "date": time.strftime('%d.%m.%Y %H:%M:%S', time.localtime(post_date)),
                            "weekday": time.strftime('%A', time.localtime(post_date)),  # Получаем название дня недели
                            "text": post['text']
                        })
                
                # Увеличиваем offset для следующего запроса
                offset += count
                
                # Если вернулось меньше постов, чем запросили, значит, достигли конца
                if len(posts) < count:
                    break
            else:
                # Прекращаем, если больше нет постов
                break
        else:
            print(f"Failed to connect to VK API. Status code: {response.status_code}")
            break

    return all_posts

def main(year, count):
    # Получаем все посты по хэштегу за указанный год
    posts = get_posts_by_hashtag_year(ACCESS_TOKEN, GROUP_IG, year, count)

    # Сохраняем результат в JSON-файл
    with open(f"posts_{year}.json", "w", encoding="utf-8") as file:
        json.dump(posts, file, ensure_ascii=False, indent=4)

    print(f"Сохранено {len(posts)} постов в файл 'posts.json'.")



if __name__=='__main__':
    Fire(main)