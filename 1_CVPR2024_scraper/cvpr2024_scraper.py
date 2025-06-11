import requests
from bs4 import BeautifulSoup
import csv
import json

# Base URL for CVPR 2024 open access papers
BASE_URL = "https://openaccess.thecvf.com"
URL = f"{BASE_URL}/CVPR2024?day=all"

def scrape_cvpr2024():
    """
    Scrapes the CVPR 2024 open access website to extract:
    - Paper title
    - Author list
    - PDF link
    - Supplementary material link
    - arXiv link (if any)

    Returns:
        List of dictionaries, each representing one paper.
    """
    # Fetch the HTML content from the CVPR 2024 website
    response = requests.get(URL)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    # List to hold all extracted paper entries
    papers = []

    # The main list of papers is wrapped in a <dl> tag
    dl = soup.find('dl')
    if not dl:
        raise ValueError("Could not find <dl> element containing papers.")

    # All entries are either <dt> (title) or <dd> (authors and links)
    entries = dl.find_all(['dt', 'dd'])

    # Temporary variables for holding the current paper's data
    current_title = None
    current_authors = []
    current_links = {'pdf': '', 'supp': '', 'arXiv': ''}

    # Iterate over each entry (alternating between <dt> and <dd>)
    for tag in entries:
        if tag.name == 'dt' and 'ptitle' in tag.get('class', []):
            # Save the previous paper's data before moving to the next
            if current_title:
                papers.append({
                    "Title": current_title,
                    "Authors": ', '.join(current_authors),
                    "pdf": current_links['pdf'],
                    "supp": current_links['supp'],
                    "arXiv": current_links['arXiv']
                })

            # Extract new paper title
            a_tag = tag.find('a')
            current_title = a_tag.text.strip()
            current_authors = []
            current_links = {'pdf': '', 'supp': '', 'arXiv': ''}

        elif tag.name == 'dd':
            # Check if it's the author section (contains multiple <form> tags)
            forms = tag.find_all('form')
            if forms:
                current_authors = [form.find('a').text.strip() for form in forms]
            else:
                # This section contains links like [pdf], [supp], [arXiv]
                links = tag.find_all('a')
                for a in links:
                    text = a.text.strip().lower()
                    href = a.get('href', '')
                    full_link = BASE_URL + href if href.startswith('/') else href

                    if text == 'pdf':
                        current_links['pdf'] = full_link
                    elif text == 'supp':
                        current_links['supp'] = full_link
                    elif 'arxiv' in full_link:
                        current_links['arXiv'] = full_link

    # Add the last paper entry to the list
    if current_title:
        papers.append({
            "Title": current_title,
            "Authors": ', '.join(current_authors),
            "pdf": current_links['pdf'],
            "supp": current_links['supp'],
            "arXiv": current_links['arXiv']
        })

    return papers

def save_to_csv(data, filename):
    """
    Saves a list of dictionaries to a CSV file.

    Args:
        data: List of dictionaries representing paper entries.
        filename: Filename for the output CSV file.
    """
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["Title", "Authors", "pdf", "supp", "arXiv"])
        writer.writeheader()
        for entry in data:
            writer.writerow(entry)

def save_to_json(data, filename):
    """
    Saves a list of dictionaries to a JSON file.

    Args:
        data: List of dictionaries representing paper entries.
        filename: Filename for the output JSON file.
    """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    # Step 1: Scrape data from the CVPR 2024 website
    papers = scrape_cvpr2024()

    # Step 2: Save to CSV
    save_to_csv(papers, 'cvpr2024_papers.csv')

    # Step 3: Save to JSON
    save_to_json(papers, 'cvpr2024_papers.json')

    # Final status update
    print(f"✅ Extracted {len(papers)} papers. Files saved as 'cvpr2024_papers.csv' and 'cvpr2024_papers.json'.")

