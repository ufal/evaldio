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
You are an expert evaluator of spoken Czech proficiency according to the Common European Framework of Reference for Languages (CEFR). Based on the automatically generated transcript of an oral exam conducted by the examiners EXAM_*, estimate the CEFR level of the candidate CAND_1.
Provide your response only as a JSON object with a single key "level" and a value of the CEFR level (A1, A2, B1, B2, C1, C2) and nothing else.

Definitions of CEFR levels:
A1 level definition:	
Can understand and use familiar everyday expressions and very basic phrases aimed at the satisfaction of needs of a concrete type.
Can introduce themselves to others and can ask and answer questions about personal details such as where they live, people they know and things they have.
Can interact in a simple way provided the other person talks slowly and clearly and is prepared to help.

A2 level definition:	
Can understand sentences and frequently used expressions related to areas of most immediate relevance (e.g. very basic personal and family information, shopping, local geography, employment).
Can communicate in simple and routine tasks requiring a simple and direct exchange of information on familiar and routine matters.
Can describe in simple terms aspects of their background, immediate environment and matters in areas of immediate need.

B1 level definition:	
Can understand the main points of clear standard input on familiar matters regularly encountered in work, school, leisure, etc.
Can deal with most situations likely to arise while travelling in an area where the language is spoken.
Can produce simple connected text on topics that are familiar or of personal interest.
Can describe experiences and events, dreams, hopes and ambitions and briefly give reasons and explanations for opinions and plans.
B2 level definition:
Can understand the main ideas of complex text on both concrete and abstract topics, including technical discussions in their field of specialisation.
Can interact with a degree of fluency and spontaneity that makes regular interaction with native speakers quite possible without strain for either party.
Can produce clear, detailed text on a wide range of subjects and explain a viewpoint on a topical issue giving the advantages and disadvantages of various options.

Proficient user	C1 level definition:
Can understand a wide range of demanding, longer clauses and recognise implicit meaning.
Can express ideas fluently and spontaneously without much obvious searching for expressions.
Can use language flexibly and effectively for social, academic and professional purposes.
Can produce clear, well-structured, detailed text on complex subjects, showing controlled use of organisational patterns, connectors and cohesive devices.

C2 level definition:
Can understand with ease virtually everything heard or read.
Can summarise information from different spoken and written sources, reconstructing arguments and accounts in a coherent presentation.
Can express themselves spontaneously, very fluently and precisely, differentiating finer shades of meaning even in the most complex situations.

The JSON object should look like this:
{"level": "<level>"}
Replace <level> with your estimated CEFR level.
Do not include any text before or after the JSON object under any circumstances. Do no offer any explanation or justification for your answer.

This is the transcript of the oral exam:

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

            f.write(f"{filename}\t{true_level}\t{output_text['level']}\n")
            f.flush()