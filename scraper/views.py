import requests
from bs4 import BeautifulSoup
from django.shortcuts import render
from django.http import JsonResponse

def index(request):
    query = request.GET.get('query', '')
    url = request.GET.get('url', '')
    results = []

    if query and url:
        try:
            # Make a request with headers to avoid being blocked
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, params={'q': query}, headers=headers)
            response.raise_for_status()  # Raise an error for HTTP failures

            # Parse HTML content
            soup = BeautifulSoup(response.content, 'html.parser')

            # Scrape different elements
            titles = scrape_titles(soup)
            links = scrape_links(soup, url)
            images = scrape_images(soup)
            descriptions = scrape_descriptions(soup)

            # Combine the scraped data
            for i in range(min(len(titles), len(links))):
                results.append({
                    'title': titles[i],
                    'link': links[i],
                    'image': images[i] if i < len(images) else None,
                    'description': descriptions[i] if i < len(descriptions) else None,
                })

        except requests.exceptions.RequestException as e:
            return render(request, 'index.html', {'error': f"Error fetching data: {str(e)}", 'results': []})

    return render(request, 'index.html', {'results': results, 'query': query, 'url': url})


def scrape_titles(soup):
    titles = []
    for item in soup.find_all('div', class_='result'):  # Adjust this to match the target website
        title_tag = item.find('h3')
        if title_tag:
            titles.append(title_tag.get_text(strip=True))
    return titles


def scrape_links(soup, base_url):
    links = []
    for item in soup.find_all('div', class_='result'):
        link_tag = item.find('a', href=True)
        if link_tag:
            link = link_tag['href']
            if link.startswith('/'):  # Convert relative URLs to absolute
                link = base_url.rstrip('/') + link
            links.append(link)
    return links


def scrape_images(soup):
    images = []
    for item in soup.find_all('div', class_='result'):
        image_tag = item.find('img')
        if image_tag and 'src' in image_tag.attrs:
            images.append(image_tag['src'])
    return images


def scrape_descriptions(soup):
    descriptions = []
    for item in soup.find_all('div', class_='result'):
        description_tag = item.find('p')
        if description_tag:
            descriptions.append(description_tag.get_text(strip=True))
    return descriptions


def api_scraper(request):
    """API endpoint to return JSON results from web scraping."""
    query = request.GET.get('query', '')
    url = request.GET.get('url', '')
    results = []

    if query and url:
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, params={'q': query}, headers=headers)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')
            titles = scrape_titles(soup)
            links = scrape_links(soup, url)
            images = scrape_images(soup)
            descriptions = scrape_descriptions(soup)

            for i in range(min(len(titles), len(links))):
                results.append({
                    'title': titles[i],
                    'link': links[i],
                    'image': images[i] if i < len(images) else None,
                    'description': descriptions[i] if i < len(descriptions) else None,
                })

        except requests.exceptions.RequestException as e:
            return JsonResponse({'error': str(e), 'results': []}, status=400)

    return JsonResponse({'results': results}, safe=False)


# Function for cURL test
def curl_test(request):
    return JsonResponse({'message': 'Use cURL with this endpoint'}, safe=False)