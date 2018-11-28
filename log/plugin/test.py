from attack import Attack
import json
p = Attack()

# print(p.rules)

log = '{"file":{"hh":"select from union select"}}'
log = json.loads(log)
print(log['file']['hh'])
# print(p.is_attack())

