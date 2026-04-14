import unittest
from app.routes.create import create_recepie

class Testcreat_recepie(unittest.TestCase):

    def test_upper(self):
        self.assertEqual(create_recepie("Köttbullar","goda kötbullar",2), "Köttbullar","goda kötbullar",2 )

if __name__ == '__main__':
    unittest.main()