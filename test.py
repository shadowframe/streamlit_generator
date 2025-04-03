import runpod
import torch
from diffusers import StableDiffusionPipeline
from io import BytesIO
import base64

assert (
    torch.cuda.is_available()
), "CUDA is not available. Make sure you have a GPU instance."


def load_model():
    model_id = "runwayml/stable-diffusion-v1-5"
    pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
    # to run on cpu change `cuda` to `cpu`
    pipe = pipe.to("cuda")
    return pipe


def image_to_base64(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")


def stable_diffusion_handler(event):
    global model

    if "model" not in globals():
        model = load_model()

    prompt = event["input"].get("prompt")

    if not prompt:
        return {"error": "No prompt provided for image generation."}

    try:
        image = model(prompt).images[0]
        image_base64 = image_to_base64(image)

        return {"image": image_base64, "prompt": prompt}

    except Exception as e:
        return {"error": str(e)}


runpod.serverless.start({"handler": stable_diffusion_handler})