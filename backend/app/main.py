from fastapi import FastAPI, BackgroundTasks
import time
from diffusers import StableDiffusionPipeline
import os
import json
import base64
from io import BytesIO

def set_calculation_percentage(userId, percentage):
    global calculations
    calculations[userId]['progress'] = str(percentage)[:3]

# Auxiliar functions
def load_sd_pipe(model_path, device):
    pipeline = StableDiffusionPipeline.from_pretrained(model_path)
    pipeline.to(device)
    return pipeline


def read_book(book):
    return list(filter(lambda x: x != '', book.split('<|endofparagraph|>')))


def generate_images(pipe, paragraph, num_samples=1, guidance_scale=7.5, num_inference_steps=50, height=512, width=512):
    # ONLY WORKING WITH A SINGLE IMAGE
    paragraph += ', in the style of a fAIrytale illustration.'
    image = pipe(
        [paragraph]*num_samples,
        num_inference_steps=num_inference_steps,
        guidance_scale=guidance_scale,
        height=height,
        width=width
    ).images[0]

    output = BytesIO()
    image.save(output, format='JPEG')
    imageData = base64.b64encode(output.getvalue())

    # Decode from bytes to string
    if not isinstance(imageData, str):
        imageData = imageData.decode()
    dataUrl = 'data:image/jpg;base64,' + imageData
    return dataUrl


# Main function
def book_to_images(book, update_percentage, num_samples=1, num_inference_steps=10, height=512, width=512, guidance_scale=7.5):
    gen_images = []
    paragraphs = read_book(book)
    
    for i, paragraph in enumerate(paragraphs):
        gen_images.append(generate_images(pipe, paragraph, num_samples, guidance_scale, num_inference_steps, height, width))
        update_percentage((i+1)/len(paragraphs))
    output = [paragraphs, gen_images]

    return output

def generate_images_task(userId, inputText):
    global calculations
    output = book_to_images(inputText, update_percentage=lambda x: set_calculation_percentage(userId, x))
    calculations[userId]['images'] = output

calculations = {}

model_path = './fAIrytale/'

pipe = load_sd_pipe(model_path, 'cpu')

tags_metadata = [
    {
        "name": "user-exists",
        "description": "Check whether the user exists in the database. They exist whenever they make a generate request.",
    },
    {
        "name": "generate",
        "description": "Send the order to generate the images from the book. Separate each paragraph of the book with the keyword <|endofparagraph|> instead of newline.",
    },
    {
        "name": "progress",
        "description": "Show a percentage progress of how many images are generated from how many paragraphs from total.",
    },
    {
        "name": "images",
        "description": "Get the images generated. One per paragraph.",
    },
]

app = FastAPI(title='Welcome to fAIrytale public API', openapi_tags=tags_metadata)


@app.get('/user-exists', tags=['user-exists'])
async def check_user(userId):
    return {'exists': userId in calculations}

@app.post('/generate', tags=['generate'])
async def create_new_calculation(userId: str, inputText: str, background_tasks: BackgroundTasks):
    global calculations
    calculations[userId] = {'progress': '0', 'images': []}
    background_tasks.add_task(generate_images_task, userId, inputText)

    #time.sleep(10) # COMMENT OUT FOR ML API
    #calculations[userId]['images'] = [1,2,3,4,5] # COMMENT OUT FOR ML API

    return {"status": "Order to generate images sent."}
    


@app.get('/progress', tags=['progress'])
async def check_progress(userId):
    if userId in calculations:
        return {'progress': calculations[userId]['progress']}
    return {'progress': -1}

@app.get('/images', tags=['images'])
async def get_images_generated(userId):
    if userId in calculations and calculations[userId]['progress'] == '1.0':
        return {'images': calculations[userId]['images']}
    return {'images': -1}


# To start the API application (on command line)
# !uvicorn main:app --reload