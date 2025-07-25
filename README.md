# Paragraph Finder

Paragraph Finder is a tool that searches an index of paragraphs for you.

## About

In 2024, I started [Wings of Fire Wiki](https://wingsoffire.wiki), an online encyclopedia documenting the children's novel series *Wings of Fire* by Tui T. Sutherland. To help verify the accuracy of wiki content, our citations are classified by book, chapter, and paragraph number. This is more reliable than page numbers, which may differ by edition.

Unfortunately, counting paragraph numbers is terrible. It is easy to make mistakes, long chapters take a long time to count, and there may be some confusion on certain types of formatting like poems.

To solve these problems, I created Paragraph Finder. Paragraph Finder takes a book title, chapter title, and paragraph quote, and gives you the number of the paragraph. It references JSON index files containing each paragraph as a string as part of a list that is labled with the chapter title. It even has fuzzy paragraph search, so you don't need to type the paragraph perfectly with the fancy punctuation.

You can find the Wings of Fire paragraph counter web GUI at <https://wingsoffire.wiki/paragraphs>.

## Use

There are two ways you can use Paragraph Finder. There is a CLI version and a web version.

**paragraph-finder-cli.py** is a command-line utility that uses index files on the local machine. This is the easiest way to get started.

Example:

```
Enter path of the JSON file: The Dragonet Prophecy.json
Enter the chapter: 1
Enter the paragraph to search for (end with two blank lines):
"Well, first we save the world," Tsunami said. "And then we go home."

Approximate match found at index 64 in chapter '1'.
Similarity score: 0.94
Closest paragraph:
“Well, first we save the world,” Tsunami said. “And then we go home.”
```

**paragraph-finder-web.py** is a backend for the web UI, which you can find at [BogTheMudWing/Paragraph-Finder-WebUI](https://github.com/BogTheMudWing/Paragraph-Finder-WebUI). The web version needs a separate backend because bundling the entire application in the browser would require distributing the entire contents of the book as well, which is illegal for works protected under copyright. The easiest way to deploy this in production is to set up a Docker container.

Build the container:

```bash
docker build -t paragraph-finder .
```

Create and start the container:

```bash
docker run -p 5000:5000 --name paragraph-finder -v ./books:/app/books/ --restart always -d paragraph-finder
```

Alternatively, you can use the included Docker Compose file:

```bash
docker compose up -d
```

You can reach it on port 5000. Index files can be placed in the books folder.

---

Whichever you use, you'll need some index files for the books you want. The easiest way is to convert a PDF of the book into JSON. You can find a script that does most of the conversion for you at [BogTheMudWing/PDF-To-Paragraphs](https://github.com/BogTheMudWing/PDF-To-Paragraphs). PDFs are not designed to be computer-friendly, so the paragraphs are detected by indent. It's not perfect and it won't work for every PDF, but it gets most of the work done and you only need to clean it up rather than copy and paste the whole thing. If you *don't* have a PDF... you might be better off asking a friend who does or not going this route at all, depending on the length of the book and your patience.

Index files should not have spaces in their names and be formatted like so:

```json
{
  "chapters": {
    "chapter_name": [
      "Paragraph 1",
      "Paragraph 2",
      "Paragraph 3",
      "and so on..."
    ],
    "another_chapter": [
      "More paragraphs"
    ],
    "and_so_on": [
      "More paragraphs"
    ]
  }
}
```

---

[![Bog The MudWing](https://blog.macver.org/content/images/2025/07/Stamp-Colored-Small-Shadow.png)](https://blog.macver.org/about-me)
