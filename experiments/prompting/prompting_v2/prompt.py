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
            prompt = """
        You are an expert evaluator of spoken Czech proficiency according to the Common European Framework of Reference for Languages (CEFR). Based on the automatically generated transcript and provided level of the oral exam conducted by the examiners EXAM_*, decide whether the candidate passed the exam. If the candidate fails the exam, estimate the CEFR level of the candidate CAND_1.
        Provide your response only as a JSON object with keys "passed" with a boolean value indicating whether the candidate passed the exam for the given level and "level" with estimated level value of the CEFR level (A1, A2, B1, B2, C1). Bear in mind that the candidate can only pass the exam if the estimated level is equal or greater to the exam level. Only 5% of candidates fail the exam.

        The JSON object should look like this:
        {"level": "<level>", "passed": <passed>}
        Replace <level> with your estimated CEFR level. Replace <passed> with either true or false.
        Do not include any text before or after the JSON object under any circumstances. Do no offer any explanation or justification for your answer.

        This is the transcript of the oral exam for level """ + true_level + ":\n" + transcript + "\nYour answer: "
            

        
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

            f.write(f"{filename}\t{true_level}\t{output_text['passed']}\t{output_text['level']}\n")
            f.flush()