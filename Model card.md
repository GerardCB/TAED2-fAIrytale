# fAIrytale model card

Last updated: September 2022

Inspired by [Stable Diffusion v1-4 Model Card](https://huggingface.co/CompVis/stable-diffusion-v1-4), we’re providing some accompanying information about the fAIrytale model we are releasing. 

Stable Diffusion is a latent text-to-image diffusion model capable of generating photo-realistic images given any text input. The fAIrytale model combines the Stable-Diffusion-v1-4 checkpoint with [FLAIR](https://huggingface.co/flair/ner-englis), for the Named Entity Recognition task, and with [ROBERTA](https://arxiv.org/abs/1907.11692), for QA and Multi Natural Languagse Inference (MNLI) tasks.

However, the fAIrytale model only fine-tunnes the Stable Diffusion Model. Therefore, in this model card ww will focus on this model.

 ## Model Details
- **Originally developed by:** Robin Rombach, Patrick Esser
- **Fine tunned by:** Helena Ferran Padua, David Pujalte Pérez, Pau Tarragó Navarra,  Marc Torrens Punsola, Gerard Calvo Bartra
- **Model type:** Diffusion-based text-to-image generation model
- **Language(s):** English
- **License:** [The CreativeML OpenRAIL M license](https://huggingface.co/spaces/CompVis/stable-diffusion-license) is an [Open RAIL M license](https://www.licenses.ai/blog/2022/8/18/naming-convention-of-responsible-ai-licenses), adapted from the work that [BigScience](https://bigscience.huggingface.co/) and [the RAIL Initiative](https://www.licenses.ai/) are jointly carrying in the area of responsible AI licensing. See also [the article about the BLOOM Open RAIL license](https://bigscience.huggingface.co/blog/the-bigscience-rail-license) on which our license is based.
- **Model Description:** This is a model that can be used to generate and modify images based on text prompts. It is a [Latent Diffusion Model](https://arxiv.org/abs/2112.10752) that uses a fixed, pretrained text encoder ([CLIP ViT-L/14](https://arxiv.org/abs/2103.00020)) as suggested in the [Imagen paper](https://arxiv.org/abs/2205.11487).
- **Resources for more information:** [GitHub Repository](https://github.com/CompVis/stable-diffusion), [Paper](https://arxiv.org/abs/2112.10752).
- **Cite as:**

      @InProceedings{Rombach_2022_CVPR,
          author    = {Rombach, Robin and Blattmann, Andreas and Lorenz, Dominik and Esser, Patrick and Ommer, Bj\"orn},
          title     = {High-Resolution Image Synthesis With Latent Diffusion Models},
          booktitle = {Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition (CVPR)},
          month     = {June},
          year      = {2022},
          pages     = {10684-10695}
      }

# Uses

## Direct Use 
The model is intended for research purposes only. Possible research areas and
tasks include

- Generation of artworks and use in design and other artistic processes.
- Applications in educational or creative tools.

Excluded uses are described below.

 ### Misuse, Malicious Use, and Out-of-Scope Use
_Note: This section is taken from the [DALLE-MINI model card](https://huggingface.co/dalle-mini/dalle-mini), but applies in the same way to fAIrytale_.


The model should not be used to intentionally create or disseminate images that create hostile or alienating environments for people. This includes generating images that people would foreseeably find disturbing, distressing, or offensive; or content that propagates historical or current stereotypes.

#### Out-of-Scope Use
The model was not trained to be factual or true representations of people or events, and therefore using the model to generate such content is out-of-scope for the abilities of this model.

#### Misuse and Malicious Use
Using the model to generate content that is cruel to individuals is a misuse of this model. This includes, but is not limited to:

- Generating demeaning, dehumanizing, or otherwise harmful representations of people or their environments, cultures, religions, etc.
- Intentionally promoting or propagating discriminatory content or harmful stereotypes.
- Impersonating individuals without their consent.
- Sexual content without consent of the people who might see it.
- Mis- and disinformation
- Representations of egregious violence and gore
- Sharing of copyrighted or licensed material in violation of its terms of use.
- Sharing content that is an alteration of copyrighted or licensed material in violation of its terms of use.

## Limitations and Bias

### Limitations

- The model does not achieve perfect photorealism
- The model cannot render legible text
- The model does not perform well on more difficult tasks which involve compositionality, such as rendering an image corresponding to “A red cube on top of a blue sphere”
- Faces and people in general may not be generated properly.
- The model was trained mainly with English captions and will not work as well in other languages.
- The autoencoding part of the model is lossy
- The model was trained on a large-scale dataset
  [LAION-5B](https://laion.ai/blog/laion-5b/) which contains adult material
  and is not fit for product use without additional safety mechanisms and
  considerations.
- No additional measures were used to deduplicate the dataset. As a result, we observe some degree of memorization for images that are duplicated in the training data.
  The training data can be searched at [https://rom1504.github.io/clip-retrieval/](https://rom1504.github.io/clip-retrieval/) to possibly assist in the detection of memorized images.

### Bias

While the capabilities of image generation models are impressive, they can also reinforce or exacerbate social biases. 
Stable Diffusion v1 was trained on subsets of [LAION-2B(en)](https://laion.ai/blog/laion-5b/), 
which consists of images that are primarily limited to English descriptions. 
Texts and images from communities and cultures that use other languages are likely to be insufficiently accounted for. 
This affects the overall output of the model, as white and western cultures are often set as the default. Further, the 
ability of the model to generate content with non-English prompts is significantly worse than with English-language prompts.


## Training

**Training Data**
The model developers used the following dataset for training the model:

- LAION-2B (en) and subsets thereof
- Custom dataset obtained through web scrapping with [monkeypen](https://monkeypen.com/pages/free-childrens-books/), using 49 of the 50 available free books that the web has available.

**Training Procedure**
Stable Diffusion v1-4 is a latent diffusion model which combines an autoencoder with a diffusion model that is trained in the latent space of the autoencoder. During training, 

- Images are encoded through an encoder, which turns images into latent representations. The autoencoder uses a relative downsampling factor of 8 and maps images of shape H x W x 3 to latents of shape H/f x W/f x 4
- Text prompts are encoded through a ViT-L/14 text-encoder.
- The non-pooled output of the text encoder is fed into the UNet backbone of the latent diffusion model via cross-attention.
- The loss is a reconstruction objective between the noise that was added to the latent and the prediction made by the UNet.

The fAIrytale model is further trained using [Textual Inversion](https://textual-inversion.github.io/) to enhance the children's book style and to achive temporal coherence of characters' representations.

The original setup used to train Stable diffusion included

- **Hardware:** 32 x 8 x A100 GPUs
- **Optimizer:** AdamW
- **Gradient Accumulations**: 2
- **Batch:** 32 x 8 x 2 x 4 = 2048
- **Learning rate:** warmup to 0.0001 for 10,000 steps and then kept constant

However, the fine tunning of the model only includes

- **Hardware:** Google Colab's 1 x Tesla K80 GPU

## Evaluation Results 
Evaluations of the original Stable Diffusion v1.4 model with different classifier-free guidance scales (1.5, 2.0, 3.0, 4.0,
5.0, 6.0, 7.0, 8.0) and 50 PLMS sampling
steps show the relative improvements of the checkpoints:

![pareto](https://huggingface.co/CompVis/stable-diffusion/resolve/main/v1-variants-scores.jpg)

Evaluated using 50 PLMS steps and 10000 random prompts from the COCO2017 validation set, evaluated at 512x512 resolution. Not optimized for FID scores.
## Environmental Impact

**Stable Diffusion v1** **Estimated Emissions**
Based on that information, we estimate the following CO2 emissions using the [Machine Learning Impact calculator](https://mlco2.github.io/impact#compute) presented in [Lacoste et al. (2019)](https://arxiv.org/abs/1910.09700). The hardware, runtime, cloud provider, and compute region were utilized to estimate the carbon impact.

- **Hardware Type:** A100 PCIe 40GB
- **Hours used:** 150000
- **Cloud Provider:** AWS
- **Compute Region:** US-east
- **Carbon Emitted (Power consumption x Time x Carbon produced based on location of power grid):** 11250 kg CO2 eq.

**fAIrytale fine tunning** **Estimated Emissions**
Still to be determined.

