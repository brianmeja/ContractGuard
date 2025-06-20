import re
from typing import List, Dict
from .risk_keywords import HIGH_RISK_KEYWORDS, MEDIUM_RISK_KEYWORDS, LOW_RISK_KEYWORDS

RISK_LEVELS = {
    'High': HIGH_RISK_KEYWORDS,
    'Medium': MEDIUM_RISK_KEYWORDS,
    'Low': LOW_RISK_KEYWORDS,
}

RISK_COLORS = {
    'High': 'red',
    'Medium': 'orange',
    'Low': 'green',
    'None': 'gray',
}

def split_into_clauses(text: str) -> List[str]:
    # Simple split by sentence-ending punctuation, but keep context
    clauses = re.split(r'(?<=[.!?])\s+(?=[A-Z])', text)
    return [c.strip() for c in clauses if c.strip()]


def assess_clause_risk(clause: str) -> Dict:
    clause_lower = clause.lower()
    for risk, keywords in RISK_LEVELS.items():
        for kw in keywords:
            if kw in clause_lower:
                return {
                    'risk': risk,
                    'keyword': kw,
                    'color': RISK_COLORS[risk],
                }
    return {
        'risk': 'None',
        'keyword': None,
        'color': RISK_COLORS['None'],
    }


def analyze_contract(text: str) -> List[Dict]:
    clauses = split_into_clauses(text)
    results = []
    for clause in clauses:
        risk_info = assess_clause_risk(clause)
        results.append({
            'clause': clause,
            'risk': risk_info['risk'],
            'keyword': risk_info['keyword'],
            'color': risk_info['color'],
        })
    return results 