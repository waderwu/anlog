from ._rule import Rule
import sys
sys.dont_write_bytecode = True

rules = [
    Rule(0.001, 0.05, r"'"),
    Rule(0.001, 0.05, r'"'),
    Rule(0.001, 0.05, r'#|--'),
    Rule(0.001, 0.05, r'select|and|or|update')
]
