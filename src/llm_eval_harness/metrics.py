import re
from collections import Counter

def normalize(text: str) -> str:
    return " ".join(re.findall(r"[a-z0-9]+", text.lower()))

def exact_match(prediction: str, reference: str) -> float:
    return float(normalize(prediction) == normalize(reference))

def token_f1(prediction: str, reference: str) -> float:
    pred = normalize(prediction).split()
    ref = normalize(reference).split()
    if not pred or not ref:
        return 0.0
    overlap = sum((Counter(pred) & Counter(ref)).values())
    if overlap == 0:
        return 0.0
    precision = overlap / len(pred)
    recall = overlap / len(ref)
    return 2 * precision * recall / (precision + recall)
