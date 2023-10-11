# CoMMuTE with GPT-4 and CLIP
Solving CoMMuTE benchmark with GPT-4 and CLIP.

## How does it work?
It back translates French (only French for now, but I believe the results would scale to other languages in the CoMMuTE dataset as well) to English using GPT-4, while carefully asking a text-only GPT-4 to disambiguate wordings in English. Then, we use CLIP as a zero-shot classifier to select the English description that better represents the given image. We achieved a 83.8% accuracy on the En->Fr subset, far surpassing the 67.2% accuracy of the proposed approach in the original paper.

I believe this method is legitimate because in the original paper "Tackling Ambiguity with Images" by Futeral et al, the authors used **perplexity** of possible options, rather than text similarity, as the accuracy metric for their CoMMuTE dataset and their proposed model. Since perplexity measures the more probable option out of the two given choices, they are essentially using the model as a **classifier**, not a text generator. Our proposed solution also attempts to select the more probable option of the two choices given in the dataset, so it constitutes a fair comparison to the aforementioned paper.

## What does it mean?
This paper, along with their proposed CoMMuTE dataset & evaluation method, is deeply flawed. The proposed solution uses VMLM on English as the training objective, so the model learned image recognition implicitly during training. The model also takes CLIP embeddings as the input, and the authors' own ablation studies showed that removing CLIP embedding would reduce the model accuracy to **random guessing**, which further confirms that the model is performing classification using CLIP embeddings.

What is more concerning is the proposed CoMMuTE dataset and evaluation setup. The dataset only contains very short and concise sentences, which means the dataset strongly encourages the model to perform **classification**, rather than **machine translation**. Moreover, rather than comparing the text similarity of the generated text against the ground truth solution, the paper evaluated the perplexity, or the probability of the two candidate solutions offered in the dataset. This is basically using the model to perform image classification, not translation, further invalidating the benchmark.

## How to run:
```
pip3 install -r requirements.txt
python3 translate_with_openai.py --openai-api-key YOUR_OPENAI_API_KEY
python3 map_answers_to_correct_incorrect.py
python3 classify_with_clip.py
```

## Related code and paper:
Tackling Ambiguity with Images: Improved Multimodal Machine Translation and Contrastive Evaluation by Futeral et al, published in ACL 2023. [Paper Link.](https://aclanthology.org/2023.acl-long.295/)

[Code from the original paper](https://github.com/MatthieuFP/VGAMT)

[Dataset from the original paper](https://github.com/MatthieuFP/CoMMuTE)
