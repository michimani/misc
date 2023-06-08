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

Measure time to get value of all features.

```bash
python -m measure
```

## Clean up

Delete all resources.

```bash
python -m cleanup
```