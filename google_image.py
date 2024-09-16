import requests
from bs4 import BeautifulSoup
import os

def telecharger_image_album(titre_album):
    # Formater la requête de recherche
    query = titre_album.replace(' ', '+')
    url = f"https://www.bing.com/images/search?q={query}&qft=+filterui:imagesize-large"
    
    # Envoyer la requête à Bing Images
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    
    # Analyser le HTML de la page de résultats
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Trouver le premier lien d'image
    img_tag = soup.find('a', class_='iusc')
    if img_tag and 'm' in img_tag.attrs:
        img_data = img_tag['m']
        img_url = img_data.split('"murl":"')[1].split('"')[0]
    else:
        print("Aucune image trouvée.")
        return
    
    # Télécharger l'image
    img_data = requests.get(img_url).content
    
    # Sauvegarder l'image
    nom_fichier = f"data/images/{titre_album.replace(' ', '_')}.jpg"
    os.makedirs(os.path.dirname(nom_fichier), exist_ok=True)
    with open(nom_fichier, 'wb') as handler:
        handler.write(img_data)
    
    print(f"Image téléchargée et sauvegardée sous le nom : {nom_fichier}")
    return nom_fichier
