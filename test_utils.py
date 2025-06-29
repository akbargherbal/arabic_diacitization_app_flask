# test_utils.py

import unittest
import json
from utils import text_to_html_spans

class TestTextToHtmlSpans(unittest.TestCase):

    def test_simple_word_processing(self):
        """
        Tests if a simple word 'أَب' is processed correctly into its data dictionaries.
        """
        # --- ARRANGE ---
        # The input text for our test
        test_verse = "أَبٌ"

        # --- ACT ---
        # Run the function we want to test
        (
            html_content,
            tokens_count,
            total_diacritics,
            wd_dict,
            char_dict_global,
            char_dict_local,
        ) = text_to_html_spans(test_verse)

        # --- ASSERT ---
        # Now, we make assertions about the output. If any of these are false, the test fails.

        # 1. Test the global character dictionary
        self.assertEqual(len(char_dict_global), 2, "Should find 2 interactive characters")
        
        # Check the first character ('أ')
        self.assertEqual(char_dict_global[0]['char'], 'أ')
        self.assertEqual(char_dict_global[0]['dia'], 'َ')
        self.assertEqual(char_dict_global[0]['wd_idx'], 0)
        self.assertEqual(char_dict_global[0]['global_dia_idx'], 0)

        # Check the second character ('ب')
        self.assertEqual(char_dict_global[1]['char'], 'ب')
        self.assertEqual(char_dict_global[1]['dia'], 'ٌ')
        self.assertEqual(char_dict_global[1]['wd_idx'], 0)
        self.assertEqual(char_dict_global[1]['global_dia_idx'], 1)

        # 2. Test the word dictionary
        self.assertEqual(len(wd_dict), 1, "Should find 1 word")
        self.assertTrue(wd_dict[0]['isWord'])
        self.assertEqual(wd_dict[0]['wordDiaCount'], 2)

        # 3. Test the overall counts
        self.assertEqual(tokens_count, 1)
        self.assertEqual(total_diacritics, 2)
        
        print("\n✅ test_simple_word_processing: PASSED")


# This allows us to run the tests by executing the file directly
if __name__ == '__main__':
    unittest.main()