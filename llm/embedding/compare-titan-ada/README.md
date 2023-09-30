Comparison of embedding with Amazon Titan and OpenAI Ada
===

# Preparing

## Install dependencies

```bash
pytnon3 -m venv .venv \
&& source .venv/bin/activate \
&& pip install pip --upgrade \
&& pip install -r requirements.lock
```

## Set up environment variables

```bash
export OPENAI_ORGANIZATION_ID='<your-org-id>'
export OPENAI_API_KEY='<your-api-key>'
```

# Run

```bash
python src/main.py 'Hello World!'
```

Output:

```
Text: Hello World!

OpenAI Ada Embedding:
Dimensions: 1536
Embedding: [0.0023471873719245195, 0.0002812144230119884 ... -0.006565207615494728, -0.014765428379178047]

Bedrock Titan Embedding:
Dimensions: 1536
Embedding: [0.45703125, 0.30078125 ... -0.64453125, 0.114746094]

Distance: 19.786382537735417

Similarity: -0.003550259960754387
```

