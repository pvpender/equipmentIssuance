import unittest
from unittest.mock import MagicMock
from user_collections import *
class TestUserCollection(unittest.TestCase):

    def setUp(self):
        self.db_mock = MagicMock()
        self.user_collection = UserCollection(self.db_mock)

    def test_count(self):
        self.assertEqual(self.user_collection.count, 0)

    def test_append_user_common_user(self):
        user = CommonUser(12345, "test@example.com", Access([1, 2]))
        self.db_mock.add_user.return_value = 1
        self.db_mock.get_user_by_mail.return_value.id = 1

        self.user_collection.append_user(user)

        self.assertEqual(self.user_collection.count, 1)
        self.assertEqual(self.user_collection.get_user_by_pass(12345), user)
        self.assertIsNotNone(self.user_collection.get_user_by_group(12345))
        self.assertEqual(self.user_collection.get_user_by_mail("test@example.com"), user)
        self.assertTrue(self.user_collection.check_user_by_mail("test@example.com"))

        self.db_mock.add_user.assert_called_once_with(user)
        self.db_mock.get_user_by_mail.assert_called_once_with("test@example.com")

    def test_append_user_admin(self):
        user = Admin(54321, "admin@example.com", AdminAccess([1, 2], True, True, True, True, True))
        self.db_mock.add_admin.return_value = 1
        self.db_mock.get_admin_by_mail.return_value.id = 1

        self.user_collection.append_user(user)

        self.assertEqual(self.user_collection.count, 1)
        self.assertEqual(self.user_collection.get_user_by_pass(54321), user)
        self.assertIsNotNone(self.user_collection.get_user_by_group(54321))
        self.assertEqual(self.user_collection.get_user_by_mail("admin@example.com"), user)
        self.assertTrue(self.user_collection.check_user_by_mail("admin@example.com"))

        self.db_mock.add_admin.assert_called_once_with(user)
        self.db_mock.get_admin_by_mail.assert_called_once_with("admin@example.com")

    def test_change_user_common_user(self):
        old_user = CommonUser(12345, "old@example.com", Access([1, 2]))
        new_user = CommonUser(12345, "new@example.com", Access([3, 4]))

        self.db_mock.get_user_by_mail.return_value.id = 1

        self.user_collection.append_user(old_user)
        self.user_collection.change_user(12345, "new@example.com", new_user)

        self.assertEqual(self.user_collection.count, 1)
        self.assertEqual(self.user_collection.get_user_by_pass(12345), new_user)
        self.assertEqual(self.user_collection.get_user_by_mail("new@example.com"), new_user)

        self.db_mock.update_user.assert_called_once_with(12345, "new@example.com", new_user)
        self.assertNotIn(12345, self.user_collection.get_user_list())

    def test_change_user_admin(self):
        old_user = Admin(54321, "old@example.com", AdminAccess([1, 2], True, True, True, True, True))
        new_user = Admin(54321, "new@example.com", AdminAccess([3, 4], False, False, False, False, False))

        self.db_mock.get_admin_by_mail.return_value.id = 1

        self.user_collection.append_user(old_user)
        self.user_collection.change_user(54321, "new@example.com", new_user)

        self.assertEqual(self.user_collection.count, 1)
        self.assertEqual(self.user_collection.get_user_by_pass(54321), new_user)
        self.assertEqual(self.user_collection.get_user_by_mail("new@example.com"), new_user)

        self.db_mock.update_admin.assert_called_once_with(54321, "new@example.com", new_user)
        self.assertNotIn(54321, self.user_collection.get_user_list())

    def test_del_user_common_user(self):
        user = CommonUser(12345, "test@example.com", Access([1, 2]))
        self.db_mock.get_user_by_mail.return_value.id = 1

        self.user_collection.append_user(user)
        self.user_collection.del_user(12345)

        self.assertEqual(self.user_collection.count, 0)
        self.assertIsNone(self.user_collection.get_user_by_id(12345))
        self.assertFalse(self.user_collection.get_user_by_group(12345))
        self.assertIsNone(self.user_collection.get_user_by_mail("test@example.com"))
        self.assertFalse(self.user_collection.check_user_by_mail("test@example.com"))

        self.db_mock.delete_user.assert_called_once_with(user)
        self.assertNotIn(12345, self.user_collection.get_user_list())

    def test_del_user_admin(self):
        user = Admin(54321, "admin@example.com", AdminAccess([1, 2], True, True, True, True, True))
        self.db_mock.get_admin_by_mail.return_value.id = 1

        self.user_collection.append_user(user)
        self.user_collection.del_user(54321)

        self.assertEqual(self.user_collection.count, 0)
        self.assertIsNone(self.user_collection.get_user_by_id(54321))
        self.assertFalse(self.user_collection.get_user_by_group(54321))
        self.assertIsNone(self.user_collection.get_user_by_mail("admin@example.com"))
        self.assertFalse(self.user_collection.check_user_by_mail("admin@example.com"))

        self.db_mock.delete_admin.assert_called_once_with(user)
        self.assertNotIn(54321, self.user_collection.get_user_list())

    def test_add_groups(self):
        user = CommonUser(12345, "test@example.com", Access([1, 2, 3]))
        groups = [3, 4]

        self.db_mock.get_user_by_mail.return_value.id = 1

        self.user_collection.append_user(user)
        self.user_collection.add_groups(12345, groups)

        self.assertEqual(self.user_collection.get_user_by_pass(12345).access.groups, [1, 2, 3, 4])
        self.db_mock.add_user_group.assert_called_once_with(1, 4)

    def test_del_groups(self):
        user = CommonUser(12345, "test@example.com", Access([1, 2, 3, 4]))
        groups = [2, 3, 4]

        self.db_mock.get_user_by_mail.return_value.id = 1

        self.user_collection.append_user(user)
        self.user_collection.del_groups(12345, groups)

        self.assertEqual(self.user_collection.get_user_by_pass(12345).access.groups, [1])

    def test_get_user_by_group(self):
        user1 = CommonUser(12345, "user1@example.com", Access([1, 2, 3]))
        user2 = CommonUser(54321, "user2@example.com", Access([2, 4]))
        user3 = Admin(98765, "admin@example.com", AdminAccess([1, 4], True, True, True, True, True))

        self.db_mock.get_user_by_mail.return_value.id = 1

        self.user_collection.append_user(user1)
        self.user_collection.append_user(user2)
        self.user_collection.append_user(user3)

        self.assertEqual(self.user_collection.get_user_by_group(2), [user1, user2])
        self.assertEqual(self.user_collection.get_user_by_group(1), [user1, user3])
        self.assertEqual(self.user_collection.get_user_by_group(4), [user2, user3])
        self.assertEqual(self.user_collection.get_user_by_group(3), [user1])

if __name__ == '__main__':
    unittest.main()
