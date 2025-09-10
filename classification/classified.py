class Classified:


    def __init__(self, len_text, num_hostile_words, num_less_hostile_words):
        """ gets the following details about text: its length, how many hostile words appear in it,
            how many less hostile words appear in it.
                responsible for giving a risk rating according to these details. """
        self.len_text = len_text
        # the value of hostile_words two of num_less_hostile_words
        self.num_hostile_words = num_hostile_words + (num_less_hostile_words / 2)
        self.risk_percent = self.risk_percent_calculation()


    def risk_percent_calculation(self):
        """ calculates risk percent - the formula: num of hostile_words divide by one-fifth the length of the text,
            ranges from zero to one max """
        risk_percent = self.num_hostile_words / (self.len_text / 5)
        if risk_percent > 1:
            risk_percent = 1.0
        return risk_percent


    def threshold_determination(self):
        """ threshold determination of incrimination - the formula: risk_percent greater than 0.5. """
        if self.risk_percent > 0.5:
            return True
        else:
            return False


    def danger_level(self):
        """ calculates danger level - the formula: "high" for 1 risk_percent,
            "medium" if risk_percent greater than 0.5, greater than "none" . """
        if self.risk_percent >= 1.0:
            return "high"
        elif self.risk_percent > 0.5:
            return "medium"
        else:
            return "none"


    def full_risk(self):
        """ full risk - centralizes all calculations of the Classified and return them as dict. """
        full_risk = {"bds_percent": self.risk_percent,
                    "is_bds": self.threshold_determination(),
                    "bds_threat_level": self.danger_level()}
        return full_risk