"""
Final Project: Open Library Book Rankings Tracker
_________________________________________________
Tracks the top 150 most-read books by genre using the Open Library Search API.

Ranking metric: readinglog_count — the total number of Open Library users
who have added the book to their reading log (want to read + currently reading
+ already read). This is the best available popularity signal in the API.

Each run prompts for a genre, fetches the top 150 books sorted by reading log
count, then appends them to book_rankings.csv below two blank separator rows.
Analysis runs across every genre block stored in the file.

API Documentation: https://openlibrary.org/developers/api
"""

import requests
import csv
import json
import os
from datetime import datetime


# Configuration

BASE_URL  = "https://openlibrary.org/search.json"
DATA_DIR  = os.path.dirname(os.path.abspath(__file__))
CSV_FILE  = os.path.join(DATA_DIR, "book_rankings.csv")
JSON_FILE = os.path.join(DATA_DIR, "results.json")
FETCH_LIMIT = 150

CSV_HEADERS = [
    "rank", "title", "author",
    "first_publish_year", "readinglog_count",
    "want_to_read_count", "already_read_count",
    "ratings_average", "ratings_count",
    "genre", "date_fetched"
]


# BookEntry Class

class BookEntry:
    """One ranked book result from a single genre fetch."""

    def __init__(self, rank, title, author, first_publish_year,
                 readinglog_count, want_to_read_count, already_read_count,
                 ratings_average, ratings_count, genre, date_fetched=None):
        self.rank               = rank
        self.title              = title
        self.author             = author
        self.first_publish_year = first_publish_year  # int or None
        self.readinglog_count   = readinglog_count    # int — main ranking metric
        self.want_to_read_count = want_to_read_count  # int
        self.already_read_count = already_read_count  # int
        self.ratings_average    = ratings_average     # float or None
        self.ratings_count      = ratings_count       # int
        self.genre              = genre               # str, normalized
        self.date_fetched       = date_fetched or datetime.today().strftime("%Y-%m-%d")

    def to_row(self):
        """Return ordered list matching CSV_HEADERS for writing."""
        return [
            self.rank,
            self.title,
            self.author,
            self.first_publish_year,
            self.readinglog_count,
            self.want_to_read_count,
            self.already_read_count,
            self.ratings_average,
            self.ratings_count,
            self.genre,
            self.date_fetched,
        ]

    def __repr__(self):
        return (f"BookEntry(#{self.rank} {self.title!r}, "
                f"readinglog={self.readinglog_count}, genre={self.genre!r})")


# ──────────────────────────────────────────────────────────────────────────────
# API Functions
# ──────────────────────────────────────────────────────────────────────────────

def fetch_top_books(genre, limit=150):
    """
    Fetch the top *limit* books for *genre* from the Open Library Search API,
    sorted by readinglog_count (most tracked by readers first).

    Parameters:
        genre (str): Genre/subject to search (e.g. "fantasy", "mystery")
        limit (int): Number of results to fetch

    Returns:
        list[BookEntry] sorted by rank (1 = most read)
    """
    params = {
        "subject": genre,
        "sort":    "readinglog",
        "fields":  ("title,author_name,first_publish_year,"
                    "readinglog_count,want_to_read_count,"
                    "already_read_count,ratings_average,ratings_count"),
        "limit":   limit,
    }

    print(f"\n  Fetching top {limit} '{genre}' books from Open Library...")

    try:
        response = requests.get(BASE_URL, params=params, timeout=15)
        response.raise_for_status()
    except requests.exceptions.ConnectionError:
        print("  ERROR: No internet connection.")
        return []
    except requests.exceptions.Timeout:
        print("  ERROR: Request timed out.")
        return []
    except requests.exceptions.HTTPError as e:
        print(f"  ERROR: {e}")
        return []

    docs = response.json().get("docs", [])
    print(f"  API returned {len(docs)} results.")

    entries = []
    for rank, doc in enumerate(docs, start=1):
        title      = doc.get("title", "Unknown Title")
        author     = ", ".join(doc.get("author_name") or ["Unknown Author"])
        year       = doc.get("first_publish_year")
        readinglog = doc.get("readinglog_count", 0)
        want_read  = doc.get("want_to_read_count", 0)
        read       = doc.get("already_read_count", 0)
        avg_rating = doc.get("ratings_average")
        num_ratings= doc.get("ratings_count", 0)

        entries.append(BookEntry(
            rank               = rank,
            title              = title,
            author             = author,
            first_publish_year = year,
            readinglog_count   = readinglog,
            want_to_read_count = want_read,
            already_read_count = read,
            ratings_average    = avg_rating,
            ratings_count      = num_ratings,
            genre              = genre,
        ))

    return entries


# CSV Functions

def append_genre_block(entries, filepath):
    """
    Append a genre block to the CSV file.

    - If the file is new or empty: write the header row first, then the data.
    - If data already exists: write two blank separator rows, then the data.

    Parameters:
        entries (list[BookEntry]): Books to write
        filepath (str): Path to the CSV file
    """
    if not entries:
        print("  Nothing to save.")
        return

    file_is_empty = not os.path.exists(filepath) or os.path.getsize(filepath) == 0

    try:
        with open(filepath, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)

            if file_is_empty:
                # Brand-new file — write the header first
                writer.writerow(CSV_HEADERS)
            else:
                # Separate this block from the previous one with two blank rows
                writer.writerow([])
                writer.writerow([])

            for entry in entries:
                writer.writerow(entry.to_row())

    except PermissionError:
        print(f"  ERROR: Cannot write to {os.path.basename(filepath)}.")
        print("  Close the file in Excel first, then re-run the program.")
        return

    print(f"  Saved {len(entries)} entries to {os.path.basename(filepath)}.")


def load_all_entries(filepath):
    """
    Load every non-blank row from the CSV file as BookEntry objects.
    Blank separator rows are skipped automatically.

    Returns:
        list[BookEntry]
    """
    entries = []
    if not os.path.exists(filepath) or os.path.getsize(filepath) == 0:
        return entries

    try:
        with open(filepath, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Skip blank separator rows (title will be empty)
                if not row.get("title", "").strip():
                    continue

                year = int(row["first_publish_year"]) \
                    if row.get("first_publish_year", "") not in ("", "None") else None
                avg_rating = float(row["ratings_average"]) \
                    if row.get("ratings_average", "") not in ("", "None") else None

                entries.append(BookEntry(
                    rank               = int(row.get("rank", 0) or 0),
                    title              = row["title"],
                    author             = row["author"],
                    first_publish_year = year,
                    readinglog_count   = int(row.get("readinglog_count", 0) or 0),
                    want_to_read_count = int(row.get("want_to_read_count", 0) or 0),
                    already_read_count = int(row.get("already_read_count", 0) or 0),
                    ratings_average    = avg_rating,
                    ratings_count      = int(row.get("ratings_count", 0) or 0),
                    genre              = row["genre"],
                    date_fetched       = row["date_fetched"],
                ))
    except Exception as e:
        print(f"  WARNING: Could not fully read {os.path.basename(filepath)}: {e}")

    return entries


# Analysis Functions

def group_by_genre_and_run(entries):
    """
    Group entries by (genre, date_fetched) so each individual run is separate.
    Returns a dict: {(genre, date): [BookEntry, ...]}
    """
    groups = {}
    for e in entries:
        key = (e.genre, e.date_fetched)
        groups.setdefault(key, []).append(e)
    return groups


def analyze_run(entries):
    """
    Compute statistics for a single genre run.

    Returns:
        dict with metrics for this run
    """
    if not entries:
        return {}

    readinglog_values = [e.readinglog_count for e in entries]
    rated_entries     = [e for e in entries if e.ratings_average is not None]

    top_book = max(entries, key=lambda e: e.readinglog_count)

    return {
        "total_books":            len(entries),
        "top_book":               top_book.title,
        "top_book_author":        top_book.author,
        "top_book_readinglog":    top_book.readinglog_count,
        "max_readinglog":         max(readinglog_values),
        "min_readinglog":         min(readinglog_values),
        "avg_readinglog":         round(sum(readinglog_values) / len(readinglog_values), 1),
        "avg_rating":             round(
                                    sum(e.ratings_average for e in rated_entries) / len(rated_entries), 3
                                  ) if rated_entries else None,
    }


def find_overall_bests(entries):
    """
    Across all loaded entries, find the single most-read book,
    the most popular author (by total readinglog count), and compare genres.

    Returns:
        dict
    """
    if not entries:
        return {}

    # Most-read single book across everything
    top = max(entries, key=lambda e: e.readinglog_count)

    # Author popularity: sum readinglog_count per author
    author_totals = {}
    for e in entries:
        author_totals[e.author] = author_totals.get(e.author, 0) + e.readinglog_count
    top_author = max(author_totals, key=author_totals.get)

    # Genre comparison: average readinglog_count per genre (using most recent run each)
    # Find the most recent date per genre
    latest_date_per_genre = {}
    for e in entries:
        prev = latest_date_per_genre.get(e.genre, "")
        if e.date_fetched > prev:
            latest_date_per_genre[e.genre] = e.date_fetched

    genre_avgs = {}
    for genre, latest_date in latest_date_per_genre.items():
        genre_entries = [e for e in entries
                         if e.genre == genre and e.date_fetched == latest_date]
        if genre_entries:
            vals = [e.readinglog_count for e in genre_entries]
            genre_avgs[genre] = round(sum(vals) / len(vals), 1)

    # Sort genres from highest to lowest average readinglog
    ranked_genres = sorted(genre_avgs.items(), key=lambda x: x[1], reverse=True)

    return {
        "most_read_book":           top.title,
        "most_read_book_author":    top.author,
        "most_read_book_genre":     top.genre,
        "most_read_book_count":     top.readinglog_count,
        "top_author_by_total_reads":top_author,
        "top_author_total_readinglog": author_totals[top_author],
        "genres_ranked_by_avg_popularity": [
            {"genre": g, "avg_readinglog": avg} for g, avg in ranked_genres
        ],
    }


# Results

def save_results(results):
    """Overwrite results.json with the latest analysis (by design — rubric req)."""
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)
    print(f"  Results saved -> {os.path.basename(JSON_FILE)}")


# Main

def main():
    print("=" * 60)
    print("  Open Library Book Rankings Tracker")
    print(f"  {datetime.today().strftime('%Y-%m-%d')}")
    print("=" * 60)

    # -- 1. Ask for genre
    print("\nAvailable genres:")
    genres = [
        "fantasy",          "mystery",          "romance",
        "science fiction",  "horror",           "thriller",
        "historical fiction","adventure",        "classics",
        "young adult",      "children",         "biography",
        "self help",        "psychology",       "philosophy",
        "history",          "science",          "technology",
        "poetry",           "drama",            "crime",
        "humor",            "cooking",          "travel",
        "art",              "music",            "sports",
        "religion",         "politics",         "western",
    ]
    # Print in 3 columns
    col_width = 22
    for i in range(0, len(genres), 3):
        row = genres[i:i+3]
        print("  " + "".join(g.ljust(col_width) for g in row))

    print()
    raw_genre = input("Enter a genre from the list above (or type your own): ").strip()
    if not raw_genre:
        print("No genre entered. Exiting.")
        return

    # Normalize: lowercase, spaces become underscores for the API subject field
    genre = raw_genre.lower().replace(" ", "_")
    print(f"  Searching for: '{genre}'")

    # -- 2. Fetch top 150 books
    entries = fetch_top_books(genre, limit=FETCH_LIMIT)
    if not entries:
        print("No results returned. Try a different genre.")
        return

    # -- 3. Append to CSV
    print(f"\n[STEP 2] Saving to {os.path.basename(CSV_FILE)}")
    append_genre_block(entries, CSV_FILE)

    # -- 4. Load full CSV and analyse
    print("\n[STEP 3] Loading full dataset for analysis")
    all_entries = load_all_entries(CSV_FILE)
    print(f"  Total entries on file: {len(all_entries)}")

    runs = group_by_genre_and_run(all_entries)
    print(f"  Total genre runs on file: {len(runs)}")

    # -- 5. Build results
    print("\n[STEP 4] Running analysis")

    per_run_stats = {}
    for (g, date), run_entries in sorted(runs.items()):
        per_run_stats[f"{g} ({date})"] = analyze_run(run_entries)

    overall = find_overall_bests(all_entries)

    results = {
        "run_date":     datetime.today().strftime("%Y-%m-%d"),
        "genre_fetched_this_run": genre,
        "per_run_stats": per_run_stats,
        "overall":       overall,
    }

    # -- 6. Print summary
    print("\n" + "-" * 60)
    print("  THIS RUN —", genre.upper())
    print("-" * 60)
    this_run = analyze_run(entries)
    print(f"  Top book         : #{1} {this_run['top_book']} by {this_run['top_book_author']}")
    print(f"  Reading log count: {this_run['top_book_readinglog']:,}")
    print(f"  Avg reading log  : {this_run['avg_readinglog']:,.1f}")
    print(f"  Avg rating       : {this_run['avg_rating']}")

    if len(runs) > 1:
        print("\n" + "-" * 60)
        print("  ACROSS ALL GENRES ON FILE")
        print("-" * 60)
        print(f"  Most-read book   : {overall['most_read_book']}")
        print(f"    by               {overall['most_read_book_author']} ({overall['most_read_book_genre']})")
        print(f"    reading log      {overall['most_read_book_count']:,}")
        print(f"  Top author       : {overall['top_author_by_total_reads']}")
        print(f"    total readinglog {overall['top_author_total_readinglog']:,}")
        print("\n  Genres by avg reading log count (most popular first):")
        for item in overall["genres_ranked_by_avg_popularity"]:
            print(f"    {item['genre']:<20} {item['avg_readinglog']:>10,.1f}")

    # -- 7. Save results.json
    print()
    save_results(results)
    print("\nDone! Run again and enter a different genre to keep building your dataset.\n")


if __name__ == "__main__":
    main()
