from django.db import migrations


def migrate_roles(apps, schema_editor):
    User = apps.get_model("user_management", "User")
    Group = apps.get_model("auth", "Group")

    # Create Site Admin group if it doesn't exist
    site_admin_group, created = Group.objects.get_or_create(name="Site Admin")

    for user in User.objects.all():
        save_needed = False
        if user.role == "HoD":
            user.role = "Domain Head"
            save_needed = True
        elif user.role == "HoS":
            user.role = "Sub Domain Head"
            save_needed = True
        elif user.role == "Site Admin":
            user.groups.add(site_admin_group)
            user.role = None
            save_needed = True

        if save_needed:
            user.save()


def reverse_migrate_roles(apps, schema_editor):
    User = apps.get_model("user_management", "User")

    # We can try to revert names, but reverting assignments from group back to role is tricky
    # if users have both. For this specific task, we'll just revert names.
    # Site Admin reversion is best effort.

    for user in User.objects.all():
        save_needed = False
        if user.role == "Domain Head":
            user.role = "HoD"
            save_needed = True
        elif user.role == "Sub Domain Head":
            user.role = "HoS"
            save_needed = True

        # Check if user is in Site Admin group and has no role, maybe they were a Site Admin
        # This part is ambiguous in reverse, so we might skip automatic full reversion of Site Admin
        # to avoid data loss if they were legitimately just a group member.

        if save_needed:
            user.save()


class Migration(migrations.Migration):
    dependencies = [
        ("user_management", "0007_user_groups_user_user_permissions_alter_user_role"),
    ]

    operations = [
        migrations.RunPython(migrate_roles, reverse_migrate_roles),
    ]
