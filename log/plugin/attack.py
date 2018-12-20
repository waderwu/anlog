import re
import os
import sys
import importlib
sys.dont_write_bytecode = True

class Attack:
    def __init__(self):
        """
        :param rules: rule list
        """
        self.rules = {}
        self.modules = []
        ruleDir = os.path.join(os.path.split(os.path.realpath(__file__))[0], "rules")
        for filename in os.listdir(ruleDir):
            if not filename.endswith(".py") or filename.startswith("_"):
                continue
            ruleName = os.path.splitext(filename)[0]
            rules = __import__("log.plugin.rules." + ruleName, fromlist=[ruleName])
            self.modules.append(rules)


    def loadRules(self):
        self.rules = {}
        ruleDir = os.path.join(os.path.split(os.path.realpath(__file__))[0], "rules")
        for filename in os.listdir(ruleDir):
            if not filename.endswith(".py") or filename.startswith("_"):
                continue
            ruleName = os.path.splitext(filename)[0]
            module_name = "log.plugin.rules." + ruleName
            rule = __import__(module_name, fromlist=[ruleName])
            # print("rule", rule)
            # print("modules", sys.modules)
            # print(module_name in sys.modules)
            if module_name in sys.modules:
                print("reload")
                rule = importlib.reload(rule)
            print("ggg: %d"%len(rule.rules))
            self.rules[ruleName] = rule.rules

    def is_attack(self, log):
        self.loadRules()
        # print(self.rules)
        for kind in self.rules:
            # print(len(self.rules[kind]))
            product1 = 1.0
            product2 = 1.0
            for rule in self.rules[kind]:
                if re.search(rule.regex, log):
                    product1 *= rule.conditionp()
                    product2 *= (1-rule.conditionp())

            p = 1/(1+product2/product1)

            if p > 0.95:
                return kind
        return None