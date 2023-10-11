import argparse
import openai


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--translated_file", type=str, default="translated.fr")
    parser.add_argument("--output_file", type=str, default="output.en")
    parser.add_argument("--system-prompt-file", type=str, default="gpt_4_system_prompt.txt")
    parser.add_argument("--question-prompt-file", type=str, default="gpt_4_question_prompt_few_shot.txt")
    parser.add_argument("--openai-api-key", type=str, required=True)
    args = parser.parse_args()

    # Read the prompts from the files
    with open(args.system_prompt_file, "r") as f:
        SYSTEM_PROMPT = f.read().strip()
    with open(args.question_prompt_file, "r") as f:
        QUESTION_PROMPT = f.read().strip()

    # Read the translated file
    with open(args.translated_file, "r") as f:
        translated_lines = f.readlines()

    openai.api_key = args.openai_api_key

    # Translate the translated file two lines at a time, and write the output to the output file.
    with open(args.output_file, "w") as f:
        for i in range(0, len(translated_lines), 2):
            # Get the two lines
            line1 = translated_lines[i]
            line2 = translated_lines[i + 1]

            # Create the prompt
            prompt = QUESTION_PROMPT.format(sentence_pair=line1 + line2)

            print("Prompt: " + prompt)

            # Generate the response
            response = openai.ChatCompletion.create(
                model="gpt-4-0613",
                messages=[
                    {
                        "role": "system",
                        "content": SYSTEM_PROMPT,
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
                temperature=1,
                max_tokens=256,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
            )

            # Get the response
            assistant_response = response['choices'][0]['message']['content'].strip()

            # Write the response to the output file
            print("Translated: \n" + assistant_response)
            f.write(assistant_response + "\n")
