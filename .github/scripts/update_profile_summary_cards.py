from pathlib import Path
import re
import urllib.request


OUTPUT_DIR = Path("image/profile-summary-cards")
TITLE_COLOR = "#000000"

CARDS = {
    "repos-per-language.svg": (
        "https://github-profile-summary-cards.vercel.app/api/cards/"
        "repos-per-language?username=yukito0209&theme=transparent"
    ),
    "most-commit-language.svg": (
        "https://github-profile-summary-cards.vercel.app/api/cards/"
        "most-commit-language?username=yukito0209&theme=transparent"
    ),
    "productive-time.svg": (
        "https://github-profile-summary-cards.vercel.app/api/cards/"
        "productive-time?username=yukito0209&utcOffset=8&theme=transparent"
    ),
}

TITLE_RE = re.compile(
    r'(<text x="30" y="40" style="font-size: 22px; fill: )[^;"]+(;">)'
)


def fetch_svg(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": "yukito0209-profile-readme"})
    with urllib.request.urlopen(request, timeout=30) as response:
        content_type = response.headers.get("content-type", "")
        if response.status != 200 or "image/svg+xml" not in content_type:
            raise RuntimeError(f"Unexpected response for {url}: {response.status} {content_type}")
        return response.read().decode("utf-8")


def set_title_color(svg: str) -> str:
    updated, count = TITLE_RE.subn(rf"\1{TITLE_COLOR}\2", svg, count=1)
    if count != 1:
        raise RuntimeError("Could not find the summary card title text")
    return updated


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for filename, url in CARDS.items():
        svg = set_title_color(fetch_svg(url))
        (OUTPUT_DIR / filename).write_text(svg, encoding="utf-8")


if __name__ == "__main__":
    main()
