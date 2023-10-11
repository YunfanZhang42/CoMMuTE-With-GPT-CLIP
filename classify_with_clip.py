import argparse
import os
import torch
import clip
from PIL import Image


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--correct-file", type=str, default="correct.en")
    parser.add_argument("--incorrect-file", type=str, default="incorrect.en")
    parser.add_argument("--img-order-file", type=str, default="img.order")
    parser.add_argument("--img-dir", type=str, default="./images")
    parser.add_argument("--clip-model-name", type=str, default="ViT-L/14")
    args = parser.parse_args()

    # Read both the correct and incorrect files
    with open(args.correct_file, "r") as f:
        correct_lines = f.readlines()
    with open(args.incorrect_file, "r") as f:
        incorrect_lines = f.readlines()
    # Read the image order file
    with open(args.img_order_file, "r") as f:
        img_order = f.readlines()

    print("Number of samples:", len(correct_lines))
    assert len(correct_lines) == len(incorrect_lines) == len(img_order), "Number of samples in the files do not match."

    # Load the CLIP model
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, preprocess = clip.load(args.clip_model_name, device=device)

    total_correct = 0

    # For every sample, compute the logits and see if the correct answer has a higher probability than the incorrect answer
    for i in range(len(img_order)):
        # Get the correct and incorrect answers
        correct_answer = correct_lines[i].strip()
        incorrect_answer = incorrect_lines[i].strip()

        # Get the image path
        img_path = os.path.join(args.img_dir, img_order[i].strip())

        # Load the image and the text
        image = preprocess(Image.open(img_path)).unsqueeze(0).to(device)
        text = clip.tokenize([correct_answer, incorrect_answer]).to(device)

        # Encode the image and the text
        with torch.no_grad():
            # Compute the logits
            logits_per_image, logits_per_text = model(image, text)
            probs = logits_per_image.softmax(dim=-1).cpu().numpy()

            correct = probs[0][0] > probs[0][1]
            print("Label probs:", probs, "Correct:", correct)

            if correct:
                total_correct += 1
    
    print("Total correct:", total_correct, "Accuracy:", total_correct / len(img_order))
