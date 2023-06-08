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
elapsed: 0.1075437090039486
elapsed: 0.014960166001401376
elapsed: 0.013572791001934092
elapsed: 0.01361416599684162
elapsed: 0.014712707998114638
elapsed: 0.014573832995665725
elapsed: 0.015756124994368292
elapsed: 0.01592954200168606
elapsed: 0.015459165995707735
elapsed: 0.014550291001796722


---- get 10 features by BatchEvaluateFeature API ----
elapsed: 0.13433566699677613
elapsed: 0.12432420800178079
elapsed: 0.13118854200001806
elapsed: 0.13287820800178451
elapsed: 0.1317335420026211
elapsed: 0.13228108300245367
elapsed: 0.1325145840019104
elapsed: 1.1390634999988833
elapsed: 0.1317663329973584
elapsed: 0.13020508300542133
```

## Clean up

Delete all resources.

```bash
python -m cleanup
```