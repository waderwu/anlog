from ._rule import Rule
import sys
sys.dont_write_bytecode = True

rules = [
    Rule(0.001, 0.05, r'\<\?php|\<\?'),
    Rule(0.001, 0.05, r'phpinfo|show_source|hightfile|file_get_contents|file_put_contents|var_dump')
]
