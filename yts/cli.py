import argparse
import requests
import re
import sys
from bs4 import BeautifulSoup
from rich.console import Console

console = Console(force_terminal=True)

STATUS_URL = "https://yifystatus.com/"
API_PATH = "/api/v2/list_movies.json"

# List of trackers for building the magnet link.
TRACKERS = [
    "udp://open.demonii.com:1337/announce",
    "udp://tracker.openbittorrent.com:80",
    "udp://tracker.coppersurfer.tk:6969",
    "udp://glotorrents.pw:6969/announce",
    "udp://tracker.opentrackr.org:1337/announce",
    "udp://torrent.gresille.org:80/announce",
    "udp://p4p.arenabg.com:1337",
    "udp://tracker.leechers-paradise.org:6969"
]


def fetch_official_domain():
    """Fetch the current official domain from the status page."""
    try:
        resp = requests.get(STATUS_URL, timeout=10)
        resp.raise_for_status()
    except requests.RequestException:
        return None

    html = resp.text
    # Look for the line that says 'Current official domain: <domain>'
    match = re.search(r"Current official domain:\s*([A-Za-z0-9\.-]+)", html)
    if match:
        return match.group(1).lower()

    # Fallback: try to parse list if above fails
    soup = BeautifulSoup(html, "html.parser")
    text = soup.get_text()
    match = re.search(r"Current official domain:\s*([A-Za-z0-9\.-]+)", text)
    if match:
        return match.group(1).lower()

    return None


def get_api_url():
    domain = fetch_official_domain()
    if not domain:
        console.print("[yellow]Warning:[/yellow] Could not get official domain, falling back to yts.lt")
        domain = "yts.lt"
    return f"https://{domain}{API_PATH}"


def build_magnet(torrent_hash, name):
    tracker_params = "&".join(f"tr={t}" for t in TRACKERS)
    return f"magnet:?xt=urn:btih:{torrent_hash}&dn={name}&{tracker_params}"


def search_movies(query):
    url = get_api_url()
    params = {"query_term": query, "limit": 10}
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()
    data = response.json()
    return data.get("data", {}).get("movies", [])


def display_movies(movies):
    for movie in movies:
        movie_id = movie.get("id")
        title = movie.get("title")
        year = movie.get("year")
        rating = movie.get("rating")
        torrents = movie.get("torrents", [])

        info_line = (f"[bold magenta][{movie_id}] {title} ({year})[/bold magenta] - "
                     f"[green]{rating}/10[/green]")
        console.print(info_line)

        printed = set()
        for torrent in torrents:
            quality = torrent.get("quality")
            type_tag = torrent.get("type", "")
            label = f"{quality} {type_tag}".strip()
            if label not in printed:
                magnet = build_magnet(torrent.get("hash"), f"{title} ({year})")
                console.print(f"[italic yellow]{label}:[/italic yellow]")
                console.print(f"[cyan]{magnet}[/cyan]\n")
                printed.add(label)


def main():
    parser = argparse.ArgumentParser(
        description=None,
        add_help=False,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--query", help="Search for a movie")

    args = parser.parse_args()

    if args.query:
        try:
            movies = search_movies(args.query)
            if not movies:
                console.print("[red]No results found.[/red]")
            else:
                display_movies(movies)
        except requests.exceptions.RequestException as e:
            console.print(f"[bold red]An error occurred: {e}[/bold red]")
    else:
        console.print("[bold cyan]YTS Magnet Link Fetcher[/bold cyan]")
        console.print("Search and display magnet links for movies from YTS.\n")
        console.print("[bold]Usage:[/bold]")
        console.print('  python yts.py --query "Mad Max"\n')
        console.print("[bold]Options:[/bold]")
        console.print("  --query QUERY    Search for a movie")
        sys.stdout.flush()


if __name__ == "__main__":
    main()


