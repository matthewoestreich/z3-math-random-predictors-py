# z3-math-random-predictors-py
 Use [z3](https://github.com/Z3Prover/z3) to predict `Math.random()` output in V8 (Node), Chrome, Firefox, and Safari.

# Confirmed Working Versions

| Environment | Version | Notes |
| --- | --- | --- |
| V8 (Node) | v23.3.0 | Random numbers created via script as well as REPL |
| Chrome | Version 135.0.7049.96 (Official Build) (x86_64) | |
| Firefox | Version: 137.0.2<br>Build ID: 20250414091429 | Had to browse to the URL `about:support` to see this info |
| Safari | Version 18.1.1 (20619.2.8.11.12) | |

# Testing

To test all predictors, from root of this project, run:

(ps. I don't really understand the Python module system that well as I rarely work with Python, so if there is a better way please let me know)

```bash
python test_all.py
```

To test a single predictor, from the root of this project, run:

```bash
# Firefox
python -m Firefox.firefox_testing
# V8/Node
python -m V8.v8_testing
# Chrome
python -m Chrome.chrome_testing
# Safari
python -m Safari.safari_testing
```

Expected Output :

```
Testing V8:

correct? True   |       predicted=0.3817506775921966    |       expected=0.3817506775921966
correct? True   |       predicted=0.796686249606257     |       expected=0.796686249606257
correct? True   |       predicted=0.9976624647084931    |       expected=0.9976624647084931
correct? True   |       predicted=0.39031891128710483   |       expected=0.39031891128710483
correct? True   |       predicted=0.7825669445360215    |       expected=0.7825669445360215

Testing Safari:

correct? True   |       predicted=0.9169503416986349    |       expected=0.9169503416986349
correct? True   |       predicted=0.1759463668507366    |       expected=0.1759463668507366
correct? True   |       predicted=0.35008784418587335   |       expected=0.35008784418587335
correct? True   |       predicted=0.023140803710573365  |       expected=0.023140803710573365
correct? True   |       predicted=0.9865562268708263    |       expected=0.9865562268708263
correct? True   |       predicted=0.8374988042057177    |       expected=0.8374988042057177
correct? True   |       predicted=0.14916960299225546   |       expected=0.14916960299225546
correct? True   |       predicted=0.696969506883636     |       expected=0.696969506883636
correct? True   |       predicted=0.7524093188618326    |       expected=0.7524093188618326
correct? True   |       predicted=0.5628165932674238    |       expected=0.5628165932674238
correct? True   |       predicted=0.603674732816703     |       expected=0.603674732816703
correct? True   |       predicted=0.8074868073655229    |       expected=0.8074868073655229
correct? True   |       predicted=0.8882697110301722    |       expected=0.8882697110301722
correct? True   |       predicted=0.5033962476806244    |       expected=0.5033962476806244
correct? True   |       predicted=0.21262148916910428   |       expected=0.21262148916910428

Testing Firefox:

correct? True   |       predicted=0.13963871472821332   |       expected=0.13963871472821332
correct? True   |       predicted=0.25068024611907636   |       expected=0.25068024611907636
correct? True   |       predicted=0.6656237481612675    |       expected=0.6656237481612675
correct? True   |       predicted=0.7381091878692425    |       expected=0.7381091878692425
correct? True   |       predicted=0.8709382509549467    |       expected=0.8709382509549467
correct? True   |       predicted=0.49171337524788294   |       expected=0.49171337524788294
correct? True   |       predicted=0.6991749430716799    |       expected=0.6991749430716799
correct? True   |       predicted=0.9530887478758369    |       expected=0.9530887478758369
correct? True   |       predicted=0.781511163650037     |       expected=0.781511163650037
correct? True   |       predicted=0.699311162730038     |       expected=0.699311162730038

Testing Chrome:

correct? True   |       predicted=0.8199006769436774    |       expected=0.8199006769436774
correct? True   |       predicted=0.6250240806313154    |       expected=0.6250240806313154
correct? True   |       predicted=0.9101975676132608    |       expected=0.9101975676132608
correct? True   |       predicted=0.5889203398264599    |       expected=0.5889203398264599
correct? True   |       predicted=0.5571161440436232    |       expected=0.5571161440436232
correct? True   |       predicted=0.9619184649129092    |       expected=0.9619184649129092
correct? True   |       predicted=0.8385620929536599    |       expected=0.8385620929536599
correct? True   |       predicted=0.3822042053588621    |       expected=0.3822042053588621
correct? True   |       predicted=0.5040552869863579    |       expected=0.5040552869863579
correct? True   |       predicted=0.12014019399083042   |       expected=0.12014019399083042
correct? True   |       predicted=0.44332968383610927   |       expected=0.44332968383610927
correct? True   |       predicted=0.37830079319230936   |       expected=0.37830079319230936
correct? True   |       predicted=0.542449069899975     |       expected=0.542449069899975
correct? True   |       predicted=0.0659240460476268    |       expected=0.0659240460476268
correct? True   |       predicted=0.9589494984837686    |       expected=0.9589494984837686
correct? True   |       predicted=0.007621633090565627  |       expected=0.007621633090565627
correct? True   |       predicted=0.14119301022498787   |       expected=0.14119301022498787
correct? True   |       predicted=0.9964718645470699    |       expected=0.9964718645470699
correct? True   |       predicted=0.14527130036353442   |       expected=0.14527130036353442
correct? True   |       predicted=0.6260597083849548    |       expected=0.6260597083849548
correct? True   |       predicted=0.86354903522581      |       expected=0.86354903522581
correct? True   |       predicted=0.7245123107811886    |       expected=0.7245123107811886
correct? True   |       predicted=0.6565323828155891    |       expected=0.6565323828155891
correct? True   |       predicted=0.3636039851663503    |       expected=0.3636039851663503
correct? True   |       predicted=0.5799453712253447    |       expected=0.5799453712253447

Are all tests successful?
        True
```