from Firefox.FirefoxRandomnessPredictor import FirefoxRandomnessPredictor

"""
All numbers generated in Firefox via devtools console.
"""

ORIGINAL_SEQUENCE = [
    0.6001352587932771,
    0.3250225488841686,
    0.2681294834228445,
    0.7019064719602867,
    0.5599697355474599,
]
ORIGINAL_EXPECTED = [
    0.5837681703073178,
    0.18128470048076706,
    0.2553924400843819,
    0.2388525040412779,
    0.9099321641840764,
]

sequence = [
    0.1321263101773572,
    0.03366887439746058,
    0.032596957696410134,
    0.9986575482138969,
    0.8479779907956815,
]

expected = [
    0.13963871472821332,
    0.25068024611907636,
    0.6656237481612675,
    0.7381091878692425,
    0.8709382509549467,
    0.49171337524788294,
    0.6991749430716799,
    0.9530887478758369,
    0.781511163650037,
    0.699311162730038,
]


def testFirefox():
    isOverallSuccess = True
    pred = FirefoxRandomnessPredictor(sequence)
    for i in range(len(expected)):
        prediction = pred.predict_next()
        correct = prediction == expected[i]
        if correct == False:
            isOverallSuccess = False
        print(
            f"correct? {correct}\t|\tpredicted={prediction}\t|\texpected={expected[i]}"
        )
    return isOverallSuccess


if __name__ == "__main__":
    testFirefox()
