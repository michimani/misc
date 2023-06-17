get-started-to-use-function-calling
===

This is a sample program to use function calling API of OpenAI API. In this sample, we create a feature flag has boolean value on CloudWatch Evidently with natural language.

## Reference

- [Function calling | GPT - OpenAI API](https://platform.openai.com/docs/guides/gpt/function-calling)
- [Chat | API Reference - OpenAI API](https://platform.openai.com/docs/api-reference/chat/create)

## Prepare

Create virtual environment and install requirements.

```bash
python3 -m venv .venv \
&& source .venv/bin/activate \
&& pip install pip --upgrade \
&& pip install -r requirements.lock
```

⚠ The permission to create project and feature on CloudWatch Evidently is required.

## Usage

```bash
python -m main
```

```bash
What do you want to create a feature? >
```

Input a project name, feature name and other information you want to create. For example:

```bash
I want to create a feature that determines if sushi is served or not. The name of the feature is sushi and the project name is food-project. If entity id is force-sushi, this feature's value will be true.
```

```bash
-------openai_message-------
{
  "role": "assistant",
  "content": null,
  "function_call": {
    "name": "create_evidently_boolean_feature",
    "arguments": "{\n  \"project_name\": \"food-project\",\n  \"feature_name\": \"sushi\",\n  \"default_value\": false,\n  \"override_rules\": [[\"force-sushi\", \"True\"]]\n}"
  }
}
--------------------
function_call: create_evidently_boolean_feature
-------params-------
CreateBooleanFeatureInput(project_name='food-project', feature_name='sushi', default_value=False, override_rules=[('force-sushi', 'True')])
--------------------
Created project food-project with ARN arn:aws:evidently:ap-northeast-1:000000000000:project/food-project
Created feature sushi with ARN arn:aws:evidently:ap-northeast-1:000000000000:project/food-project/feature/sushi

-------Response-------
created a feature info

    Project: food-project
    Feature: sushi

    Check the feature on CloudWatch Evidently using following command:

    aws evidently get-feature --project 'food-project' --feature 'sushi'
```

Check the feature on CloudWatch Evidently.

```bash
$ aws evidently get-feature --project 'food-project' --feature 'sushi'

{
    "feature": {
        "arn": "arn:aws:evidently:ap-northeast-1:000000000000:project/food-project/feature/sushi",
        "createdTime": "2023-06-18T01:48:39.219000+09:00",
        "defaultVariation": "False",
        "description": "",
        "entityOverrides": {
            "force-sushi": "True"
        },
        "evaluationRules": [],
        "evaluationStrategy": "ALL_RULES",
        "lastUpdatedTime": "2023-06-18T01:48:39.219000+09:00",
        "name": "sushi",
        "project": "arn:aws:evidently:ap-northeast-1:000000000000:project/food-project",
        "status": "AVAILABLE",
        "tags": {},
        "valueType": "BOOLEAN",
        "variations": [
            {
                "name": "True",
                "value": {
                    "boolValue": true
                }
            },
            {
                "name": "False",
                "value": {
                    "boolValue": false
                }
            }
        ]
    }
}
```