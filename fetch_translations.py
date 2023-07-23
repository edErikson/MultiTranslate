from translations_to_db import Session, Translations


def fetch_translations_by_language(language):
    session = Session()
    results = session.query(Translations).filter_by(language=language).all()
    session.close()
    return results


def fetch_translations_by_category(category_name):
    session = Session()
    tag = session.query(Translations).filter_by(category_name=category_name).first().tag
    results = session.query(Translations).filter_by(tag=tag).all()
    session.close()
    return results


def fetch_translations_by_tag(tag):
    session = Session()
    results = session.query(Translations).filter_by(tag=tag).all()
    session.close()
    return results


if __name__ == '__main__':
    # Example usages of the fetch functions:
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

