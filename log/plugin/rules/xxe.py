from ._rule import Rule
rules = [
    Rule(0.001, 0.05, r'<!ENTITY'),
    Rule(0.001, 0.05, r'<!DOCTYPE')
]
