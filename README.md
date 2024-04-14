# LLM Risk Assessment automatization

Repo containing code discussed in: https://medium.com/@ishish222/revolutionizing-risk-assessment-part-2-boilerplate-application-5df41609bd39

## Prerequisites

I'm using poetry for dependency management. 

You'll need access to AWS Bedrock service and the 'anthropic.claude-v2' model. 
You can export AWS credentials into env, set them up in .env.* or set up default 
profile with necessary access in ~/.aws 

## Usage

Dependencies are managed with poetry. Once you installed poetry:

```bash
$ poetry install
$ poetry shell
$ cd app/src
$ python risk_register.py
```

The application should be available at: http://127.0.0.1:8080.
Samples are available in resources/samples.

## Langsmith integration

In order to integrate with Langsmith you'll need to set envs:

```bash
#LangSmith configuration
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
LANGCHAIN_API_KEY="<your Langsmith API key>"
LANGCHAIN_PROJECT="<your project name>"
```

either by exporting or configuring in an .env.* file.