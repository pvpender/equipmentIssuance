import unittest
from accesses import *


class TestAdminAccess(unittest.TestCase):

    def test_admin_access_properties(self):
        groups = ['group1', 'group2']
        can_add_users = True
        can_change_users = False
        can_add_inventory = True
        can_change_inventory = True
        can_get_request = False

        admin_access = AdminAccess(groups, can_add_users, can_change_users, can_add_inventory, can_change_inventory, can_get_request)

        self.assertEqual(admin_access.groups, groups)
        self.assertEqual(admin_access.can_add_users, can_add_users)
        self.assertEqual(admin_access.can_change_users, can_change_users)
        self.assertEqual(admin_access.can_add_inventory, can_add_inventory)
        self.assertEqual(admin_access.can_change_inventory, can_change_inventory)
        self.assertEqual(admin_access.can_get_request, can_get_request)

    def test_admin_access_inherits_from_access(self):
        groups = ['group1', 'group2']
        can_add_users = True
        can_change_users = False
        can_add_inventory = True
        can_change_inventory = True
        can_get_request = False

        admin_access = AdminAccess(groups, can_add_users, can_change_users, can_add_inventory, can_change_inventory,
                                   can_get_request)

        self.assertIsInstance(admin_access, Access)

if __name__ == '__main__':
    unittest.main()








