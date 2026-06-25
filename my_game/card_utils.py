import requests
import pygame
import os
import random

def load_card_image(card, size=(90, 102)):
    card_id = card["id"]
    cache_path = f"cache/{card_id}.png"
    if not os.path.exists(cache_path):
        os.makedirs("cache", exist_ok=True)
        img_response = requests.get(card["images"]["large"])
        with open(cache_path, "wb") as f:
            f.write(img_response.content)
    img = pygame.image.load(cache_path)
    return pygame.transform.smoothscale(img, size)

def load_large_image(card):
    return load_card_image(card, size=(250, 350))

def fetch_cards(limit=10):
    page = random.randint(1, 400)
    response = requests.get("https://api.pokemontcg.io/v2/cards", params={"page": page,"pageSize": limit})
    if response.status_code != 200:
        raise RuntimeError(f"Error API: {response.status_code}")
    return response.json()["data"]