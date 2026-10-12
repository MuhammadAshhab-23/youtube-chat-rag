
from urllib.parse import urlparse, parse_qs

from youtube_transcript_api import YouTubeTranscriptApi


def extract_video_id(url):
    parsed_url = urlparse(url)
    hostname = parsed_url.hostname

    if hostname in ("youtu.be", "www.youtu.be"):
        return parsed_url.path.strip("/")

    if hostname in (
        "youtube.com",
        "www.youtube.com",
        "m.youtube.com",
    ):
        return parse_qs(parsed_url.query).get("v", [None])[0]

    raise ValueError("Invalid YouTube URL")


def fetch_transcript(url):
    video_id = extract_video_id(url)

    api = YouTubeTranscriptApi()
    transcript = api.fetch(video_id, languages=["en"])

    return " ".join(
        snippet.text for snippet in transcript.snippets
    )
