#!/usr/bin/env python3
 
import os
import argparse
import json
import logging
import random

from pydantic import BaseModel
import requests

API_KEY = os.environ.get('AI_UFAL_TOKEN')

class LLMOutput(BaseModel):
    passed: bool
 
def get_true_level(filename):
    if 'A1' in filename:
        return 'A1'
    if 'A2_older' in filename:
        return 'A2_older'
    if 'A2' in filename:
        return 'A2'
    if 'B1' in filename:
        return 'B1'
    if 'B2' in filename:
        return 'B2'
    if 'C1' in filename:
        return 'C1'
    assert False, f"Unknown level in filename {filename}"


def instruct_model_api(model, model_args, prompt):
    API_URL = f"https://ai.ufal.mff.cuni.cz/ollama/api/chat"
    messages = [{"role": "user", "content": prompt}]
    format = LLMOutput.model_json_schema()    
    data = {"model": model, "mode": "instruct", "messages": messages, "stream": False, "format": format, "options": model_args}

    response = requests.post(
        API_URL,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}",
        },
        json=data,
        verify=False,
    )
    try:
        output_json = json.loads(response.json()["message"]["content"])
        llm_output = LLMOutput.model_validate(output_json)
        return llm_output
    except:
        print(f"API error message: {response}")


def parse_args():
    # fmt: off
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", "-m", help="Model name", type=str, default="LLM3-AMD-MI210.llama3.3:latest")
    #parser.add_argument("--max_tokens", "-m", help="Maximum number of tokens to generate", type=int, default=300) 
    parser.add_argument("--seeds", "-r", help="Seeds for random number generator. If multiple, the same experiments will be run multiple times with different seeds.", type=int, nargs='+', default=[42])
    parser.add_argument("--temperature", "-t", help="Temperature parameter", type=float, default=1.0) 
    parser.add_argument("--top_p", "-p", help="Top-p sampling parameter", type=float, default=1.0) 
    parser.add_argument("--top_k", "-k", help="Top-k sampling parameter", type=int, default=0)
    #parser.add_argument("--num_beams", "-b", help="Number of beams for beam search", type=int, default=1)
    #parser.add_argument("--do_sample", "-s", help="Use sampling instead of greedy decoding", action="store_true")

    parser.add_argument("exam_transcript_path", help="path to the exam transcript", type=str)
    parser.add_argument("exam_labels_path", help="path to the JSON with labels for the given transcript", type=str)
    args = parser.parse_args()
    # fmt: on
    return args

def main():
 
    args = parse_args()

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    
    exam_transcript_path = args.exam_transcript_path
    logging.info(f"Processing transcript: {exam_transcript_path}")
    transcript = open(exam_transcript_path).read().strip()
    exam_transcript_file = os.path.basename(exam_transcript_path)
    true_level = get_true_level(exam_transcript_file)

    prompt = f"""
You are an expert evaluator of spoken Czech proficiency according to the Common European Framework of Reference for Languages (CEFR). Based on the automatically generated transcript of an oral exam conducted by the examiners EXAM_*, estimate whether the candidate CAND_1 passes or fails the exam.

This is the transcript of the oral exam for proficiency at the {true_level} level:

{transcript}

Your answer:
"""

    logging.info(f"<PROMPT>{prompt}</PROMPT>")

    label_json = json.load(open(args.exam_labels_path))

    for i, seed in enumerate(args.seeds, 1):

        logging.info(f"Run {i}: seed={seed}")

        model_args = {
    #        "max_tokens": args.max_tokens,
    #        "num_beams": args.num_beams,
            "temperature": args.temperature,
            "top_p": args.top_p,
            "top_k": args.top_k,
    #        "do_sample": args.do_sample,
            "seed": seed,
        }

        output = instruct_model_api(
            model=args.model, model_args=model_args, prompt=prompt
        )

        print("\t".join([
            true_level,
            exam_transcript_file,
            str(label_json["avg"]["result"]),
            str(seed),
            str(output.passed),
        ]))

if __name__ == "__main__":
    main()