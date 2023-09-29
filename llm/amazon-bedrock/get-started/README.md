Get started Amazon Bedrock
===

Sample implementation of Amazon Bedrock using AWS CDK for Python (boto3).

# Preparing

```bash
python3 -m venv .venv \
&& source .venv/bin/activate \
&& pip install pip --upgrade \
&& pip install -r requirements.txt
```

# Run

## List foundation models

```bash
python src/main.py list-models
```


## Create embedding

Create embedding using **Titan Embeddings G1** model.

```bash
python src/main.py create-embedding --input-text 'Today is sunny'
```