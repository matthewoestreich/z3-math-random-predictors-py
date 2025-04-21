from Safari.SafariRandomnessPredictor import SafariRandomnessPredictor

"""
All numbers generated in Safari via devtools console.
"""

sequence_og = [
    0.6663962879405719,
    0.6024809927558423,
    0.16506417842523025,
    0.18138630317100313,
    0.6993210053643432,
]

expected_og = [
    0.2959814655785803,
    0.378049342563327,
    0.5729973893645592,
    0.45186669410185754,
    0.3653124927904573,
    0.0926216232931818,
    0.0027796814434313255,
    0.43004672005601663,
    0.7688095836856329,
    0.20944875623977732,
    0.6768731758679019,
    0.913787319793328,
    0.9795986365713938,
    0.4330400271108311,
    0.5967102957238284,
]

sequence = [
    0.8915648990458412,
    0.24318082036313127,
    0.8954436283231135,
    0.03158370321205917,
    0.7432899476140522,
]

expected = [
    0.9169503416986349,
    0.1759463668507366,
    0.35008784418587335,
    0.023140803710573365,
    0.9865562268708263,
    0.8374988042057177,
    0.14916960299225546,
    0.696969506883636,
    0.7524093188618326,
    0.5628165932674238,
    0.603674732816703,
    0.8074868073655229,
    0.8882697110301722,
    0.5033962476806244,
    0.21262148916910428,
]


def testSafari():
    isOverallSuccess = True
    pred = SafariRandomnessPredictor(sequence)
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
    testSafari()
