"""
class rule
"""

class Rule:
    def __init__(self, normal, anomaly, regex=None, kindp=0.5):
        """
        :param type: lfi
        :param msg: ../
        :param probability: 0.04
        :param regex:
        """
        self.kindp = kindp
        self.normal = normal
        self.anomaly = anomaly
        self.regex = regex

    def conditionp(self):
        return 1/(1+(self.normal*(1-self.kindp))/(self.anomaly*self.kindp))




