#!/usr/bin/env python3
"""
YouTube Transcript Downloader - Download and format YouTube video transcripts
Usage: python youtube_transcript.py --url "https://youtube.com/watch?v=..."
"""

import sys
import argparse
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs

def get_video_id(url):
    """Extract video ID from YouTube URL"""
    parsed = urlparse(url)
    if parsed.hostname in ['www.youtube.com', 'youtube.com']:
        if parsed.path == '/watch':
            return parse_qs(parsed.query)['v'][0]
    elif parsed.hostname == 'youtu.be':
        return parsed.path[1:]
    return None

def download_transcript(video_url, language='en', format_type='text'):
    """Download transcript from YouTube video"""
    video_id = get_video_id(video_url)

    if not video_id:
        print("❌ Error: Invalid YouTube URL")
        sys.exit(1)

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[language])

        if format_type == 'text':
            result = '\n'.join([item['text'] for item in transcript])
        elif format_type == 'srt':
            result = format_as_srt(transcript)
        elif format_type == 'json':
            import json
            result = json.dumps(transcript, indent=2)
        else:
            result = str(transcript)

        return result

    except Exception as e:
        print(f"❌ Error downloading transcript: {e}")
        sys.exit(1)

def format_as_srt(transcript):
    """Format transcript as SRT subtitles"""
    srt = []
    for i, item in enumerate(transcript, 1):
        start = format_timestamp(item['start'])
        end = format_timestamp(item['start'] + item['duration'])
        srt.append(f"{i}\n{start} --> {end}\n{item['text']}\n")
    return '\n'.join(srt)

def format_timestamp(seconds):
    """Convert seconds to SRT timestamp format"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

def main():
    parser = argparse.ArgumentParser(description='Download YouTube video transcripts')
    parser.add_argument('--url', type=str, required=True, help='YouTube video URL')
    parser.add_argument('--language', type=str, default='en', help='Language code (default: en)')
    parser.add_argument('--format', type=str, default='text',
                       choices=['text', 'srt', 'json'], help='Output format')
    parser.add_argument('--output', type=str, help='Save to file (optional)')

    args = parser.parse_args()

    print(f"🔄 Downloading transcript from YouTube...")
    transcript = download_transcript(args.url, args.language, args.format)

    print("\n" + "="*60)
    print("📺 YOUTUBE TRANSCRIPT")
    print("="*60)
    print(transcript[:500] + "..." if len(transcript) > 500 else transcript)
    print("="*60 + "\n")

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(transcript)
        print(f"💾 Transcript saved to: {args.output}")
    else:
        print(f"💡 Use --output filename.txt to save the full transcript")

if __name__ == "__main__":
    main()
