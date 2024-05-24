from mlx_lm import generate, load

model, tokenizer = load("mlx-community/Meta-Llama-3-8B-Instruct-4bit")

prompt = "<|begin_of_text|>"

while True:
    try:
        user_input = input("\n>> ")

        if user_input == "exit":
            break

        prompt += f"""<|start_header_id|>user<|end_header_id|>
        <|start_header_id|>user<|end_header_id|>
        {user_input}<|eot_id|>

        <|start_header_id|>assistant<|end_header_id|>"""

        response = generate(model, tokenizer, prompt=prompt, verbose=False)

        print(response)

        prompt += f"<|start_header_id|>{response}<|end_header_id|>\n"
    except KeyboardInterrupt:
        print("\n\nGoodbye!")
        break
    except Exception as e:
        print(e)
        break
