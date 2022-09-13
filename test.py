import unittest
from avgWordsSong import CalculateSongWordAverage as clsAvg

class Test_AvgWordSong(unittest.TestCase):
    def test_word_count(self):
        self.assertEqual(clsAvg._word_count(self,"one two three 4"), 4)
        self.assertEqual(clsAvg._word_count(self,None), 0)
        self.assertEqual(clsAvg._word_count(self,), 0)
        self.assertEqual(clsAvg._word_count(self,"one"), 1)
        self.assertEqual(clsAvg._word_count(self,"o n e"), 3)

    def test_calculate_list_average(self):
        self.assertEqual(clsAvg._calculate_list_average(self,[2,2,2,2]), 2)
        self.assertEqual(clsAvg._calculate_list_average(self,[1,1,1]), 1)
        self.assertEqual(clsAvg._calculate_list_average(self,None), 0)
        

if __name__ == '__main__':
    unittest.main()

