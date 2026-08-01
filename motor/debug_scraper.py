"""Debug script to inspect Amazon HTML structure."""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode

# Configuration
BASE_URL = "https://www.amazon.es"
SEARCH_TERM = "freidoras de aire"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'es-ES,es;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
    'DNT': '1',
    'Connection': 'keep-alive',
}

# Make request
params = {'k': SEARCH_TERM}
search_url = f"{BASE_URL}/s?{urlencode(params)}"

print(f"🔍 Buscando en: {search_url}\n")

try:
    response = requests.get(search_url, headers=HEADERS, timeout=10)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Save HTML for inspection
    with open('amazon_response.html', 'w', encoding='utf-8') as f:
        f.write(soup.prettify())
    
    print("✓ HTML guardado en amazon_response.html\n")
    
    # Try different selectors
    print("📊 Probando selectores CSS:\n")
    
    # Old selector
    old_selector = soup.find_all('div', {'data-component-type': 's-search-result'})
    print(f"1. data-component-type='s-search-result': {len(old_selector)} resultados")
    
    # New selectors to try
    new_selectors = [
        ('div[data-component-type="s-search-result"]', lambda s: s.find_all('div', {'data-component-type': 's-search-result'})),
        ('h2 a', lambda s: s.find_all('h2')),
        ('[data-asin]', lambda s: s.find_all(attrs={'data-asin': True})),
        ('span[data-a-price-whole]', lambda s: s.find_all('span', {'data-a-price-whole': True})),
        ('.s-result-item', lambda s: s.find_all(class_='s-result-item')),
        ('[data-component-type="s-search-result"]', lambda s: s.find_all(attrs={'data-component-type': 's-search-result'})),
    ]
    
    for selector, func in new_selectors:
        results = func(soup)
        print(f"{selector}: {len(results)} resultados")
    
    # Print first few product containers found
    products = soup.find_all('div', {'data-component-type': 's-search-result'})
    if products:
        print(f"\n✓ Se encontraron {len(products)} contenedores\n")
        print("Estructura del primer producto:")
        print(products[0].prettify()[:500] if products else "No products found")
    else:
        # Check for alternative structure
        print("\n⚠ No se encontraron con selector antiguo, buscando alternativas...")
        divs = soup.find_all('div', class_='s-result-item')
        print(f"Encontrados con .s-result-item: {len(divs)}")
        
        if divs:
            print("\nPrimer resultado con .s-result-item:")
            print(divs[0].prettify()[:500])
    
except Exception as e:
    print(f"✗ Error: {e}")
