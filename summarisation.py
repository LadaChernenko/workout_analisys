import torch
import requests
import json
import re
from openai import OpenAI
from constants import OPENROUTER_API_KEY

 
# {"Приседания": 100, "Болгарские приседания": 100, "Подъемы на носки": 300, "Выпрыгивания": 200}
 
# {"Отжимания на брусьях": 100, "Отжимания от упоров": 100}
promt = """
Count the number of repetitions of each exercise.
Учитывай информацию что Л-лесенка (или /\ лесенка) значит упражнение делается с минимального значения до максимального и обратно.
А 30-минутки, 60-минутки и т.д. значит что каждую минуту новый подход. 
Не пиши рассчёты.
Выведи итоговую информацию в виде словаря как в примерах:
```
{"Приседания": 100, "Болгарские приседания": 100, "Подъемы на носки": 300, "Выпрыгивания": 200},
{"Боковые подъемы ног": 150, "Боковые скручивания в висе с согнутыми ногами": 100, "Додо": 400}
{"Подтягивания": 50, "Выходы силой": 100, "Отжимания": 10
}
```
"""
text = "Силы есть, настрой есть... но повторения не идут - бывает)\nВыходы совсем со скрипом пошли, о прошлой 10-ке даже смысла думать нет. Поэтому плавный вход в тренировочный процесс после болезни ну и старт нового тренировочного года.\n\nПонедельник - выходы, подъемы в передний вис, подтягивания \"Австралийский тюлень\" (90 минут)\n\n⁣⁣1. Подтягивания + отжимания от низкой перекладины. 5 подходов (5+10) повторений. Отдых 30 сек \n⁣⁣2. Выходы силой \"Л-лесенка от 1 до 5 с шагом 1\": 1-2-3-4-5+4+3+2+1. Отдых 1 мин.\n⁣⁣3. Выходы силой. 5 подходов на техничный максимум (8-5-5-5-5). Отдых 2 мин.\n⁣4. Спуск из вертикального положения в вис. 5 подходов по 5 повторений. Отдых 2 мин.\n5. Подъемы в передний вис. 5 подходов по 10 повторений. С добивками. Отдых 2 мин.\n6. Подтягивания \"Австралийский тюлень\" на заднюю дельту. 5 подходов на техничный максимум. Отдых 2 мин.\n\nОтдых между упражнениями - 3 минуты."

def parse_to_dict(text):
    try:
        # Clean up common issues (e.g., trailing commas)
        cleaned_text = text.strip() #.replace("\n", "").replace(",}", "}")
        # Convert to a dictionary
        return json.loads(cleaned_text)
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON: {e}")
        return None
    
def get_summary(text: str) -> dict:
  client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
  )

  completion = client.chat.completions.create(

  model="google/gemini-2.0-flash-exp:free",
  #  temperature=1,
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": promt
            },
            {
              "type": "text",
              "text": text
            }
          ]
        }
      ]
  )

  # print(completion.choices[0].message.content)
  try:
    out_text = completion.choices[0].message.content
    print(out_text)
    results = parse_to_dict(out_text)
  except Exception as e:
    print(f"Failed: {e}")
    results = None

  return results


if __name__=="__main__":
    print(get_summary(text))

