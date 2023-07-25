from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base, sessionmaker
from words import eng_word_lists
from googletrans import Translator

# Define declarative base class for SQLAlchemy ORM
Base = declarative_base()

# Database engine setup. Here we're using SQLite.
engine = create_engine('sqlite:///translations.db')

# Creating a Session class using sessionmaker factory, bound to our database engine
Session = sessionmaker(bind=engine)


# List of language codes to translate English words into
LANG_CODES = [
    {'name': 'Swedish', 'code': 'sv'},
    {'name': 'Finnish', 'code': 'fi'},
    {'name': 'Estonian', 'code': 'et'},
    {'name': 'Latvian', 'code': 'lv'},
    {'name': 'Lithuanian', 'code': 'lt'},
    {'name': 'Russian', 'code': 'ru'},
    {'name': 'Polish', 'code': 'pl'},
]


# Define the Category model, which represents a category of words
class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String)


# Define the Word model, representing a word in English and its category
class Word(Base):
    __tablename__ = 'words'
    id = Column(Integer, primary_key=True)
    word = Column(String)
    category_id = Column(Integer, ForeignKey('categories.id'))

    category = relationship("Category", back_populates="words")


Category.words = relationship("Word", order_by=Word.id, back_populates="category")


# Define the Translation model, representing a translation of a word into another language
class Translation(Base):
    __tablename__ = 'translations'
    id = Column(Integer, primary_key=True)
    word_id = Column(Integer, ForeignKey('words.id'))
    language = Column(String)
    translation = Column(String)

    word = relationship("Word", back_populates="translations")


Word.translations = relationship("Translation", order_by=Translation.id, back_populates="word")

# Translator setup
translator = Translator()


def populate_database():
    session = Session()

    # For each category and list of words in that category
    for category_name, words in eng_word_lists.items():
        category = Category(name=category_name)
        session.add(category)
        for word in words:
            w = Word(word=word, category=category)
            session.add(w)
            for lang in LANG_CODES:
                # Translate each word into each language and create a Translation object
                translation = translator.translate(word, dest=lang['code'], src='en').text
                t = Translation(word=w, language=lang['name'], translation=translation)
                session.add(t)
    session.commit()
    session.close()


if __name__ == '__main__':
    # Create tables
    Base.metadata.create_all(engine)

    # Populate the database with English words and their translations
    populate_database()
