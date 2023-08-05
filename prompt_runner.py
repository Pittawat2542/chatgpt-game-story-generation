import os
import openai
import time
import random
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = 'gpt-3.5-turbo'

openai.api_key = API_KEY

def run_prompt(prompt, temperature = -1):
    sleep_t = random.randint(3, 7)
    print(f"(zzz) now sleeping for {sleep_t}s to refresh OpenAI rate limit")
    time.sleep(sleep_t)

    result = ""
    try:
        messages = [ {"role": "user", "content": prompt}]

        if temperature < 0:
            print("running prompt with temperature: default")            
            response = openai.ChatCompletion.create(model = MODEL, messages = [{"role": "user", "content": prompt}])
            result = response.choices[0].message.content
        else:
            print(f"running prompt with temperature: {temperature}")
            response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}])
            openai.ChatCompletion.create(model = MODEL, messages = [{"role": "user", "content": prompt}], temperature = temperature)
            result = response.choices[0].message.content
    except openai.error.APIError as e:
        #Handle API error here, e.g. retry or log
        print(f"OpenAI API returned an API Error: {e}")
        result = ""
        pass
    except openai.error.APIConnectionError as e:
        #Handle connection error here
        print(f"Failed to connect to OpenAI API: {e}")
        result = ""
        pass
    except openai.error.RateLimitError as e:
        #Handle rate limit error (we recommend using exponential backoff)
        print(f"OpenAI API request exceeded rate limit: {e}")
        result = ""
        pass
    except openai.error.InvalidRequestError as e:
        #Handle invalid request, e.g. message is too long
        print(f"OpenAI API invalid request: {e}")
        result = ""
        pass
    except:
        print("something else is wrong")
        result = ""
        pass
    return result