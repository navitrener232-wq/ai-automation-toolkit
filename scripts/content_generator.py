#!/usr/bin/env python3
"""
Content Generator - Generate blog posts, social media content, product descriptions
Usage: python content_generator.py --type blog --topic "AI in Healthcare" --length 500
"""

import os
import sys
import argparse
from openai import OpenAI

CONTENT_TYPES = {
    'blog': 'Write a comprehensive blog post about',
    'social': 'Create engaging social media posts (Twitter, LinkedIn, Facebook) about',
    'product': 'Write a compelling product description for',
    'email': 'Write a professional email marketing campaign about',
    'ad': 'Create persuasive ad copy for'
}

def generate_content(content_type, topic, length=500, tone='professional', api_key=None):
    """Generate content using OpenAI API"""
    if not api_key:
        api_key = os.getenv('OPENAI_API_KEY')

    if not api_key:
        print("❌ Error: OPENAI_API_KEY not found")
        sys.exit(1)

    if content_type not in CONTENT_TYPES:
        print(f"❌ Error: Invalid content type. Choose from: {', '.join(CONTENT_TYPES.keys())}")
        sys.exit(1)

    client = OpenAI(api_key=api_key)

    prompt = f"{CONTENT_TYPES[content_type]} '{topic}'. Tone: {tone}. Length: approximately {length} words."

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"You are a professional content writer. Create {tone} content that engages readers."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=int(length * 1.5),
            temperature=0.7
        )

        content = response.choices[0].message.content
        return content

    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Generate various types of content using AI')
    parser.add_argument('--type', type=str, required=True,
                       help=f"Content type: {', '.join(CONTENT_TYPES.keys())}")
    parser.add_argument('--topic', type=str, required=True, help='Topic or subject')
    parser.add_argument('--length', type=int, default=500, help='Approximate word count (default: 500)')
    parser.add_argument('--tone', type=str, default='professional',
                       help='Tone: professional, casual, enthusiastic, formal (default: professional)')
    parser.add_argument('--output', type=str, help='Save to file (optional)')
    parser.add_argument('--api-key', type=str, help='OpenAI API key')

    args = parser.parse_args()

    print(f"🔄 Generating {args.type} content about '{args.topic}'...")
    content = generate_content(args.type, args.topic, args.length, args.tone, args.api_key)

    print("\n" + "="*60)
    print(f"✨ GENERATED {args.type.upper()} CONTENT")
    print("="*60)
    print(content)
    print("="*60 + "\n")

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"💾 Content saved to: {args.output}")

if __name__ == "__main__":
    main()
