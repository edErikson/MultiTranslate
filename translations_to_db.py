from sqlalchemy import create_engine, Column, Integer, String, exc
from sqlalchemy.orm import declarative_base, sessionmaker
from words import eng_word_lists
from googletrans import Translator

Base = declarative_base()

# Database engine setup. Here we're using SQLite.
engine = create_engine('sqlite:///translations.db')

# Creating a Session class using sessionmaker factory, bound to our database engine
Session = sessionmaker(bind=engine)


class Translations(Base):
    """
    ORM class for the words table.
    """
    __tablename__ = 'words'

    id = Column(Integer, primary_key=True)
    category_name = Column(String)
    words = Column(String, unique=True)
    tag = Column(Integer)  # This tag is used to identify groups of related translations across different languages
    language = Column(String)

    def __repr__(self):
        return f"<Translations(category_name='{self.category_name}'," \
               f" words='{self.words}'," \
               f" tag={self.tag}," \
               f" language='{self.language}')>"


LANG_CODES = [
    {'name': 'English', 'code': 'en'},
    {'name': 'Swedish', 'code': 'sv'},
    {'name': 'Finnish', 'code': 'fi'},
    {'name': 'Estonian', 'code': 'et'},
    {'name': 'Latvian', 'code': 'lv'},
    {'name': 'Lithuanian', 'code': 'lt'},
    {'name': 'Russian', 'code': 'ru'},
    {'name': 'Polish', 'code': 'pl'},
]
translator = Translator()


def populate_database():
    """
    Populate the database with words from the English word dictionary.
    All words from the same category are stored in a single string.
    """
    session = Session()

    for tag, (category_name, words) in enumerate(eng_word_lists.items()):
        tag += 1
        # Check if the category already exists in the database
        existing_category = session.query(Translations).filter_by(category_name=category_name,
                                                                  language="English").first()
        if existing_category is None:
            # Join all words into a single string separated by commas
            words_str = ", ".join(words)
            category = Translations(category_name=category_name, words=words_str, tag=tag, language="English")
            session.add(category)

        # Commit the changes and close the session
    session.commit()
    session.close()

def translate_words(target_language):
    """
    Translate English words to the target language and store the translations in the database.
    Note: This function should be called after populate_database, as it relies on the English
    translations being present in the database.
    """
    session = Session()

    # Fetch all English categories from the database
    english_translations = session.query(Translations).filter_by(language="English").all()

    for translation in english_translations:
        # Translate the category name
        translated_category_name = translator.translate(translation.category_name, dest=target_language['code'], src='en').text

        # Check if the translated category already exists in the database
        existing_translated_category = session.query(Translations).filter_by(category_name=translated_category_name,
                                                                             language=target_language['name']).first()
        if existing_translated_category is None:
            # Translate the words
            translated_words = translator.translate(translation.words, dest=target_language['code'], src='en').text

            # Create a new row for the translated words
            translated_category = Translations(category_name=translated_category_name, words=translated_words,
                                               tag=translation.tag, language=target_language['name'])
            session.add(translated_category)

    # Commit the changes and close the session
    session.commit()
    session.close()


if __name__ == '__main__':
    # Create tables
    Base.metadata.create_all(engine)

    # Populate the database with English words
    populate_database()

    # Translate words to all languages in LANG_CODES (excluding English)
    for target_language in LANG_CODES[1:]:
        translate_words(target_language)

    # Create a new engine and session for the purpose of retrieving and printing all database rows.
    # This is separate from the above operations to ensure all transactions are committed before we query the database.
    engine = create_engine('sqlite:///translations.db')
    Session = sessionmaker(bind=engine)
    session = Session()
    rows = session.query(Translations).all()

    for row in rows:
        print(
            f"ID: {row.id}, Category: {row.category_name}, Words: {row.words}, Tag: {row.tag}, Language: {row.language}")

    session.close()
