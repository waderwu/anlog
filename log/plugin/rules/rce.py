from ._rule import Rule

rules = [
    Rule(0.001, 0.05, r'\|'),
    Rule(0.001, 0.05, r'`|;|&'),
    Rule(0.001, 0.05, r'system|eval|exec'),
    Rule(0.001, 0.05, r'cat.*flag'),
    Rule(0.001, 0.05, r'\/bin\/|base64 -d'),
    Rule(0.001, 0.05, r'curl|wget|phpinfo\(\)')
]
