#!/usr/bin/env python3
 
import os
import argparse
import inspect
import json
import logging
import random
import sys

from pydantic import BaseModel
from ollama import Client

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
commondir = os.path.join(parentdir, "2025-04-09_prompting_v6")
sys.path.insert(0, commondir)

from common import get_true_level, model_name

API_KEY = os.environ.get('AI_UFAL_TOKEN')

class TraitAssessment(BaseModel):
    score: float
    justification: str
    examples: list[str]

class ExerciseAssessment(BaseModel):
    task_fulfillment: TraitAssessment
    interaction: TraitAssessment
    lexical_resource: TraitAssessment
    grammatical_accuracy: TraitAssessment

class LLMOutput(BaseModel):
    exercises: list[ExerciseAssessment]

def instruct_model_api(model, model_args, prompt):
    API_URL = f"https://ai.ufal.mff.cuni.cz/ollama"
    client = Client(host=API_URL, headers={"Authorization": f"Bearer {API_KEY}"})

    messages = [{"role": "user", "content": prompt}]
    format = LLMOutput.model_json_schema()    
    data = {"model": model, "messages": messages, "stream": True, "format": format, "options": model_args}

    stream = client.chat(**data)
    
    try:
        output_json = ""
        last_chunk = None
        for i, chunk in enumerate(stream):
            if chunk["message"]["role"] == "assistant":
                output_json += chunk["message"]["content"]
            last_chunk = chunk
            #if i % 100 == 0:
            #    logging.debug(f"Output so far: {output_json}")
        logging.debug(f"API response metadata: {last_chunk}")
        llm_output = LLMOutput.model_validate(json.loads(output_json))
        return llm_output
    except Exception as e:
        logging.error(f"Error processing API response: {e}")

def average_trait_scores(llm_output):
    # Calculate the average scores for each trait across all exercises
    num_exercises = len(llm_output.exercises)
    avg_scores = {
        "task_fulfillment": 0,
        "interaction": 0,
        "lexical_resource": 0,
        "grammatical_accuracy": 0,
    }

    for exercise in llm_output.exercises:
        avg_scores["task_fulfillment"] += exercise.task_fulfillment.score
        avg_scores["interaction"] += exercise.interaction.score
        avg_scores["lexical_resource"] += exercise.lexical_resource.score
        avg_scores["grammatical_accuracy"] += exercise.grammatical_accuracy.score

    if num_exercises > 0:
        for trait in avg_scores:
            avg_scores[trait] /= num_exercises

    return avg_scores

def calculate_holistic_score(llm_output):
    # Calculate the holistic score based on the scores of the exercises
    total_score = 0
    num_exercises = len(llm_output.exercises)

    if num_exercises == 0:
        return 0.0
    
    for exercise in llm_output.exercises:
        total_score += (exercise.task_fulfillment.score + exercise.interaction.score +
                        exercise.lexical_resource.score + exercise.grammatical_accuracy.score) / 4
    
    holistic_score = total_score / num_exercises
    return holistic_score

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

    parser.add_argument("--json-out", "-o", help="Path to save the outputs of the LLM", type=str)
    parser.add_argument("--dry-run", "-d", help="If set, the script will not run the LLM, but only collect all results", action="store_true")

    parser.add_argument("exam_transcript_path", help="path to the exam transcript", type=str)
    args = parser.parse_args()
    # fmt: on
    return args

def main():
 
    args = parse_args()

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    
    exam_transcript_path = args.exam_transcript_path
    logging.info(f"Processing transcript: {exam_transcript_path}")
    transcript = open(exam_transcript_path).read().strip()
    exam_transcript_file = os.path.basename(exam_transcript_path)
    true_level = get_true_level(exam_transcript_path, for_prompt=False)
    true_level_for_prompt = get_true_level(exam_transcript_path, for_prompt=True)

    prompt = f"""
You are an expert evaluator of spoken Czech proficiency, using the Common European Framework of Reference for Languages (CEFR). Assess the performance of a candidate (CAND_1) in an oral {true_level_for_prompt}-level Czech exam based on the provided transcript. The exam is divided into multiple exercises. Each exercise must be evaluated separately.

For each exercise, evaluate the candidate on the following four traits: 
 * Task Fulfillment: to what extent does the candidate accomplish the communicative goal of the exercise?
 * Interaction: how well does the candidate engage in interaction with the examiner (EXAM_*)?
 * Lexical Resource: does the candidate use appropriate and varied vocabulary for the level?
 * Grammatical Accuracy: is the candidate's use of grammar appropriate and accurate for the level?

For each trait, do the following:
 * Assign a score between 0 and 100.
 * Provide a brief explanation justifying the score, with examples from the transcript.

This is the transcript of the oral exam:

{transcript}

Your answer:
"""

    logging.debug(f"<PROMPT>{prompt}</PROMPT>")

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

        output = None

        if args.json_out:
            json_out_path = f"{args.json_out}.model={model_name(args.model)}.seed={seed}.json"
            if os.path.exists(json_out_path):
                logging.info(f"Output already exists, loading: {json_out_path}")
                try:
                    with open(json_out_path, "r") as f:
                        output = LLMOutput.model_validate(json.load(f))
                except json.JSONDecodeError as e:
                    output = None
    
        if output is None and not args.dry_run:
            #continue
            output = instruct_model_api(
                model=args.model, model_args=model_args, prompt=prompt
            )

            if args.json_out:
                json_out_path = f"{args.json_out}.model={model_name(args.model)}.seed={seed}.json"
                with open(json_out_path, "w") as f:
                    json.dump(output.model_dump(), f, indent=2)
                logging.info(f"Output saved to {json_out_path}")

        if output:
            print("\t".join([
                true_level,
                exam_transcript_file,
                str(seed),
                f"{calculate_holistic_score(output):.2f}",
                f"{average_trait_scores(output)['task_fulfillment']:.2f}",
                f"{average_trait_scores(output)['interaction']:.2f}",
                f"{average_trait_scores(output)['lexical_resource']:.2f}",
                f"{average_trait_scores(output)['grammatical_accuracy']:.2f}",
            ]))

if __name__ == "__main__":
    main()
