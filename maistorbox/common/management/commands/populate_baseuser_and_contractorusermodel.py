import os
import random

from django.contrib.auth.hashers import make_password
from django.core.management import BaseCommand

from maistorbox import settings
from maistorbox.accounts.choices import UserTypeChoice
from maistorbox.accounts.models import Regions, Specializations, BaseUserModel, ContractorUserModel

names = [
    ("Александър", "Александров"), ("Ангел", "Ангелов"), ("Асен", "Асенов"),
    ("Благой", "Богданов"), ("Богдан", "Борисов"), ("Борислав", "Георгиев"),
    ("Боян", "Димитров"), ("Дамян", "Добрев"), ("Данаил", "Драгомиров"),
    ("Димитър", "Емилов"), ("Емил", "Живков"), ("Живко", "Иванов"),
    ("Ивайло", "Калоянов"), ("Иван", "Кирилов"), ("Калоян", "Костадинов"),
    ("Кирил", "Красимиров"), ("Костадин", "Лазаров"), ("Красимир", "Мартинов"),
    ("Лазар", "Миленов"), ("Мартин", "Мирославов"), ("Милен", "Николов"),
    ("Мирослав", "Огнянов"), ("Николай", "Петров"), ("Петър", "Пламенов"),
    ("Пламен", "Радославов"),
    ("Александра", "Александрова"), ("Анастасия", "Ангелова"), ("Биляна", "Асенова"),
    ("Боряна", "Богданова"), ("Ваня", "Борисова"), ("Виктория", "Георгиева"),
    ("Гергана", "Димитрова"), ("Десислава", "Добрева"), ("Диана", "Драгомирова"),
    ("Елена", "Емилова"), ("Жана", "Живкова"), ("Златина", "Иванова"),
    ("Илияна", "Калоянова"), ("Йоана", "Кирилова"), ("Катерина", "Костадинова"),
    ("Кристина", "Красимирова"), ("Лиляна", "Лазарова"), ("Мария", "Мартинова"),
    ("Милена", "Миленова"), ("Надежда", "Мирославова"), ("Николина", "Николова"),
    ("Петя", "Огнянова"), ("Ралица", "Петрова"), ("Росица", "Пламенова"),
    ("Светлана", "Радославова")
]

class Command(BaseCommand):
    help = 'Populate the database with contractor users'

    def handle(self, *args, **kwargs):
        media_dir = settings.MEDIA_ROOT
        profile_images_media_folder = os.path.join(media_dir, 'test_profile_images')

        if not os.path.exists(profile_images_media_folder):
            self.stdout.write(self.style.ERROR(f"Profile images folder not found: {profile_images_media_folder}"))
            return

        # Generate the list of profile picture URLs using MEDIA_URL
        profile_pictures_urls = [os.path.join('test_profile_images', image) for image in
                                 os.listdir(profile_images_media_folder)]

        # Fetch all regions and specializations for random assignment
        all_regions = Regions.objects.all()
        all_specializations = Specializations.objects.all()

        # Number of users to create
        num_users = 50

        for _ in range(num_users):
            # Randomly select first name and last name
            first_name, last_name = random.choice(names)

            # Create a Base User
            base_user = BaseUserModel.objects.create(
                username=f'contractor{_ + 1}',
                email=f'user{_ + 1}@example.com',
                password=make_password('password123'),  # You can use a default password
                first_name=first_name,
                last_name=last_name,
                user_type=UserTypeChoice.CONTRACTOR_USER,  # Assuming user_type for contractor
            )

            # Create a Contractor User
            contractor_user = ContractorUserModel.objects.create(
                user=base_user,
                about_me='Имам опит в майсторенето повече от 25 години, като през последните 10 съм и учител в техникум по дървообработване.',
                phone_number=f'+35912345678{_ + 1}',  # Example phone number
                profile_image=random.choice(profile_pictures_urls),  # Placeholder for image
            )

            # Assign 3 random regions and 3 random specializations to the contractor user
            contractor_user.regions.set(random.sample(list(all_regions), 3))
            contractor_user.specializations.set(random.sample(list(all_specializations), 3))

            contractor_user.save()

            # Output information about the created user
            self.stdout.write(self.style.SUCCESS(f"Created BaseUser(type=contractor) with username: {base_user.username}"))