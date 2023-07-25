# MultiTranslate

MultiTranslate is a Python application that populates a SQLite database with word lists from various categories in English, and then translates them into multiple languages using the Google Translate API.

## Overview

MultiTranslate consists of two Python scripts:

1. `translations_to_db.py` - Populates a SQLite database with English word lists and translates those words into various languages, adding those translations to the database.
2. `fetch_translations.py` - Contains functions to fetch translations from the database, and can filter by language or category.

It also includes a dictionary file:

1. `words.py` - Contains a dictionary with categories and words in English.

## Features

- Uses the SQLAlchemy ORM for easy database operations.
- Uses the googletrans library to translate English words into multiple languages.
- Provides utility functions for fetching translations from the database, filtering by language or category.

## Installation

1. Clone this repository.
2. Install the required dependencies: Important note - install googletrans==3.1.0a0 version.
3. Run `translations_to_db.py` to populate the database with English words and their translations.

## Usage

Use the functions in `fetch_translations.py` to fetch translations from the database.

Here are some examples:

```python
# Fetch all categories
categories = get_all_categories()
for category in categories:
    print(category.name)

# Fetch and print all words in the 'animals' category
words = get_words_in_category('animals')
for word in words:
    print(word.word)

# Fetch and print Swedish translation for 'dog'
translation = get_word_translation('dog', 'Swedish')
print(translation)

# Fetch and print all translations for 'dog'
translations = get_all_translations('dog')
for translation in translations:
    print(f'{translation.language}: {translation.translation}')

# Fetch and print all Estonian translations along with their corresponding English words
word_translation_pairs = get_words_in_language('Estonian')
for word, translation in word_translation_pairs:
    print(f'{word}: {translation}')
```

Each function opens and closes a session to interact with the database, fetching the required data and returning it in a format that's easy to work with. The use of SQLAlchemy's ORM capabilities ensures that the code is clean, efficient, and maintainable.
