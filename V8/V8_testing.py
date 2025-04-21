from V8.V8RandomnessPredictor import V8RandomnessPredictor

sequence_og = [
    0.552974198778651,
    0.6091405699404759,
    0.30377761820864757,
    0.6615235206792083,
    0.27808781139439565,
]

expected_og = [
    0.4343553191734457,
    0.22840345766161696,
    0.5582855770529151,
    0.50415840256704,
    0.5362054737043922,
]

sequence_b = [
    0.5444405645692001,
    0.9203027285129253,
    0.0880920246518424,
    0.6555723374589169,
    0.06183370879928152,
]

expected_b = [
    0.3817506775921966,
    0.796686249606257,
    0.9976624647084931,
    0.39031891128710483,
    0.7825669445360215,
]


def testV8():
    isOverallSuccess = True
    p = V8RandomnessPredictor(sequence_b)
    for _, expect in enumerate(expected_b):
        predicted = p.predict_next()
        correct = predicted == expect
        if correct == False:
            isOverallSuccess = False
        print(f"Correct? {correct}\t| predicted={predicted}\t| expected={expect}")
    return isOverallSuccess


if __name__ == "__main__":
    testV8()
