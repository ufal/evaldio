# Experiment 2024-04-23

## Description

Extended version of the most basic experiment of prompting LLMs.
Given the transcript of a dialog between the examiner and the candidate, the CEFR level of the exam and the score threshold to pass the exam for the particular level, the LLM is prompted to estimate the score the candidate would earn for the exam dialog.
The score threshold is normalized to be between 0 and 100. The score estimated by the LLM is expected to be in the same range.

## Models

* `llama3.3.latest`
* `deepseek-r1:70b`

## Variations

* (2024-04-23) LLM is prompted 3-times using different random seeds: 42, 1986, 2025
