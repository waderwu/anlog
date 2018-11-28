import re
import os


class Attack:
    def __init__(self):
        """
        :param rules: rule list
        """

        self.rules = {}
        self.loadRules()

    def loadRules(self):
        ruleDir = os.path.join(os.path.split(os.path.realpath(__file__))[0], "rules")
        for filename in os.listdir(ruleDir):
            if not filename.endswith(".py") or filename.startswith("_"):
                continue
            ruleName = os.path.splitext(filename)[0]
            rule = __import__("log.plugin.rules." + ruleName, fromlist=[ruleName])
            self.rules[ruleName] = rule.rules

    def is_attack(self, log):

        for kind in self.rules:
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