class Classified:

    def __init__(self, len_text, num_hostile_words, num_less_hostile_words):
        self.len_text = len_text
        self.num_hostile_words = num_hostile_words + (num_less_hostile_words // 2)


    def risk_percent_calculation(self):
        risk_percent = self.num_hostile_words / (self.len_text / 5)
        if risk_percent > 1:
            risk_percent = 1.0
        return risk_percent


    def threshold_determination(self, risk_percent):
        if risk_percent > 0.5:
            return True
        else:
            return False


    def danger_level(self, risk_percent):
        if risk_percent >= 1.0:
            return "high"
        elif risk_percent > 0.5:
            return "medium"
        else:
            return "none"


    def full_risk(self):
        risk_percent = self.risk_percent_calculation()
        full_risk = {"bds_percent": risk_percent,
                    "is_bds": self.threshold_determination(risk_percent),
                    "bds_threat_level": self.danger_level(risk_percent)}
        return full_risk



c = Classified(20, 2, 2)
print(c.risk_percent_calculation())