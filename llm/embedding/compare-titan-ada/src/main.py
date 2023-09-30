import sys

from bedrock import BedrockEmbeddingClient
from calc import distance
from embedding import create_embedding, debug_embedding
from oa import OpenAIEmbeddingClient

if __name__ == "__main__":
    openai_client = OpenAIEmbeddingClient()
    bedrock_client = BedrockEmbeddingClient()

    text = "Hello, world!"
    if len(sys.argv) > 1:
        text = sys.argv[1]
    print(f"Text: {text}")

    ada_embd = create_embedding(openai_client, text)
    titan_embd = create_embedding(bedrock_client, text)

    print("\nOpenAI Ada Embedding:")
    debug_embedding(ada_embd)

    print("\nBedrock Titan Embedding:")
    debug_embedding(titan_embd)

    d = distance(ada_embd, titan_embd)

    print(f"\nDistance: {d}")
