# Experiment 2024-04-09

## Description

The most basic experiment of prompting LLMs.
Given the transcript of a dialog between the examiner and the candidate and the CEFR level of the exam, the LLM is prompted to estimate whether the candidate passes the oral exam.
It should only output True=pass or False=fail.

## Models

* `llama3.3.latest`
* `deepseek-r1:70b`

## Variations

* (2024-04-23) LLM is prompted 3-times using different random seeds: 42, 1986, 2025
