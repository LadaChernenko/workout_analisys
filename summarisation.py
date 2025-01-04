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
# text = "Вторник как вторник, без группировок - обычные отжимания на брусьях.\n\nВторник - отжимания на брусьях (90 минут)\n- Отжимания на брусьях. 10 подходов по 10 повторений. Отдых 30 сек.\n- Отдых 3 минуты.\n- Отжимания на брусьях. 10 подходов по 30 повторений с добивками. Отдых 2 мин.\n- Отдых 3 минуты.\n- Отжимания на брусьях. 10 подходов по 20 повторений. Отдых 2 мин.\n- Отдых 3 минуты.\n- Отжимания на брусьях. 10 подходов по 10 повторений. Отдых 1 мин."

def parse_to_dict(text):
    try:
        start_index = text.find('{')
        end_index = text.rfind('}')
        json_content = text[start_index:end_index + 1]

        parsed_dict = json.loads(json_content)
        return parsed_dict
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON: {e}")
        return text
    except json.decoder.JSONDecodeError as e:
        print(f"Failed to parse JSON: {e}")
        return text
    
def get_summary(text: str) -> dict:
  client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
  )

  completion = client.chat.completions.create(

  # model="google/gemini-2.0-flash-exp:free",
  model="deepseek/deepseek-chat",
  temperature=0.8,
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
    # results = out_text
    results = parse_to_dict(out_text)
  except Exception as e:
    print(f"Failed: {e}")
    results = None

  return results


# if __name__=="__main__":
#     print(get_summary(text))

