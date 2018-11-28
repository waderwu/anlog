from ._rule import Rule
rules = [
    Rule(0.001, 0.05, r'../'),
    Rule(0.001, 0.05, r'php:|phar|zlib:'),
    Rule(0.001, 0.05, r'/root|/home|/etc/passwd|/flag')
]
