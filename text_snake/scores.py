import hashlib
import pathlib

BASE = pathlib.Path(__file__).parent
file_path = BASE / "high_scores.txt"
MAX_SCORES = 10
CHECKSUM_PREFIX = "# "

def compute_checksum(data: str) -> str:
    return hashlib.sha256(data.encode('UTF-8')).hexdigest()

def compare_checksums(data: str, checksum: str) -> bool:
    """Compare the computed checksum with the stored checksum."""
    return compute_checksum(data) == checksum

def load_scores():
    """Read and return the high scores from the file."""
    if not file_path.exists():
        return []

    text = file_path.read_text().splitlines()

    if not text or not text[-1].startswith(CHECKSUM_PREFIX):
        print("Invalid high scores file.")
        return []

    *score_lines, checksum_line = text
    raw_data = "\n".join(score_lines) + "\n"
    stored = checksum_line[len(CHECKSUM_PREFIX):].strip()
    if not compare_checksums(raw_data, stored):
        print("File checksum mismatch. File has been modified or corrupted.")
        return []

    return [int(l) for l in score_lines if l.strip().isdigit()]

def save_scores(scores):
    """Save the high scores to the file."""
    top = scores[:MAX_SCORES]
    scores_text = "\n".join(str(s) for s in top) + "\n"
    checksum = compute_checksum(scores_text)
    content = scores_text + CHECKSUM_PREFIX + checksum + "\n"
    file_path.write_text(content)

def update_scores(new_score):
    """Append a new score to the high scores list and save it."""
    scores = load_scores()
    scores.append(new_score)
    save_scores(sorted(scores, reverse=True))

def display_scores():
    """Print the high scores to the console."""
    try:
        scores = load_scores()
    except RuntimeError as e:
        print(f"Error loading scores: {e}")
        return
    lines = ["=== High Scores ==="]
    if not scores:
        lines.append("No scores yet. Keep playing!")
    else:
        for i, score in enumerate(scores, start=1):
            lines.append(f"{i}. {score}")
    print("\n".join(lines))

def clear_scores():
    """Clear the high scores file."""
    file_path.write_text("")
    print("Scores cleared.")