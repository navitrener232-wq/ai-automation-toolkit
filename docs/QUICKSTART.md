# 📖 Quick Start Guide

## Installation

1. **Clone the repository:**
```bash
git clone https://github.com/navitrener232-wq/ai-automation-toolkit.git
cd ai-automation-toolkit
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set your OpenAI API key:**
```bash
# Windows PowerShell
$env:OPENAI_API_KEY="sk-your-key-here"

# Linux/Mac
export OPENAI_API_KEY="sk-your-key-here"
```

## Script Examples

### 1. Email Summarizer
Summarize long emails quickly:
```bash
python scripts/email_summarizer.py --file my_email.txt
```

### 2. Content Generator
Generate blog posts:
```bash
python scripts/content_generator.py --type blog --topic "AI in Marketing" --length 800
```

Generate social media posts:
```bash
python scripts/content_generator.py --type social --topic "Product Launch" --tone enthusiastic
```

### 3. YouTube Transcript Downloader
Download video transcripts:
```bash
python scripts/youtube_transcript.py --url "https://youtube.com/watch?v=dQw4w9WgXcQ" --output transcript.txt
```

### 4. Web Scraper with AI
Extract structured data from websites:
```bash
python scripts/web_scraper.py --url "https://example.com/products" --extract "product names, prices, ratings" --output data.json
```

## Pro Tips

- **Save API costs:** Use `gpt-3.5-turbo` (default) for most tasks
- **Batch processing:** Create shell scripts to process multiple files
- **Custom prompts:** Modify the system prompts in each script for your use case
- **Error handling:** All scripts have built-in error handling and helpful messages

## Troubleshooting

**Error: OPENAI_API_KEY not found**
- Make sure you've set the environment variable
- Check spelling and format

**Error: Module not found**
- Run `pip install -r requirements.txt` again
- Use a virtual environment: `python -m venv venv`

**Rate limit errors**
- Add delays between API calls
- Upgrade your OpenAI plan

## Support

Need help? Email: navitrener232@gmail.com

## Updates

This toolkit receives lifetime updates. Re-download to get new scripts and features.
