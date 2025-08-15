from django.contrib.auth.models import Permission, Group, User
from django.contrib.contenttypes.models import ContentType


manager_group, created = Group.objects.get_or_create(name="Managers")


content_type = ContentType.objects.get_for_model(User)
view_all = Permission.objects.get(codename="can_view_all")
is_manager = Permission.objects.get(codename="is_manager")


manager_group.permissions.add(view_all, is_manager)

# Assign user to group
user = User.objects.get(email="ekaterina.kuz@gmail.com")
user.groups.add(manager_group)
user.save()
