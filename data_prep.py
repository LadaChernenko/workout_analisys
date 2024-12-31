from fire import Fire
from pathlib import Path
import time
import re
import json
from tqdm import tqdm
import typing as tp


def diary_classifaer(data: tp.List[tp.Dict]) -> tp.List[tp.Dict]:
    new_data = []
    teg_list = ['Рутинка', '#ВызовПринят', '#ВоркаутЛикбез@swtbarboss', 'Тренировочная схема дня', ]
    week_list = ['Понедельник', 'Вторник', 'Четверг', 'Среда', 'Пятница', 'Суббота', 'Воскресенье']
    teg_set = set(teg_list)
    week_set = set(week_list)

    for day in tqdm(data):

        contains_word = any(tag in day['text'] for tag in week_set) #ndiary_classificationt(day['text'])
        day['dairy'] = contains_word
        new_data.append(day)
        # time.sleep(2)
    print('second check')
    for day in tqdm(new_data):
        if any(tag in day['text'] for tag in teg_set):
            day['dairy'] = False
    return new_data

def prep_data(json_file: str):
    json_path = Path(json_file)

    with open(json_path, 'r') as file:
        data = json.load(file)

    prep_data = diary_classifaer(data)
    out_path = Path(json_path.parent, json_path.stem + '_prep.json')

    with open(out_path, "w", encoding="utf-8") as file:
        json.dump(prep_data, file, ensure_ascii=False, indent=4)   

    print(f'prep data saved in {out_path}')


if __name__=="__main__":
    Fire(prep_data)


