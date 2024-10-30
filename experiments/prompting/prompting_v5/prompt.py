#!/usr/bin/env python3
 
import os
import requests
import argparse
import json

import tqdm
 
API_KEY = "YOUR_API_KEY"
 
def instruct_model_api(model_args, prompt):
    API_URL = f"http://quest.ms.mff.cuni.cz/nlg/text-generation-api/v1/chat/completions"
    messages = [{"role": "user", "content": prompt}]
    data = {"mode": "instruct", "messages": messages, **model_args}
 
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
        output_text = response.json()["choices"][0]["message"]["content"]
        return output_text
    except:
        print(f"API error message: {response}")
 
 
if __name__ == "__main__":
    # fmt: off
    parser = argparse.ArgumentParser()
    parser.add_argument("--max_tokens", "-m", help="Maximum number of tokens to generate", type=int, default=300) 
    parser.add_argument("--seed", "-r", help="Seed for random number generator", type=int, default=42) 
    parser.add_argument("--temperature", "-t", help="Temperature parameter", type=float, default=1.0) 
    parser.add_argument("--top_p", "-p", help="Top-p sampling parameter", type=float, default=1.0) 
    parser.add_argument("--top_k", "-k", help="Top-k sampling parameter", type=int, default=0)
    parser.add_argument("--num_beams", "-b", help="Number of beams for beam search", type=int, default=1)
    parser.add_argument("--do_sample", "-s", help="Use sampling instead of greedy decoding", action="store_true")

    parser.add_argument("--exam_transcripts", "-e", help="paths to exam transcripts", type=str, required=True, nargs="+")
    args = parser.parse_args()
    # fmt: on
    
    with open("output.txt", "w") as f:
        exams = args.exam_transcripts
        import random
        random.shuffle(exams)
        for exam_transcript in tqdm.tqdm(exams):

            transcript = open(exam_transcript).read().strip()
            prompt = """
You are an expert evaluator of spoken Czech proficiency according to the Common European Framework of Reference for Languages (CEFR). Based on the automatically generated transcript of an oral exam conducted by the examiners (EXAM_*), estimate the CEFR level of the candidate (CAND_1). Additionally, explain the reasoning behind your decision and support it with examples from the exam. Bear in mind that ASR generates this transcript and contains a lot of recognition errors that are due to the ASR's poor robustness, and the errors are not due to the candidate's inability. In the explanation, try to assess how much of the errors made are due to ASR and how much is due to the candidate.

Provide your response in the following JSON format:

{"level": "<level>", "explanation": "<explanation>"}

Replace <level> with your estimated CEFR level and <explanation> with your explanation.

Do not include any text before or after the JSON object.

        """ + transcript + "\n\n Your answer:"
            
            filename = os.path.basename(exam_transcript)
            def get_true_level(filename):
                if 'A1' in filename:
                    return 'A1'
                if 'A2' in filename:
                    return 'A2'
                if 'B1' in filename:
                    return 'B1'
                if 'B2' in filename:
                    return 'B2'
                if 'C1' in filename:
                    return 'C1'
                assert False, f"Unknown level in filename {filename}"

            true_level = get_true_level(filename)
        
            model_args = {
                "max_tokens": args.max_tokens,
                "num_beams": args.num_beams,
                "temperature": args.temperature,
                "top_p": args.top_p,
                "top_k": args.top_k,
                "do_sample": args.do_sample,
                "seed": args.seed,
            }
        
            prompt += transcript
            output_text = instruct_model_api(
                model_args=model_args, prompt=prompt
            )
            output_text = output_text.strip()
            try:
                output_text = json.loads(output_text)
            except:
                with open("error.txt", "a") as e:
                    e.write(f"{filename}\t{true_level}\t{output_text}\n")
                    e.flush()
                    continue

            f.write(f"{filename}\t{json.dumps(output_text)}\n")
            f.flush()