from django.contrib.auth.hashers import make_password
from django.core.management import BaseCommand

from maistorbox.accounts.models import BaseUserModel


class Command(BaseCommand):
    help = ('Populate base_footer_header user model. The need for base_footer_header users in the project comes for the '
            'randomness of the given feedbacks. Some feedbacks will be from contractors and '
            'some of them will be from regular users.')

    def handle(self, *args, **options):

        # Number of base_footer_header users to be created
        NUM_OF_BASE_USERS = 20

        for _ in range(NUM_OF_BASE_USERS):

            new_regular_user = BaseUserModel.objects.create_user(
                username=f'regular_user{_ + 1}',
                email=f'regular_user{_ + 1}@testmail.com',
                password='password123',
            )

            new_regular_user.save()

            self.stdout.write(
                self.style.SUCCESS(f"Created BaseUser with username: {new_regular_user.username}"))
