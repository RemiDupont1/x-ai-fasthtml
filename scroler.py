from selenium import webdriver
from selenium.webdriver.firefox.options import Options

def scroll_html_file(file_path):
    options = Options()
    options.add_argument("--headless")
    browser = webdriver.Firefox(options=options)
    browser.get(file_path)
    # Sauvegarder le contenu de la page dans un fichier HTML
    source = browser.page_source
    visible_text = browser.find_element_by_tag_name('body').get_attribute('textContent')

    with open('document.html', 'w', encoding='utf-8') as f:
        f.write(source)

    # Sauvegarder le texte visible dans un fichier texte
    with open('page_text.txt', 'w', encoding='utf-8') as f:
        f.write(visible_text)

    # Filtrer et sauvegarder le texte visible dans un nouveau fichier
    filtered_lines = [line.strip() for line in visible_text.split('\n') if line.strip()]
    filtered_text = '\n'.join(line[:10000] for line in filtered_lines)

    with open('visible_text_filtered.txt', 'w', encoding='utf-8') as f:
        f.write(filtered_text)

    print("Le texte visible filtré a été sauvegardé dans visible_text_filtered.txt")
    browser.quit()
    return filtered_text

