# Oskar's Parser

A morphological and syntactic parser for **Kashubian**, a West Slavic language spoken in northern Poland. The parser takes prose text as input, tokenizes and morphologically analyses each word, and stores the annotated corpus in MongoDB.

## Features

- **Preprocessing** — sentence segmentation and word-list extraction
- **Morphological tokenization** — identifies stems and inflectional endings (nouns, adjectives, verbs, pronouns, prepositions, conjunctions, etc.) using suffix dictionaries and preset word lists
- **Lexical database lookup** — optionally queries a PostgreSQL morphology database to validate or refine morphological analyses
- **Syntactic parsing** — resolves case requirements imposed by prepositions
- **Corpus statistics** — word-frequency ranking written to `output/word_frequencies.txt`
- **MongoDB output** — annotated corpus is inserted into the `gryf` database, `texts` collection

## Requirements

- Python ≥ 3.13
- PostgreSQL (for the lexical database, optional)
- MongoDB running on `localhost:27017`

## Installation

```bash
pip install -e .
```

Or with [uv](https://github.com/astral-sh/uv):

```bash
uv sync
```

## Configuration

Create a `.env` file (or set environment variables) with the PostgreSQL connection details:

```
db=<database_name>
db_user=<username>
DB_PASS=<password>
DB_HOST=<host>
DB_PORT=<port>
```

## Usage

```bash
# Parse a text file
python parse.py -f /path/to/text.txt

# Parse a text file and query the lexical database
python parse.py -f /path/to/text.txt --lexical_database

# Parse an inline text string
python parse.py -t "Twój tekst kaszëbsczi."
```

## Project structure

```
parse.py            Entry point and CLI argument handling
analyser.py         Main Analyser class (composes all pipeline steps)
preprocessor.py     Sentence segmentation and word-list extraction
tokenizer.py        Morphological tokenization and suffix matching
parsesyntax.py      Syntactic parsing (preposition–case resolution)
output_stats.py     Word-frequency statistics
db_handler.py       Morphology database query interface
db_connect.py       PostgreSQL connection wrapper
mongo_handler.py    MongoDB connection and insertion
morphemes.py        Suffix dictionaries and preset word lists
helpers.py          Shared utility functions
attrs.py            Morphological attribute definitions
data_handler.py     General data-handling utilities
file_handler.py     File I/O helpers
json_handler.py     JSON I/O helpers
ConfigFiles/        Runtime configuration (e.g. custom ignore lists)
JSON/               Corpus input/output JSON files
output/             Generated statistics files
Texts/              Input text files
loggers/            Logging setup
```

## Output

Each word in the analysed corpus is represented as a dictionary:

```json
{
  "orth": "Kaszëbów",
  "value": "kaszëbów",
  "morph": ["kaszëb", "ów"],
  "attrs": [{"pos": ["subst"], "case": ["gen"], "num": ["pl"]}],
  "index": 0,
  "s_index": 0,
  "ignore": false,
  "syntax_resolved": true
}
```

The full annotated corpus is inserted as a single document into MongoDB (`gryf.texts`).
