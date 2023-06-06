import unittest
import tempfile
import os.path
import json

from user_emails import UserEmails


class TestUserEmails(unittest.TestCase):
    def setUp(self):
        self.emails = UserEmails.from_file('emails.txt')

    def test_from_file(self):
        self.assertEqual(len(self.emails), 4)
        self.assertIn('bole@example.com', self.emails)
        self.assertIn('tesa@example.com', self.emails)
        self.assertIn('jeca@example.com', self.emails)
        self.assertIn('mari@example.com', self.emails)

    def test_from_json(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(['kris@example.com', 'zile@example.com'], f)
        try:
            path = f.name
            emails = UserEmails.from_json(path)
            self.assertEqual(len(emails), 2)
            self.assertIn('kris@example.com', emails)
            self.assertIn('zile@example.com', emails)
        finally:
            os.unlink(path)

    def test_union(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(['tesa@example.com', 'kris@example.com'], f)
        try:
            path = f.name
            other_emails = UserEmails.from_json(path)
            union_emails = self.emails.union(other_emails)
            self.assertEqual(len(union_emails), 5)
            self.assertIn('tesa@example.com', union_emails)
            self.assertIn('kris@example.com', union_emails)
            self.assertIn('bole@example.com', union_emails)
            self.assertIn('jeca@example.com', union_emails)
            self.assertIn('mari@example.com', union_emails)
        finally:
            os.unlink(path)


if __name__ == '__main__':
    unittest.main()


