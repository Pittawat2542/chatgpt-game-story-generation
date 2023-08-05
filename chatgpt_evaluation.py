import os
import json
import random
import time
import prompt_runner as runner
from pathlib import Path

def evaluate(input_file, result_file):
    input_file_path = Path(input_file)
    result_file_path = Path(result_file)

    with open(input_file_path, 'r') as exported_results_file:
        stories = json.load(exported_results_file)

    
    idx = 0
    # for story in stories['responses']:
    while idx < len(stories['responses']):
        story = stories['responses'][idx]
        prompt = f"""Please identify the type of ending in this story. Please make sure to format your output as a code block using triple backticks (```json and ```).

Story:
{story}

Output format:
```json
{{
    "ending": "positive", "negative", or "neutral"
}}
```"""        
        response = runner.run_prompt(prompt = prompt, temperature = 0)
        if len(response) <= 0:
            continue
        
        ending_type = ""
        try:
            ending_type = response.split('```json')[1].split('```')[0]
        except Exception as error:
            print(error)
            print(response)
            print("=========")
            ending_type = response

        if not os.path.exists(result_file_path):
            with open(result_file_path, 'w') as eval_result_file:
                eval_result_file.write('{"evaluation_results": []}')

        with open(result_file_path, 'r+') as eval_result_file:
            result = json.load(eval_result_file)

            result['evaluation_results'].append(
                {'id': story['id'], 'story_type': story['ending_type'], 'evaluation_ending_type': ending_type})

            eval_result_file.seek(0)
            eval_result_file.write(json.dumps(result, indent=4))

        idx = idx + 1

def main():
    evaluate(Path(__file__).parent / "data/results_endings.json", Path(__file__).parent / "data/eval_results_endings.json")
    evaluate(Path(__file__).parent / "data/results_no_endings.json", Path(__file__).parent / "data/eval_results_no_endings.json")

if __name__ == '__main__':
    main()
