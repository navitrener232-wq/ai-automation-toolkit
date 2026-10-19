#!/usr/bin/env python3
"""
Web Scraper with AI - Scrape websites and extract structured data intelligently
Usage: python web_scraper.py --url "https://example.com" --extract "prices, titles"
"""

import sys
import argparse
import requests
from bs4 import BeautifulSoup
from openai import OpenAI
import os
import json

def scrape_website(url):
    """Scrape website content"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()

        text = soup.get_text()
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = '\n'.join(chunk for chunk in chunks if chunk)

        return text[:4000]  # Limit to 4000 chars

    except Exception as e:
        print(f"❌ Error scraping website: {e}")
        sys.exit(1)

def extract_data(content, extract_fields, api_key=None):
    """Use AI to extract structured data from scraped content"""
    if not api_key:
        api_key = os.getenv('OPENAI_API_KEY')

    if not api_key:
        print("❌ Error: OPENAI_API_KEY not found")
        sys.exit(1)

    client = OpenAI(api_key=api_key)

    prompt = f"""Extract the following information from this website content: {extract_fields}

Return the data as a JSON object.

Content:
{content}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a data extraction assistant. Extract requested information and return it as valid JSON."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.3
        )

        result = response.choices[0].message.content
        return result

    except Exception as e:
        print(f"❌ Error extracting data: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Scrape websites and extract structured data using AI')
    parser.add_argument('--url', type=str, required=True, help='Website URL to scrape')
    parser.add_argument('--extract', type=str, required=True,
                       help='Fields to extract (e.g., "product names, prices, descriptions")')
    parser.add_argument('--output', type=str, help='Save to JSON file (optional)')
    parser.add_argument('--api-key', type=str, help='OpenAI API key')

    args = parser.parse_args()

    print(f"🔄 Scraping {args.url}...")
    content = scrape_website(args.url)

    print(f"🔄 Extracting data: {args.extract}...")
    extracted = extract_data(content, args.extract, args.api_key)

    print("\n" + "="*60)
    print("📊 EXTRACTED DATA")
    print("="*60)
    print(extracted)
    print("="*60 + "\n")

    if args.output:
        try:
            data = json.loads(extracted)
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"💾 Data saved to: {args.output}")
        except:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(extracted)
            print(f"💾 Data saved to: {args.output}")

if __name__ == "__main__":
    main()
