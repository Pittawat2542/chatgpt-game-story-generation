import os
import json
import time
import uuid
import chatgpt_evaluation as eval
import random
import prompt_runner as runner
from pathlib import Path

RESULT_FILE_PATH_ENDINGS = Path(__file__).parent / "data/results_endings.json"
RESULT_FILE_PATH_NO_ENDINGS = Path(__file__).parent / "data/results_no_endings.json"
EVAL_RESULT_FILE_PATH_ENDINGS = Path(__file__).parent / "data/eval_results_endings.json"
EVAL_RESULT_FILE_PATH_NO_ENDINGS = Path(__file__).parent / "data/eval_results_no_endings.json"
TIMES = 100

def data_generation():
    generate_with_endings()
    generate_no_endings()
    eval.evaluate(RESULT_FILE_PATH_ENDINGS, EVAL_RESULT_FILE_PATH_ENDINGS)
    eval.evaluate(RESULT_FILE_PATH_NO_ENDINGS, EVAL_RESULT_FILE_PATH_NO_ENDINGS)

def generate_with_endings():
    remainders = { "positive": TIMES, "negative": TIMES, "neutral": TIMES }    
    try:
        with open(RESULT_FILE_PATH_ENDINGS, 'r') as exported_results_file:
            stories = json.load(exported_results_file)
            for idx, res in enumerate(stories['responses']):
                remainders[res['ending_type']] = remainders[res['ending_type']] - 1
    except Exception as error:
        print(str(error))    
    
    print(remainders)

    endings = ["positive"] * remainders["positive"] + ["negative"] * remainders["negative"] + ["neutral"] * remainders["neutral"]
    if len(endings) <= 0:
        print("already completed")
        return
    
    idx = 0
    while idx < len(endings):
    # for idx, ending in enumerate(endings):
        ending = endings[idx]
        prompt = f'''Please write a brief 300-word game story with a {ending} ending based on the following concepts.
    
Places:
- mountain
- city
- kingdom

Characters:
- civilians
- mages
- adventurers

Game genre: fantasy action RPG

Story:'''

        response = runner.run_prompt(prompt = prompt)
        if len(response) <= 0:
            continue

        if not os.path.exists(RESULT_FILE_PATH_ENDINGS):
            with open(RESULT_FILE_PATH_ENDINGS, 'w') as result_file:
                result_file.write('{"responses": []}')

        with open(RESULT_FILE_PATH_ENDINGS, 'r+') as result_file:
            result = json.load(result_file)
            result['responses'].append({'id': str(uuid.uuid4()), 'ending_type': ending, 'story': response})

            result_file.seek(0)
            result_file.write(json.dumps(result, indent=4))

        print('Round: ', idx + 1)
        idx = idx + 1

def generate_no_endings():    
    max_generation = TIMES

    try:
        with open(RESULT_FILE_PATH_NO_ENDINGS, 'r') as exported_results_file:
            stories = json.load(exported_results_file)
            max_generation = TIMES - len(stories['responses'])            
    except:
        max_generation = TIMES
        print("json not found")
    
    if max_generation <= 0:
        print("already completed")
        return

    idx = 0
    while idx < max_generation:
    # for idx in range(max_generation):
        prompt = f'''Please write a brief 300-word game story with an ending based on the following concepts.

Places:
- mountain
- city
- kingdom

Characters:
- civilians
- mages
- adventurers

Game genre: fantasy action RPG

Story:'''

        response = runner.run_prompt(prompt = prompt)
        if len(response) <= 0:
            continue

        if not os.path.exists(RESULT_FILE_PATH_NO_ENDINGS):
            with open(RESULT_FILE_PATH_NO_ENDINGS, 'w') as result_file:
                result_file.write('{"responses": []}')

        with open(RESULT_FILE_PATH_NO_ENDINGS, 'r+') as result_file:
            result = json.load(result_file)
            result['responses'].append({'id': str(uuid.uuid4()),'ending_type': "NA", 'story': response})

            result_file.seek(0)
            result_file.write(json.dumps(result, indent=4))

        print('Round: ', idx + 1)
        idx = idx + 1

def main():
    data_generation()

if __name__ == '__main__':
    main()