import json

# Raw string input
input_file = 'data/prep_posts/posts_2024_prep_diary_200.json'
with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

for obj in data:       
    if (obj['dairy'] == True) and (obj['exercises'] != None):
        text = obj['exercises']

        # Step 1: Extract the JSON part
        start_index = text.find('{')
        end_index = text.rfind('}')
        json_content = text[start_index:end_index + 1]

        # Step 2: Parse the JSON content
        parsed_dict = json.loads(json_content)

        # Output the dictionary
        print(parsed_dict)
        obj['exercises'] = parsed_dict

with open(input_file, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print("Updated data saved successfully.")