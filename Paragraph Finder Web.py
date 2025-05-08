import json
import difflib
from flask import Flask, request, jsonify

app = Flask(__name__)

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

@app.route('/find_paragraph', methods=['POST'])
def find_paragraph():
    data = request.get_json()
    book_name = data.get('book_name')
    chapter_key = data.get('chapter')
    paragraph = data.get('paragraph')

    if not book_name or not chapter_key or not paragraph:
        return jsonify({"reason": "Missing required parameters (book_name, chapter, paragraph)"}), 400

    try:
        book = load_book(f"{book_name}.json")  # assuming book name corresponds to JSON file
    except FileNotFoundError:
        return jsonify({"reason": "Book not found. Did you type it correctly? Check the wiki."}), 404

    try:
        index, match, score = find_paragraph_index(book, chapter_key, paragraph)
    except TypeError:
        return jsonify({"reason": "Chapter not found. Did you type it correctly? It should be a lowercase name like \"epilogue\" (without quotes) or a number."})

    if index:
        response = {
            "index": index,
            "similarity_score": round(score, 2),
            "match": match
        }
        return jsonify(response)
    else:
        return jsonify({"reason": "No close match found. Make sure you have entered the entire paragraph and that the book and chapter are correct."}), 404


if __name__ == "__main__":
    app.run(debug=True)
