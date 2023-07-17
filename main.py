import os
import json
import time
import uuid
from pathlib import Path

import openai
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = API_KEY

RESULT_FILE_PATH = Path(__file__).parent / "data/results.json"


def data_generation():
    TIMES = 10
    endings = ["positive"] * TIMES + ["negative"] * TIMES + ["neutral"] * TIMES

    for idx, ending in enumerate(endings):
#         prompt = f'''Please write a brief 300-word game story with an ending based on the following concepts.
#
# Places:
# - mountain
# - city
# - kingdom
#
# Characters:
# - civilians
# - mages
# - adventurers
#
# Game genre: fantasy action RPG
#
# Story:'''

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

        chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                                       messages=[{"role": "user", "content": prompt}])

        response = chat_completion.choices[0].message.content

        if not os.path.exists(RESULT_FILE_PATH):
            with open(RESULT_FILE_PATH, 'w') as result_file:
                result_file.write('{"responses": []}')

        with open(RESULT_FILE_PATH, 'r+') as result_file:
            result = json.load(result_file)
            result['responses'].append({'id': str(uuid.uuid4()), 'ending_type': ending, 'story': response})

            result_file.seek(0)
            result_file.write(json.dumps(result, indent=4))

        print('Round: ', idx + 1)
        time.sleep(7)


def main():
    data_generation()


if __name__ == '__main__':
    main()
