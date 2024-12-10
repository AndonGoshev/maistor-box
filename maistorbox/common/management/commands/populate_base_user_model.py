from django.core.management import BaseCommand

from maistorbox.accounts.models import BaseUserModel
from maistorbox.helpers import last_model_instance_created


class Command(BaseCommand):
    help = ('Populate base user model. The need for base_footer_header users in the project comes for the '
            'randomness of the given feedbacks. Some feedbacks will be from contractors and '
            'some of them will be from regular users.')

    def handle(self, *args, **options):

        # Number of regular users to be created
        NUM_OF_REGULAR_USERS = 20

        for user_num in range(last_model_instance_created(BaseUserModel), last_model_instance_created(BaseUserModel) + NUM_OF_REGULAR_USERS):

            new_regular_user = BaseUserModel.objects.create_user(
                username=f'regular_user{user_num + 1}',
                email=f'regular_user{user_num + 1}@testmail.com',
                password='password123',
            )

            new_regular_user.save()

            self.stdout.write(
                self.style.SUCCESS(f"Created BaseUser with username: {new_regular_user.username}"))
