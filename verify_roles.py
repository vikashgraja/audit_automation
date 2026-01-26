import os
import secrets
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "audit_automation.settings")
django.setup()


def verify():
    from django.contrib.auth.models import Group

    from user_management.models import User, UserExactRoles

    print("Verifying Roles and Privileges...")

    # Clean up previous test
    User.objects.filter(employee_id=99999).delete()

    # 1. Create a Vertical Head User
    password = secrets.token_urlsafe(16)
    user = User.objects.create_user(
        employee_id=99999,
        first_name="Test",
        last_name="User",
        role=UserExactRoles.VERTICAL_HEAD,
        password=password,
    )
    print(f"Created User: {user} with Role: {user.role}")

    # 2. Assign Site Admin Group
    site_admin_group = Group.objects.get(name="Site Admin")
    user.groups.add(site_admin_group)
    print(f"Assigned Group: {site_admin_group.name}")

    # 3. Verify
    user.refresh_from_db()

    is_vertical_head = user.role == UserExactRoles.VERTICAL_HEAD
    is_site_admin = user.groups.filter(name="Site Admin").exists()

    print(f"Is Vertical Head: {is_vertical_head}")
    print(f"Is Site Admin (Group): {is_site_admin}")

    if is_vertical_head and is_site_admin:
        print("SUCCESS: User acts as both Vertical Head and Site Admin.")
    else:
        print("FAILURE: Roles/Groups mismatch.")


if __name__ == "__main__":
    verify()
