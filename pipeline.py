import json
import os
from typing import Callable
import time
import random
import re
from pathlib import Path
# from translation import ru2eng
from summarisation import get_summary
from tqdm import tqdm


device = 'cpu'


def preprocess_json_objects(
    input_file: str, 
    output_path: str, 
    preprocess_function: Callable[[dict], dict], 
    batch_size: int, 
    log_file: str = "./data/prep_posts/progress_log.json"
):
    """
    Iteratively preprocess JSON objects in batches and save to a file.

    Args:
        input_file (str): Path to the input JSON file containing a list of objects.
        output_file (str): Path to the output JSON file to save processed objects.
        preprocess_function (Callable[[dict], dict]): Function to preprocess each JSON object.
        batch_size (int): Number of objects to process in one batch.
        log_file (str): Path to the log file to track progress. Defaults to 'progress_log.json'.
    """
    # Load progress log
    if os.path.exists(log_file):
        with open(log_file, "r", encoding="utf-8") as log:
            progress = json.load(log)
    else:
        progress = {"processed": 0}

    start_index = progress["processed"]

    # Read input JSON file
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Determine the batch to process
    end_index = min(start_index + batch_size, len(data))
    batch = data[start_index:end_index]

    # Preprocess the batch
    processed_batch = [preprocess_function(obj) for obj in tqdm(batch)]


    # Append processed data to the output file
    input_name = Path(input_file).stem
    output_file = Path(output_path, f"{input_name}_diary_{end_index}.json")

    if os.path.exists(output_file):
        with open(output_file, "r", encoding="utf-8") as f:
            existing_data = json.load(f)
    else:
        existing_data = []

    existing_data.extend(processed_batch)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(existing_data, f, indent=4, ensure_ascii=False)

    # Update progress log
    progress["processed"] = end_index
    with open(log_file, "w", encoding="utf-8") as log:
        json.dump(progress, log, indent=4, ensure_ascii=False)

    print(f"Processed objects from index {start_index} to {end_index - 1} from {input_file}.")

# Example preprocess function
def sample_preprocess_function(obj):
    if obj["dairy"] == True:
        time.sleep(random.randint(2, 4))
        print(obj['text'])
        exercises = get_summary(obj['text'])
        obj["exercises"] = exercises
        obj["processed"] = True
    else:
        obj["processed"] = True
    return obj



if __name__=="__main__":
    preprocess_json_objects(
        input_file="/mnt/workout_analisys/data/posts_2024_prep.json",
        output_path="/mnt/workout_analisys/data/prep_posts",
        preprocess_function=sample_preprocess_function,
        batch_size=100
    )
