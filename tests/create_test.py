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
        result = register_user('f_name','l_name','email@test.se','pass','pass')
        self.assertIsInstance(result, User) # correct, should pass
        with self.assertRaises(RuntimeError): # missing username argument exception    
            result = register_user('','','','','')
        with self.assertRaises(RuntimeError): # missing password argument
            result = register_user('f_name','l_name','email@test.se','','')
        with self.assertRaises(RuntimeError): # password miss match error
            result = register_user('f_name','l_name','email@test.se','pass','ssap')
        with self.assertRaises(RuntimeError): # incorrect email formatting
            result = register_user('f_name','l_name','emailtestse','pass','pass')

    def test_create_step(self):
        result = create_step("step 1 boil potato", 1)
        self.assertEqual(result.name, "step 1 boil potato")
        self.assertEqual(result.recipe_id, 1)
    
    def test_create_wrong_step(self):
        result = create_step("step 2 eat potato", 2)
        self.assertIsNot(result.name, "step 1 eat potato")
        self.assertEqual(result.recipe_id, 2)

    def test_create_empty_step(self):
        result = create_step("", 1)
        self.assertIsNone(result)

    def test_create_negative_index(self):
        result = create_step("test", -1)
        self.assertIsNone(result)



if __name__ == '__main__':
    unittest.main()