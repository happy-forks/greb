import unittest

from greb import meaning as greb

import data

class TestGreb(unittest.TestCase):

	def test_read_page(self):
		for each_word, each_status_code in data.READ_PAGE_DATA.iteritems():
			response, status_code = greb.read_page(data.COMMON['URLS']['base'].format(word=each_word))
			self.assertEqual(status_code, each_status_code)

	def test_read_page_exception(self):
		response, status_code = greb.read_page(data.COMMON['URLS']['invalid'])
		self.assertFalse(status_code)

	def test_find_meaning(self):
		for each_word, each_word_meaning in data.INPUT_WORDS['MEANING'].iteritems():
			tree, status_code = greb.make_parse_tree(data.COMMON['URLS']['base'].format(word=each_word))
			self.assertEqual(status_code, data.COMMON['STATUS_CODE']['ok'])
			
			meaning = greb.find_meaning_copy(tree)
			self.assertEqual(meaning, each_word_meaning)

	def test_find_sentences(self):
		for each_word, each_word_sentence in data.INPUT_WORDS['SENTENCE'].iteritems():
			tree, status_code = greb.make_parse_tree(data.COMMON['URLS']['base'].format(word=each_word))
			self.assertEqual(status_code, data.COMMON['STATUS_CODE']['ok'])

			sentence = greb.find_sentences(tree, each_word)
			self.assertEqual(sentence, each_word_sentence)

	def test_find_synonyms(self):
		for each_word, each_word_synonym in data.INPUT_WORDS['SYNONYM'].iteritems():
			tree, status_code = greb.make_parse_tree(data.COMMON['URLS']['base'].format(word=each_word))
			self.assertEqual(status_code, data.COMMON['STATUS_CODE']['ok'])

			synonym = greb.find_synonyms(tree)
			self.assertEqual(synonym, each_word_synonym)

	def test_find_antonyms(self):
		for each_word, each_word_antonym in data.INPUT_WORDS['ANTONYM'].iteritems():
			tree, status_code = greb.make_parse_tree(data.COMMON['URLS']['base'].format(word=each_word))
			self.assertEqual(status_code, data.COMMON['STATUS_CODE']['ok'])

			antonym = greb.find_antonyms(tree)
			self.assertEqual(antonym, each_word_antonym)

	def test_find_trending_words(self):
		tree, status_code = greb.make_parse_tree(data.COMMON['URLS']['home'])
		self.assertEqual(status_code, data.COMMON['STATUS_CODE']['ok'])

		trending_words = greb.find_trending_words(tree)
		self.assertEqual(len(trending_words), 5)

	def test_find_word_of_the_day(self):
		tree, status_code = greb.make_parse_tree(data.COMMON['URLS']['home'])
		self.assertEqual(status_code, data.COMMON['STATUS_CODE']['ok'])

		word_of_day = greb.find_word_of_the_day(tree)
		self.assertEqual(len(word_of_day), 1)


if __name__ == '__main__':
	unittest.main()
