from ._rule import Rule
rules = [
    Rule(0.001, 0.05, r"'"),
    Rule(0.001, 0.05, r'"'),
    Rule(0.001, 0.05, r'#|--'),
    Rule(0.001, 0.05, r'select|and|or|update')
]
