

def score_grade(score):
    if score >= 90:
        return "A"
    elif score <= 89 and score >= 70:
        return "B"
    elif score <= 69 and score >= 55:
        return "C"
    else: 
        return "D"