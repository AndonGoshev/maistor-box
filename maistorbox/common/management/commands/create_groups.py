from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management import BaseCommand


class Command(BaseCommand):
    help = 'Create admin groups and assign permissions.'

    def handle(self, *args, **kwargs):
        # Define groups and their specific permission types
        group_definitions = {
            'Super Admin': 'all_permissions',  # All permissions
            'Client Feedback Redactor': 'client_feedback_crud',  # CRUD for ClientFeedbackModel + view everything
            'Viewer': 'view_only',  # View-only permissions
        }

        # Define permission codenames for ClientFeedbackModel
        client_feedback_permissions = ['add_clientfeedbackmodel', 'change_clientfeedbackmodel',
                                        'delete_clientfeedbackmodel', 'view_clientfeedbackmodel']

        for group_name, permission_type in group_definitions.items():
            group, created = Group.objects.get_or_create(name=group_name)

            if created:
                self.stdout.write(self.style.SUCCESS(f'Group "{group_name}" created successfully'))
            else:
                self.stdout.write(self.style.WARNING(f'Group "{group_name}" already exists'))

            # Assign permissions based on the group type
            if permission_type == 'all_permissions':
                # Assign all permissions to Super Admin
                permissions = Permission.objects.all()
            elif permission_type == 'client_feedback_crud':
                # Fetch CRUD permissions for ClientFeedbackModel
                crud_permissions = Permission.objects.filter(codename__in=client_feedback_permissions)
                # Fetch all view permissions
                view_permissions = Permission.objects.filter(codename__startswith='view_')
                # Combine both permission sets
                permissions = crud_permissions | view_permissions
            elif permission_type == 'view_only':
                # Assign only view permissions for all models
                permissions = Permission.objects.filter(codename__startswith='view_')
            else:
                permissions = []

            # Assign permissions to the group
            group.permissions.set(permissions)
            self.stdout.write(self.style.SUCCESS(f'Permissions assigned to group "{group_name}"'))



