from config import SCORES_FILE, TOP_SCORES_COUNT


def load_scores():
    """Challenge 12: read scores.txt. Each line is 'name;score'."""
    scores = []
    try:
        with open(SCORES_FILE, "r", encoding="utf-8") as f:
            for line in f:
                name, separator, value = line.strip().rpartition(";")
                if separator and value.isdigit():
                    scores.append((name, int(value)))
    except OSError:
        pass  # the file does not exist yet (or cannot be read): no scores
    return scores


def load_top_scores():
    """Return the best scores, sorted from highest to lowest"""
    ordered = sorted(load_scores(), key=lambda item: item[1], reverse=True)
    return ordered[:TOP_SCORES_COUNT]


def save_score(name, score):
    """Add one line to scores.txt. Returns False if the file could not be written."""
    try:
        with open(SCORES_FILE, "a", encoding="utf-8") as f:
            f.write(f"{name};{score}\n")
        return True
    except OSError:
        return False
