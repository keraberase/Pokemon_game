import requests
import pygame
from PIL import Image
from io import BytesIO
import os

def load_card_image(card, size=(90, 102)):
    card_id = card["id"]
    cache_path = f"cache/{card_id}.png"
    if os.path.exists(cache_path):
        img = Image.open(cache_path)
    else:
        os.makedirs("cache", exist_ok=True)
        img_response = requests.get(card["images"]["large"])
        img = Image.open(BytesIO(img_response.content))
        img.save(cache_path)
    img = img.resize(size)
    img_bytes = BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    return pygame.image.load(img_bytes)

def load_large_image(card):
    return load_card_image(card, size=(250, 350))