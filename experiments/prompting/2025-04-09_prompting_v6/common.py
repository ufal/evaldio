def get_true_level(filename, for_prompt=False):
    if not for_prompt and 'A2_older' in filename:
        return 'A2_older'
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

def model_name(model):
    for model_str in ["llama3", "deepseek"]:
        if model_str in model:
            return model_str
