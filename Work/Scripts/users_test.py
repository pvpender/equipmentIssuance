import unittest

class AdminAccess:
    def __init__(self, groups):
        self.groups = groups


class Access:
    def __init__(self, groups):
        self.groups = groups


class Admin:
    def __init__(self, pass_number, mail, access: AdminAccess, base_id=None):
        self.pass_number = pass_number
        self.mail = mail
        self.access = access
        self.base_id = base_id

    def del_user(self):
        self.access = None


class CommonUser:
    def __init__(self, pass_number: int, mail: str, access: Access, base_id=None):
        self.pass_number = pass_number
        self.mail = mail
        self.access = access
        self.base_id = base_id

    def del_user(self):
        self.access = None


class TestAdmin(unittest.TestCase):

    def test_admin_properties(self):
        pass_number = 12345
        mail = "test@example.com"
        access = AdminAccess(groups=['group1', 'group2'])
        base_id = None

        admin = Admin(pass_number, mail, access, base_id)

        self.assertEqual(admin.pass_number, pass_number)
        self.assertEqual(admin.mail, mail)
        self.assertEqual(admin.base_id, base_id)
        self.assertEqual(admin.access, access)

    def test_admin_property_setters(self):
        pass_number = 12345
        mail = "test@example.com"
        access = AdminAccess(groups=['group1', 'group2'])
        base_id = None

        admin = Admin(pass_number, mail, access, base_id)

        new_pass_number = 54321
        new_mail = "new@example.com"
        new_access = AdminAccess(groups=['group3'])

        admin.pass_number = new_pass_number
        admin.mail = new_mail
        admin.access = new_access

        self.assertEqual(admin.pass_number, new_pass_number)
        self.assertEqual(admin.mail, new_mail)
        self.assertEqual(admin.access, new_access)

    def test_admin_del_user(self):
        pass_number = 12345
        mail = "test@example.com"
        access = AdminAccess(groups=['group1', 'group2'])
        base_id = None

        admin = Admin(pass_number, mail, access, base_id)

        admin.del_user()

        self.assertIsNone(admin.access)


class TestCommonUser(unittest.TestCase):

    def test_common_user_properties(self):
        pass_number = 12345
        mail = "test@example.com"
        access = Access(groups=['group1', 'group2'])
        base_id = None

        common_user = CommonUser(pass_number, mail, access, base_id)

        self.assertEqual(common_user.pass_number, pass_number)
        self.assertEqual(common_user.mail, mail)
        self.assertEqual(common_user.base_id, base_id)
        self.assertEqual(common_user.access, access)

    def test_common_user_property_setters(self):
        pass_number = 12345
        mail = "test@example.com"
        access = Access(groups=['group1', 'group2'])
        base_id = None

        common_user = CommonUser(pass_number, mail, access, base_id)

        new_pass_number = 54321
        new_mail = "new@example.com"
        new_access = Access(groups=['group3'])

        common_user.pass_number = new_pass_number
        common_user.mail = new_mail
        common_user.access = new_access

        self.assertEqual(common_user.pass_number, new_pass_number)
        self.assertEqual(common_user.mail, new_mail)
        self.assertEqual(common_user.access, new_access)

    def test_common_user_del_user(self):
        pass_number = 12345
        mail = "test@example.com"
        access = Access(groups=['group1', 'group2'])
        base_id = None

        common_user = CommonUser(pass_number, mail, access, base_id)

        common_user.del_user()

        self.assertIsNone(common_user.access)


if __name__ == '__main__':
    unittest.main()