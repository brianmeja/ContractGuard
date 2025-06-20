# Risk keywords and phrases for clause risk detection

HIGH_RISK_KEYWORDS = [
    'indemnify', 'hold harmless', 'unlimited liability', 'penalty', 'liquidated damages',
    'termination without cause', 'exclusive remedy', 'waiver of subrogation',
    'non-compete', 'non-solicitation', 'automatic renewal', 'one-sided',
    'irrevocable', 'perpetual', 'unilateral', 'forfeit', 'forfeiture',
    'no liability', 'sole discretion', 'without notice', 'as is', 'no warranty',
]

MEDIUM_RISK_KEYWORDS = [
    'limitation of liability', 'cap on damages', 'notice period', 'assignment',
    'governing law', 'jurisdiction', 'arbitration', 'dispute resolution',
    'intellectual property', 'ownership', 'confidentiality', 'force majeure',
    'payment terms', 'late fee', 'interest', 'termination for convenience',
]

LOW_RISK_KEYWORDS = [
    'term', 'renewal', 'scope of work', 'definitions', 'entire agreement',
    'severability', 'counterparts', 'notices', 'amendment', 'signatures',
] 