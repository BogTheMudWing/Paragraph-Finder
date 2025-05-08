import json
import difflib

def load_book(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return json.load(file)

def normalize_text(text):
    return ' '.join(text.split())

def find_paragraph_index(book, chapter_key, target_paragraph, threshold=0.8):
    chapter = book.get(chapter_key)
    if chapter is None:
        print(f"Chapter '{chapter_key}' not found.")
        return None
    
    # Clean and normalize whitespace
    target_paragraph = ' '.join(target_paragraph.split())

    # Normalize all chapter paragraphs the same way for matching
    normalized_chapter = [' '.join(p.split()) for p in chapter]

    # Try exact match first
    if target_paragraph in normalized_chapter:
        index = normalized_chapter.index(target_paragraph)
        return index + 1, chapter[index], 1.0

    # Use difflib to find the closest match
    best_match = None
    best_score = 0.0
    best_index = -1

    for i, para in enumerate(normalized_chapter):
        score = difflib.SequenceMatcher(None, target_paragraph, para).ratio()
        if score > best_score:
            best_score = score
            best_index = i
            best_match = chapter[i]

    if best_score >= threshold:
        return best_index + 1, best_match, best_score

    return None, None, None

def main():
    book_name = input("Enter path of the JSON file")
    book = load_book(book_name)

    chapter_key = input("Enter the chapter (e.g., 'prologue', '1', '2', etc.): ")
    print("Enter the paragraph to search for (end with two blank lines):")

    lines = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line == "":
            break
        lines.append(line)

    paragraph = normalize_text(' '.join(lines))

    index, match, score = find_paragraph_index(book, chapter_key, paragraph)

    if index:
        if score == 1.0:
            print(f"Exact match found at index {index} in chapter '{chapter_key}'.")
        else:
            print(f"Approximate match found at index {index} in chapter '{chapter_key}'.")
            print(f"Similarity score: {score:.2f}")
            print("Closest paragraph:")
            print(match)
    else:
        print("No close match found.")

if __name__ == "__main__":
    main()
