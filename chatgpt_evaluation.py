import os
import json
from pathlib import Path

import openai
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = API_KEY

EVALUATION_MODEL = 'gpt-3.5-turbo'

INPUT_FILE_PATH = Path('data/results.json')
RESULT_FILE_PATH = Path('data/evaluation_results.json')


def main():
    with open(INPUT_FILE_PATH, 'r') as exported_results_file:
        stories = json.load(exported_results_file)

    for story in stories['responses']:
        prompt = f"""Please identify the type of ending in this story. Please make sure to format your output as a code block using triple backticks (```json and ```).

Story:
{story}

Output format:
```json
{{
    "ending": "positive", "negative", or "neutral"
}}
```"""

        chat_completion = openai.ChatCompletion.create(model=EVALUATION_MODEL,
                                                       messages=[{"role": "user", "content": prompt}],
                                                       temperature=0)

        response = chat_completion.choices[0].message.content
        ending_type = response.split('```json')[1].split('```')[0]

        if not os.path.exists(RESULT_FILE_PATH):
            with open(RESULT_FILE_PATH, 'w') as eval_result_file:
                eval_result_file.write('{"evaluation_results": []}')

        with open(RESULT_FILE_PATH, 'r+') as eval_result_file:
            result = json.load(eval_result_file)

            result['evaluation_results'].append(
                {'id': story['id'], 'evaluation_ending_type': ending_type})

            eval_result_file.seek(0)
            eval_result_file.write(json.dumps(result, indent=4))


if __name__ == '__main__':
    main()
