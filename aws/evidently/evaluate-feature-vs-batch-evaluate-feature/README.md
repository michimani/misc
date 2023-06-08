EvaluateFeature vs BatchEvaluateFeature
===

Now, we check that how long does it take to get value of each features.  

## Setup

```bash
. .venv/bin/activate \
&& pip install pip --upgrade \
&& pip install -r requirements.lock
```

## Prepare

Create following resources.

- An Evidently::Project
- 10 Evidently::Feature

```bash
python -m prepare
```

## Measure time

Measure time to get value of all features. The process of acquiring the values of 10 features is executed 10 times each.

```bash
python -m measure
```

Result.

```
Listed features. count: 10


---- get 10 features by EvaluateFeature API ----
elapsed: 0.1720401669954299
elapsed: 0.12039266699866857
elapsed: 0.12361987500480609
elapsed: 0.12408404199959477
elapsed: 0.1212201250018552
elapsed: 0.11948174999997718
elapsed: 0.10677008399943588
elapsed: 0.11592154199752258
elapsed: 0.12358333299926016
elapsed: 0.12295774999802234


---- get 10 features by BatchEvaluateFeature API ----
elapsed: 0.0610867089999374
elapsed: 0.016109041003801394
elapsed: 0.014233082998543978
elapsed: 0.016069457997218706
elapsed: 0.016354667000996415
elapsed: 0.015939832999720238
elapsed: 0.014508166997984517
elapsed: 0.014131541000097059
elapsed: 0.013616000003821682
elapsed: 0.014615457999752834
```

## Clean up

Delete all resources.

```bash
python -m cleanup
```