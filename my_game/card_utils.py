import requests
import pygame
import os
import random


# Load card image
def load_card_image(card, size=(90, 102)):
    # Get cache path
    card_id = card["id"]
    cache_path = f"cache/{card_id}.png"

    # Download image
    if not os.path.exists(cache_path):
        os.makedirs("cache", exist_ok=True)

        try:
            # Fetch image
            img_response = requests.get(card["images"]["large"], timeout=10)
            img_response.raise_for_status()

            # Save image
            with open(cache_path, "wb") as f:
                f.write(img_response.content)

        except requests.exceptions.RequestException:
            # Use placeholder
            placeholder = pygame.Surface(size)
            placeholder.fill((80, 80, 80))
            return placeholder

    # Scale image
    img = pygame.image.load(cache_path)
    return pygame.transform.smoothscale(img, size)


# Load preview image
def load_large_image(card):
    return load_card_image(card, size=(250, 350))


# Fetch cards
def fetch_cards(limit=60):
    # Card storage
    collected = []
    seen_ids = set()

    # Try enough times
    max_attempts = max(30, limit * 3)

    for _ in range(max_attempts):
        # Stop when full
        if len(collected) >= limit:
            break

        # Pick random page
        total_pages = max(1, 20359 // 20)
        page = random.randint(1, total_pages)

        try:
            # Fetch cards
            response = requests.get(
                "https://api.pokemontcg.io/v2/cards",
                params={"page": page, "pageSize": 20},
                timeout=10,
            )
        except requests.exceptions.RequestException:
            continue

        # Check response
        if response.status_code != 200:
            continue

        try:
            # Read data
            data = response.json()["data"]
        except (ValueError, KeyError):
            continue

        # Collect cards
        for c in data:
            if c.get("attacks") and c["id"] not in seen_ids:
                seen_ids.add(c["id"])
                collected.append(c)

    # Shuffle cards
    random.shuffle(collected)

    # Return cards
    return collected[:limit]