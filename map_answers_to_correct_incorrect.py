import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output_file", type=str, default="output.en")
    parser.add_argument("--correct-file", type=str, default="correct.en")
    parser.add_argument("--incorrect-file", type=str, default="incorrect.en")
    args = parser.parse_args()

    # Read the translated file
    with open(args.output_file, "r") as f:
        translated_lines = f.readlines()

    # For every two lines, map the first line to correct and the second line to incorrect,
    # and then map the second line to correct and the first line to incorrect.
    with open(args.correct_file, "w") as f_correct, open(args.incorrect_file, "w") as f_incorrect:
        for i in range(0, len(translated_lines), 2):
            # Get the two lines
            line1 = translated_lines[i]
            line2 = translated_lines[i + 1]

            # Write the lines to the files
            f_correct.write(line1)
            f_incorrect.write(line2)
            f_correct.write(line2)
            f_incorrect.write(line1)
