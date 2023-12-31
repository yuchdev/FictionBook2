import os
import unittest
from fictionbook.reader import Fb2Reader


class Fictionbook2ReaderTest(unittest.TestCase):
    TEST_ASSETS_PATH = os.path.join(os.path.dirname(__file__), 'assets')

    def test_book1_metadata(self):
        test_book_path = os.path.join(self.TEST_ASSETS_PATH, 'sol_invictus_book1.fb2')
        expected_metadata = {
            'title-info': {
                'genre': 'prose_contemporary',
                'author': {
                    'first-name': 'Виктор',
                    'middle-name': 'Олегович',
                    'last-name': 'Пелевин'
                },
                'book-title': 'Непобедимое солнце. Книга 1', 'annotation': {
                    'p': 'Какой стала Саша после встречи с тайной, вы узнаете из книги. '
                         'Какой стала тайна после встречи с\n                    '
                         'Сашей, вы уже немного в курсе и так.'
                },
                'keywords': 'постмодернизм,тайна,философская проза,духовные поиски,современное искусство',
                'date': '2020', 'coverpage': {'image': ''}, 'lang': 'ru', 'sequence': ''
            },
            'document-info': {
                'author': {'nickname': 'MCat78'},
                'program-used': 'FictionBook Editor Release 2.6.7', 'date': '2020-07-31',
                'src-url': 'http://www.litres.ru/pages/biblio_book/?art=57212123',
                'src-ocr': 'Текст предоставлен правообладателем',
                'id': 'f67de95a-d34a-11ea-a2b5-0cc47a520475', 'version': '1.0',
                'history': {
                    'p': 'v\xa01.0\xa0– создание fb2\xa0– (MCat78)'
                },
                'publisher': {
                    'first-name': 'Литагент', 'last-name': '1 редакция (6)',
                    'id': 'fad0e42f-3c1a-11e9-b9d6-0cc47a520474'
                }
            },
            'publish-info': {
                'book-name': 'Непобедимое Солнце. Книга I', 'publisher': 'Эксмо',
                'city': 'Москва', 'year': '2020', 'isbn': '978-5-532-02805-0',
                'sequence': ''
            },
            'custom-info': '© В. О. Пелевин, текст, 2020, © Оформление. ООО «Издательство «Эксмо», 2020'
        }
        expected_chapters = 2
        expected_paragraphs = 2596
        expected_cover = './images/cover.jpg'

        reader = Fb2Reader(test_book_path, images_dir='./images')
        self.assertEqual(reader.metadata, expected_metadata)
        self.assertEqual(len(reader.chapters), expected_chapters)
        self.assertEqual(len(reader.paragraphs), expected_paragraphs)
        self.assertEqual(reader.cover, expected_cover)

    def test_book2_metadata(self):
        test_book_path = os.path.join(self.TEST_ASSETS_PATH, 'frost.fb2')
        expected_metadata = {'title-info': {'author': {'last-name': 'Anton Pavlovich Chekhov'}, 'book-title': 'Frost'}}
        expected_chapters = 1
        expected_paragraphs = 44
        expected_cover = None

        reader = Fb2Reader(test_book_path, images_dir='./images')
        self.assertEqual(reader.metadata, expected_metadata)
        self.assertEqual(len(reader.chapters), expected_chapters)
        self.assertEqual(len(reader.paragraphs), expected_paragraphs)
        self.assertEqual(reader.cover, expected_cover)

    def test_book3_metadata(self):
        test_book_path = os.path.join(self.TEST_ASSETS_PATH, 'transients_in_arcadia.fb2')
        expected_metadata = {'title-info': {'author': {'last-name': 'O. Henry'}, 'book-title': 'Transients In Arcadia'}}
        expected_chapters = 1
        expected_paragraphs = 35
        expected_cover = None

        reader = Fb2Reader(test_book_path, images_dir='./images')
        self.assertEqual(reader.metadata, expected_metadata)
        self.assertEqual(len(reader.chapters), expected_chapters)
        self.assertEqual(len(reader.paragraphs), expected_paragraphs)
        self.assertEqual(reader.cover, expected_cover)

    def test_images(self):
        test_book_path = os.path.join(self.TEST_ASSETS_PATH, 'sol_invictus_book1.fb2')
        expected_images_content = [
            './images/cover.jpg',
            './images/i_001.png',
            './images/i_002.png',
            './images/i_003.png',
            './images/i_004.png',
            './images/i_005.png',
            './images/i_006.png',
            './images/i_007.png',
            './images/i_008.png',
            './images/i_009.png',
            './images/i_010.png',
            './images/i_011.png',
            './images/i_012.png',
            './images/i_013.png',
            './images/i_014.png',
            './images/i_015.png',
            './images/i_016.png',
            './images/i_017.png',
            './images/i_018.png',
            './images/i_019.png',
            './images/i_020.png',
            './images/i_021.png',
        ]
        reader = Fb2Reader(test_book_path, images_dir='./images')
        # compare sets of images to handle different order of sorting
        self.assertEqual(set(reader.images), set(expected_images_content))


if __name__ == '__main__':
    unittest.main()
