import pathlib

BASE = pathlib.Path(__file__).parent
file_path = BASE / "high_scores.txt"
MAX_SCORES = 10

def load_scores():
    """Read and return the high scores from the file."""
    if not file_path.exists():
        return [], MAX_SCORES

    lines = file_path.read_text().splitlines()
    if not lines:
        raise RuntimeError("Invalid high scores file format")

    scores = []
    for l in lines:
        try:
            scores.append(int(l.strip()))
        except ValueError:
            continue

    return scores

def save_scores(scores):
    """Save the high scores to the file."""
    top = scores[:MAX_SCORES]
    body = "\n".join(str(s) for s in top)
    file_path.write_text(body)

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