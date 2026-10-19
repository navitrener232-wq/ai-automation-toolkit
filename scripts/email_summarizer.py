#!/usr/bin/env python3
"""
Email Summarizer - Automatically summarize long emails using AI
Usage: python email_summarizer.py --email "your email content" or --file email.txt
"""

import os
import sys
import argparse
from openai import OpenAI

def summarize_email(email_content, api_key=None):
    """Summarize email content using OpenAI API"""
    if not api_key:
        api_key = os.getenv('OPENAI_API_KEY')

    if not api_key:
        print("❌ Error: OPENAI_API_KEY not found. Set it with: export OPENAI_API_KEY='your-key'")
        sys.exit(1)

    client = OpenAI(api_key=api_key)

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional email assistant. Summarize emails concisely, highlighting key points, action items, and deadlines."},
                {"role": "user", "content": f"Summarize this email:\n\n{email_content}"}
            ],
            max_tokens=300,
            temperature=0.5
        )

        summary = response.choices[0].message.content
        return summary

    except Exception as e:
        print(f"❌ Error during summarization: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Summarize emails using AI')
    parser.add_argument('--email', type=str, help='Email content as string')
    parser.add_argument('--file', type=str, help='Path to email text file')
    parser.add_argument('--api-key', type=str, help='OpenAI API key (optional, uses env var by default)')

    args = parser.parse_args()

    # Get email content
    if args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                email_content = f.read()
        except FileNotFoundError:
            print(f"❌ Error: File '{args.file}' not found")
            sys.exit(1)
    elif args.email:
        email_content = args.email
    else:
        print("❌ Error: Provide either --email or --file argument")
        parser.print_help()
        sys.exit(1)

    print("🔄 Summarizing email...")
    summary = summarize_email(email_content, args.api_key)

    print("\n" + "="*50)
    print("📧 EMAIL SUMMARY")
    print("="*50)
    print(summary)
    print("="*50 + "\n")

if __name__ == "__main__":
    main()
