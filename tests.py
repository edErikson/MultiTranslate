import unittest
from unittest.mock import MagicMock, patch
from translations_to_db import populate_database, Translations
from words import eng_word_lists

class TestPopulateDatabase(unittest.TestCase):
    @patch('translations_to_db.Session')
    def test_populate_database(self, MockSession):
        # Create a mock session and configure it to return a mock query object
        mock_session = MockSession.return_value
        mock_query = MagicMock()
        mock_session.query.return_value = mock_query

        # The database is initially empty, so filter_by should return a query that has no results
        mock_query.filter_by.return_value.first.return_value = None

        # Call the function with the mock session
        populate_database()

        # Check that a new Translations object was created and added to the session for each category
        self.assertEqual(mock_session.add.call_count, len(eng_word_lists))

        # Check that commit was called once after all categories were added
        mock_session.commit.assert_called_once()

    @patch('translations_to_db.Session')
    def test_populate_database_existing_words(self, MockSession):
        # Create a mock session and configure it to return a mock query object
        mock_session = MockSession.return_value
        mock_query = MagicMock()
        mock_session.query.return_value = mock_query

        # This time, the database already contains some words, so filter_by should return a non-empty result
        mock_query.filter_by.return_value.first.return_value = Translations()

        # Call the function with the mock session
        populate_database()

        # Check that no new Translations objects were added to the session
        mock_session.add.assert_not_called()

        # Check that commit was not called
        mock_session.commit.assert_not_called()

if __name__ == '__main__':
    unittest.main()
