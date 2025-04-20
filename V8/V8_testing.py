from V8RandomnessPredictor import V8RandomnessPredictor

sequence = [
    0.552974198778651,
    0.6091405699404759,
    0.30377761820864757,
    0.6615235206792083,
    0.27808781139439565,
]

expected = [
    0.4343553191734457,
    0.22840345766161696,
    0.5582855770529151,
    0.50415840256704,
    0.5362054737043922,
]

pred = V8RandomnessPredictor(sequence)

for i in range(len(expected)):
    predicted = pred.predict_next()
    correct = predicted == expected[i]
    if correct == False:
        raise Exception(
            f"Incorrect prediction! Expected {expected[i]} but got {predicted}"
        )
    print(f"Correct? {correct}\t| predicted={predicted}\t| expected={expected[i]}")
