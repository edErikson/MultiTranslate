from translations_to_db import Session, Category, Word, Translation


def get_all_categories():
    session = Session()
    categories = session.query(Category).all()
    session.close()
    return categories


def get_words_in_category(category_name):
    session = Session()
    category = session.query(Category).filter_by(name=category_name).first()
    words = category.words if category else []
    session.close()
    return words


def get_word_translation(word, language):
    session = Session()
    word_obj = session.query(Word).filter_by(word=word).first()
    if word_obj:
        translation = session.query(Translation).filter_by(word_id=word_obj.id, language=language).first()
        session.close()
        return translation.translation if translation else None
    session.close()
    return None


def get_all_translations(word):
    session = Session()
    word_obj = session.query(Word).filter_by(word=word).first()
    translations = word_obj.translations if word_obj else []
    session.close()
    return translations


def get_words_in_language(language):
    session = Session()
    translations = session.query(Translation).filter_by(language=language).all()
    word_translation_pairs = [(translation.word.word, translation.translation) for translation in translations]
    session.close()
    return word_translation_pairs



if __name__ == '__main__':

    # categories = get_all_categories()
    # for category in categories:
    #     print(category.name, end=' ')

    # words = get_words_in_category('animals')
    # for word in words:
    #     print(word.word, end=' ')

    # translation = get_word_translation('dog', 'Swedish')
    # print(translation)

    # translations = get_all_translations('dog')
    # for translation in translations:
    #     print(f'{translation.language}: {translation.translation}')

    words = get_words_in_language('Estonian')
    for word in words:
        print(word)



