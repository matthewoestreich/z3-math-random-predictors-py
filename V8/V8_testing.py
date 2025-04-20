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

sequence = [
    0.5444405645692001,
    0.9203027285129253,
    0.0880920246518424,
    0.6555723374589169,
    0.06183370879928152,
]

expected = [
    0.3817506775921966,
    0.796686249606257,
    0.9976624647084931,
    0.39031891128710483,
    0.7825669445360215,
]

def testV8():
    p = V8RandomnessPredictor(sequence)
    for _, expect in enumerate(expected):
        predicted = p.predict_next()
        correct = predicted == expect
        print(f"Correct? {correct}\t| predicted={predicted}\t| expected={expect}")
        
if __name__ == "__main__":
    from V8RandomnessPredictor import V8RandomnessPredictor
    testV8()
else:
    from V8.V8RandomnessPredictor import V8RandomnessPredictor
