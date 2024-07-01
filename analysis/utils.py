from mosestokenizer import MosesTokenizer, MosesPunctuationNormalizer
import re

PUNCT_REPLACE = re.compile(r'[\.,\?!:]+')

punct_normalizer = MosesPunctuationNormalizer('cs')

def normalize_text(text, char_level=False):
    text = text.replace('\n', ' ')
    if text:
        text = punct_normalizer(text)
    text = text.replace('-', '')
    text = text.replace('*', '')
    text = text.replace('\'', '')
    text = re.sub(PUNCT_REPLACE, ' ', text)
    text = text.split()
    if char_level:
        return [t for t in ''.join(text).lower() if t.isalnum()]
    return [t.lower() for t in text if t.isalnum()]