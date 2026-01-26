import os
import secrets
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "audit_automation.settings")
django.setup()


def verify_ui_logic():
    from django.contrib.auth.models import Group
    from user_management.models import User

    print("Verifying Privilege Management Logic...")

    # 1. Create a "UI Test Privilege" Group
    group_name = "UI Test Privilege"
    Group.objects.filter(name=group_name).delete()
    group = Group.objects.create(name=group_name)
    print(f"Created Group: {group.name}")

    # 2. Assign to a User (Simulating Form save)
    user = User.objects.filter(employee_id=99999).first()
    if not user:
        print("User 99999 not found, creating...")
        password = secrets.token_urlsafe(16)
        user = User.objects.create_user(employee_id=99999, password=password, role="Auditor")

    user.groups.add(group)
    user.save()
    print(f"Assigned {group.name} to User {user.employee_id}")

    # 3. List Logic (Simulating privilege_list view)
    groups = Group.objects.all()
    found = False
    for g in groups:
        member_count = g.user_set.count()
        if g.name == group_name:
            found = True
            print(f"List View Check: Group '{g.name}' has {member_count} members.")
            if member_count >= 1:
                print("SUCCESS: Member count reflected correctly.")
            else:
                print("FAILURE: Member count incorrect.")

    if found:
        print("SUCCESS: Group found in list.")
    else:
        print("FAILURE: Group not found in list.")

    # Cleanup
    group.delete()
    print("Cleanup done.")


if __name__ == "__main__":
    verify_ui_logic()
