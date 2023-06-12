import unittest

from request import *

class RequestTestCase(unittest.TestCase):
    def setUp(self):
        self.request = Request(1, 2, 3, "Test purpose")

    def test_initial_state(self):
        self.assertFalse(self.request.solved)
        self.assertFalse(self.request.approved)
        self.assertFalse(self.request.rejected)
        self.assertEqual(self.request.equipment_id, 2)
        self.assertEqual(self.request.purpose, "Test purpose")
        self.assertEqual(self.request.sender_id, 1)
        self.assertEqual(self.request.count, 3)
        self.assertEqual(self.request.approved_id, 0)
        self.assertFalse(self.request.notified)
        self.assertFalse(self.request.taken)

    def test_approve(self):
        self.request.approve(4)
        self.assertTrue(self.request.solved)
        self.assertTrue(self.request.approved)
        self.assertEqual(self.request.approved_id, 4)

    def test_reject(self):
        self.request.reject(5)
        self.assertTrue(self.request.solved)
        self.assertTrue(self.request.rejected)
        self.assertEqual(self.request.approved_id, 5)

if __name__ == "__main__":
    unittest.main()