from ._rule import Rule
rules = [
    Rule(0.001, 0.05, r'http://|https://'),
    Rule(0.001, 0.05, r'ftp://'),
    Rule(0.001, 0.05, r'file://'),
    Rule(0.001, 0.05, r'gopher://')
]