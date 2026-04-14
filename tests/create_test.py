import unittest
from app.routes.create import create_recepie
from app.routes.register import register_user
from app.utils.modify_db import *

class Testcreat_recepie(unittest.TestCase):

    def test_create_one_recepie(self):
        result = create_recepie("Köttbullar","goda kötbullar", 2)
        self.assertEqual(result.recipe_title,"Köttbullar")
        self.assertEqual(result.description,"goda kötbullar")
        self.assertEqual(result.user_id, 2)

    def test_create_two_recepies(self):
        result = create_recepie("Hamburgare","goda Hamburgare", 3)
        self.assertEqual(result.recipe_title,"Hamburgare")
        self.assertEqual(result.description,"goda Hamburgare")
        self.assertEqual(result.user_id, 3)
        
    def test_ingredient_create(self):
        result = ingredient_create("Kött", "3/4", "st", 1)
        self.assertEqual(result.name, "Kött")
        self.assertEqual(result.amount, 0.75)
        self.assertEqual(result.unit, "st")

    def test_ingredient_create_2(self):
        result = ingredient_create("Äpple", "abc", "kg", 2)
        self.assertIsNone(result)

    def test_register_user(self):
        result = register_user('user','pass','pass')
        self.assertIsInstance(result, User)
        with self.assertRaises(RuntimeError):    
            result = register_user('','','')
        with self.assertRaises(RuntimeError):
            result = register_user('user','','')
        with self.assertRaises(RuntimeError):
            result = register_user('user','pass','ssap')



if __name__ == '__main__':
    unittest.main()