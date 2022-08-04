from unittest import TestCase

from firebase_admin import db

from db.FirebaseRTDB import FirebaseRTDB
from utils.nested_dict import deep_read


class TestFirebaseRTDB(TestCase):
    ROOT = "debug/unittest"
    STORAGE = FirebaseRTDB()
    STORAGE.ROOT = ROOT

    @classmethod
    def setUpClass(cls) -> None:
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def test_load(self):
        saved = {
            "a": 1,
            "b": {
                "c": "cat",
                "d": {
                    "e": True
                }
            }
        }

        ref = db.reference()
        ref.child(self.ROOT).set(saved)

        self.STORAGE.load()
        self.assertEqual(saved, self.STORAGE.JSON)

    def test_write(self):
        self.STORAGE.JSON = {
            "a": 1,
            "b": {
                "c": "cat",
                "d": {
                    "e": True
                }
            }
        }

        self.STORAGE.write(42, "b/d/f")
        self.assertEqual(42, deep_read(self.STORAGE.JSON, "b/d/f".split('/')))

        self.STORAGE.ROOT += "b/d"
        self.STORAGE.write(None, "g/h")
        self.assertEqual(None, deep_read(self.STORAGE.JSON, "g/h".split('/')))
        self.STORAGE.ROOT = ''

    def test_read(self):
        self.STORAGE.JSON = {
            "a": 1,
            "b": {
                "c": "cat",
                "d": {
                    "e": True
                }
            }
        }

        self.assertEqual(True, self.STORAGE.read("b/d/e"))
        with self.assertRaises(ValueError):
            self.STORAGE.read("b/d/e/f")

    def test_exists(self):
        self.STORAGE.JSON = {
            "a": 1,
            "b": {
                "c": "cat",
                "d": {
                    "e": True
                }
            }
        }

        self.assertTrue(self.STORAGE.exists("b/d"))
        self.assertFalse(self.STORAGE.exists("b/skjdf"))

    def test_delete(self):
        self.STORAGE.JSON = {
            "a": 1,
            "b": {
                "c": "cat",
                "d": {
                    "e": True
                }
            }
        }
        self.assertTrue(self.STORAGE.exists("b"))
        self.STORAGE.delete("b")
        self.assertFalse(self.STORAGE.exists("b"))

    def test_is_empty(self):
        self.STORAGE.JSON = {
            "a": 1,
            "b": {
                "c": "cat",
                "d": {
                    "e": {}
                }
            }
        }

        self.assertTrue(self.STORAGE.is_empty("b/d/e"))
        self.assertFalse(self.STORAGE.is_empty("a"))

    def test_make(self):
        self.STORAGE.JSON = {
            "a": 1,
            "b": {
                "c": "cat",
                "d": {
                    "e": True
                }
            }
        }

        self.assertFalse(self.STORAGE.exists("b/d/f"))
        self.STORAGE.make("b/d/f")
        self.assertTrue(self.STORAGE.exists("b/d/f"))
        self.assertTrue(self.STORAGE.is_empty("b/d/f"))

    def test_list_nodes(self):
        self.STORAGE.JSON = {
            "a": 1,
            "b": {
                "c": "cat",
                "d": {
                    "e": True
                }
            }
        }

        self.assertEqual(["a", "b"], self.STORAGE.list_nodes())
        self.assertEqual([], self.STORAGE.list_nodes("b/d/e"))

    def test_reset(self):
        self.STORAGE.JSON = {
            "a": 1,
            "b": {
                "c": "cat",
                "d": {
                    "e": True
                }
            }
        }

        self.STORAGE.reset()
        self.assertEqual({}, self.STORAGE.JSON)

    def test_save(self):
        self.STORAGE.JSON = {
            "a": 1,
            "b": {
                "c": "cat",
                "d": {
                    "e": True
                }
            }
        }

        self.STORAGE.write({"g": [1, 2, 3]}, "b/d/f")
        self.STORAGE.save()
        self.assertEqual({
            "a": 1,
            "b": {
                "c": "cat",
                "d": {
                    "e": True,
                    "f": {
                        "g": [1, 2, 3]
                    }
                }
            }
        }, self.STORAGE.JSON)

        old_storage_json = self.STORAGE.JSON

        self.STORAGE.JSON = {}
        self.STORAGE.load()

        self.assertEqual(old_storage_json, self.STORAGE.JSON)

    def test_change_root(self):
        self.STORAGE.reset()
        self.assertEqual({}, self.STORAGE.read())
        self.assertEqual(self.ROOT, self.STORAGE.ROOT)

        self.STORAGE.write("test", "a/b/c")

        self.assertEqual({
            'a': {
                'b': {
                    'c': 'test'
                }
            }
        }, self.STORAGE.JSON)
        self.assertEqual("test", self.STORAGE.read("a/b/c"))

        json_i = self.STORAGE.JSON
        self.STORAGE.change_ref("a/b")
        json_f = self.STORAGE.JSON

        self.assertEqual(json_i, json_f)
        self.assertEqual(["c"], self.STORAGE.list_nodes())
        self.assertEqual("test", self.STORAGE.read("c"))

        self.STORAGE.write(42, "d/e")
        self.assertEqual(["c", "d"], self.STORAGE.list_nodes())
        self.assertEqual(42, self.STORAGE.read("d/e"))

        json_i = self.STORAGE.JSON
        self.STORAGE.change_ref("d")
        json_f = self.STORAGE.JSON

        self.assertEqual(json_i, json_f)
        self.assertEqual(["e"], self.STORAGE.list_nodes())
        self.assertEqual(42, self.STORAGE.read("e"))

        json_i = self.STORAGE.JSON
        self.STORAGE.change_ref("", reset=True)
        json_f = self.STORAGE.JSON

        self.assertEqual(json_i, json_f)
        self.STORAGE.save()
