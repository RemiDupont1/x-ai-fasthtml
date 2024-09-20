import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import re

def download_image(query, num_images=1):
    # Rechercher des images sur Google
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    search_url = f"https://www.google.com/search?hl=en&tbm=isch&q={query}"
    response = requests.get(search_url, headers=headers)
    response.raise_for_status()

    # Analyser la page de résultats
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Utiliser une expression régulière pour extraire les URLs des images
    image_urls = re.findall(r'https://encrypted-tbn0\.gstatic\.com/images\?q=.*?(?=")', response.text)
    
    # Télécharge les images
    for i, url in enumerate(image_urls[:num_images]):
        img_response = requests.get(url)
        img_response.raise_for_status()

        # Ouvrir l'image avec PIL et l'enregistrer
        img = Image.open(BytesIO(img_response.content))
        img.save(f'image_{i+1}.jpg')
        print(f'Downloaded image_{i+1}.jpg')

if __name__ == "__main__":
    query = 'puppies'  # Remplacez cela par votre requête de recherche
    download_image(query, num_images=3)  # Télécharge les 3 premières images
