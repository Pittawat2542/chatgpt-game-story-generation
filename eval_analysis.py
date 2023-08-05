import os
import json
import time
import uuid
import chatgpt_evaluation as eval
import random
import pandas as pd
import prompt_runner as runner
from pathlib import Path

EVAL_RESULT_FILE_PATH_ENDINGS = Path(__file__).parent / "data/eval_results_endings.json"
EVAL_RESULT_FILE_PATH_NO_ENDINGS = Path(__file__).parent / "data/eval_results_no_endings.json"
SUMMARY_FILE_PATH = Path(__file__).parent / "data/summary.csv"

def summarize():
    data = []
    with open(EVAL_RESULT_FILE_PATH_ENDINGS, 'r') as results_file:
        results = json.load(results_file)
        for idx, res in enumerate(results['evaluation_results']):
            data.append([(idx+1), res['id'], res['story_type'], get_evaluation(res['evaluation_ending_type'])])
    
    with open(EVAL_RESULT_FILE_PATH_NO_ENDINGS, 'r') as results_file:
        results = json.load(results_file)
        for idx, res in enumerate(results['evaluation_results']):
            data.append([(idx+1), res['id'], res['story_type'], get_evaluation(res['evaluation_ending_type'])])       

    df = pd.DataFrame(data, columns = ["n", "id", "story_type", "evaluation"])
    df.to_csv(SUMMARY_FILE_PATH, index = False)
    
def get_evaluation(evalString):
    if "positive" in evalString:
        return "positive"
    elif "negative" in evalString:
        return "negative"
    elif "neutral" in evalString:
        return "neutral"
    else:
        return "NA"
    
if __name__ == '__main__':
    summarize()