# YTS Magnet Link Fetcher

A command-line tool to search for movies on [YTS](https://yts.mx) and fetch magnet links for available torrents.

## Features

-  Search for movies using the YTS API
-  Display available torrents with quality labels
-  Generate full magnet links with tracker support


## Usage

```bash
python yts.py --query "name of movie"
```
## Example
```
python yts.py --query "Mad Max"
```
Results
```YAML
[44321] Mad Max: Fury Road (2015) - 8.1/10
  720p:
    magnet:?xt=urn:btih:...&dn=Mad Max...&tr=...

  1080p:
    magnet:?xt=urn:btih:...&dn=Mad Max...&tr=...
```
## Requirements and Dependencies:
Python 3.7+
```
pip install rich
```
## Limitations
- Returns a maximum of 10 results per query

## Legal Disclaimer
This tool  does not host or distribute copyrighted content. Accessing or downloading copyrighted materials without proper authorization may violate copyright laws in your country.

By using this tool, you agree that:
- You are solely responsible for complying with all applicable local, national, and international laws.
- The author assumes no liability for misuse or unlawful use of this tool.
- This project is not affiliated with or endorsed by YTS, YIFY, or any related entities.
