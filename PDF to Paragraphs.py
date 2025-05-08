import fitz
import json

def extract_text_by_indent(pdf_path, indent_threshold=5):
    doc = fitz.open(pdf_path)
    paragraphs = []
    current_paragraph = []
    previous_x = None

    for page in doc:
        blocks = page.get_text("blocks")
        blocks = sorted(blocks, key=lambda x: (x[1], x[0]))  # Top-to-bottom, then left-to-right

        for i, block in enumerate(blocks):
            text = block[4].strip()
            x0 = block[0]

            if text:
                is_new_paragraph = False

                if previous_x is None:
                    is_new_paragraph = True
                else:
                    is_new_paragraph = x0 - previous_x > indent_threshold

                if is_new_paragraph:
                    if current_paragraph:
                        paragraphs.append(" ".join(current_paragraph).strip())
                    current_paragraph = [text]
                else:
                    current_paragraph.append(text)

                previous_x = x0

    return paragraphs

def save_paragraphs_to_json(paragraphs, json_path):
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(paragraphs, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    pdf_file = "The Dragonet Prophecy.pdf" # Input file
    json_file = "ebook_paragraphs.json" # Output file

    paragraphs = extract_text_by_indent(pdf_file)
    save_paragraphs_to_json(paragraphs, json_file)
    print(f"Extracted {len(paragraphs)} paragraphs and saved to {json_file}")
