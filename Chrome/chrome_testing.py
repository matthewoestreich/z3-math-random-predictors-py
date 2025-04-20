from ChromeRandomnessPredictor import ChromeRandomnessPredictor

sequence = [
    0.11590966799438174,
    0.8827994404701779,
    0.931965836684493,
    0.053910018249548,
    0.10002302879586344,
]

expected = [
    0.4107857334881625,
    0.9678947364255936,
    0.5656948155949282,
    0.9616116961598181,
    0.5745843601953992,
]

pred = ChromeRandomnessPredictor(sequence)

for i in range(len(expected)):
    prediction = pred.predict_next()
    correct = prediction == expected[i]
    if correct == False:
        raise Exception(
            f"Incorrect prediction! Expect {expected[i]} but got {prediction}"
        )
    print(f"Correct? {correct}\t| Predicted={prediction}\t| Expected={expected[i]}")
