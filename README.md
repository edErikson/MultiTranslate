# MultiTranslate

This Python application populates a SQLite database with word lists from various categories in English, then translates them into multiple languages using the Google Translate API.

## Overview

This application is comprised of two Python scripts:

1. `translations_to_db.py` - Populates a SQLite database with English word lists, then translates those words into various languages and adds those translations to the database.
2. `fetch_translations.py` - Contains functions to fetch translations from the database based on language, category, or tag.
3. `words.py` - Dictionary with categories and words in english

## Features

- Uses SQLAlchemy ORM for easy database operations.
- Uses googletrans library for translating English words into multiple languages.
- Provides utility functions for fetching translations from the database by language, category, or tag.

## Installation

1. Clone this repository:
2. Install the required dependencies: Important note - install googletrans==3.1.0a0 version
3. Run `translations_to_db.py` to populate the database with English words and their translations:



## Usage

Use the functions in `fetch_translations.py` to fetch translations from the database.

Here are some examples:

```python
# Fetch and print all Finnish translations
translations = fetch_translations_by_language('Finnish')
for translation in translations:
 print(f"ID: {translation.id},"
       f" Category: {translation.category_name},"
       f" Words: {translation.words},"
       f" Tag: {translation.tag},"
       f" Language: {translation.language}")

# Fetch and print all translations with tag 6
tags = fetch_translations_by_tag(6)
for translation in tags:
 print(f"ID: {translation.id},"
       f" Category: {translation.category_name},"
       f" Words: {translation.words},"
       f" Tag: {translation.tag},"
       f" Language: {translation.language}")

# Fetch and print all translations in the 'question' category
category = fetch_translations_by_category("question")
for translation in category:
 print(f"ID: {translation.id},"
       f" Category: {translation.category_name},"
       f" Words: {translation.words},"
       f" Tag: {translation.tag},"
       f" Language: {translation.language}")
