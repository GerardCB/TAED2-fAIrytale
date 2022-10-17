from fastapi import FastAPI
import time
from diffusers import StableDiffusionPipeline
import os

def set_calculation_percentage(userId, percentage):
    global calculations
    calculations[userId]['progress'] = percentage

# Auxiliar functions
def load_sd_pipe(model_path, device):
    pipeline = StableDiffusionPipeline.from_pretrained(model_path)
    pipeline.to(device)
    return pipeline


def read_book(book):
    paragraphs = book.split('\n')
    return paragraphs


def generate_images(pipe, paragraph, num_samples=1, guidance_scale=7.5, num_inference_steps=50, height=512, width=512):
    paragraph += ', in the style of a fAirytale illustration.'
    images = pipe(
        [paragraph]*num_samples,
        num_inference_steps=num_inference_steps,
        guidance_scale=guidance_scale,
        height=height,
        width=width
    )
    return images


# Main function
def book_to_images(book, update_percentage, num_samples=1, num_inference_steps=10, height=512, width=512, guidance_scale=7.5):
    gen_images = []
    paragraphs = read_book(book)
    
    for i, paragraph in enumerate(paragraphs):
        update_percentage((i+1)/len(paragraphs))
        gen_images.append(generate_images(pipe, paragraph, num_samples, guidance_scale, num_inference_steps, height, width).images)
    output = [paragraphs, gen_images]

    return output

calculations = {}

model_path = '/fAIrytale/'

#pipe = load_sd_pipe(model_path, 'cpu')

app = FastAPI(title='Welcome to fAIrytale public API')


@app.get('/user-exists')
async def check_user(userId):
    return {'exists': userId in calculations}

@app.post('/generate')
async def create_new_calculation(userId, inputText):
    global calculations
    calculations[userId] = {'progress': 0, 'images': []}
    time.sleep(10)
    #output = book_to_images(inputText, update_percentage=lambda x: set_calculation_percentage(userId, x))
    #calculations[userId]['images'] = output
    calculations[userId]['images'] = [1,2,3,4,5]
    calculations[userId]['progress'] = 1

@app.get('/progress')
async def check_progress(userId):
    if userId in calculations:
        return {'progress': calculations[userId]['progress']}
    return {'progress': -1}

@app.get('/images')
async def get_images_generated(userId):
    if userId in calculations and calculations[userId]['progress'] == 1:
        return {'images': calculations[userId]['images']}
    return {'images': -1}


# To start the API application (on command line)
# !uvicorn main:app --reload