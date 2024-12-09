import os
import random

from django.core.management import BaseCommand

from maistorbox import settings
from maistorbox.accounts.models import ContractorUserModel, ContractorProjectModel, ImageModel


class Command(BaseCommand):
    help = 'Populate all ContractorProject objects'

    def handle(self, *args, **kwargs):
        potential_number_of_projects_per_contractor = [3, 4, 5]
        potential_number_of_images_per_project = [6, 7, 8]

        project_name = 'Ремонт на обект'
        project_description = 'Това е примерно описание за текущия проект. Работихме здраво на работната площадка. Резултатите са на лице както можете да видите от снимките приложение към проекта!'
        average_price_for_similar_project = 100

        image_caption = 'Това е коментар за снимката.'

        media_dir = settings.MEDIA_ROOT
        project_images_media_folder = os.path.join(media_dir, 'test_project_images')

        if not os.path.exists(project_images_media_folder):
            self.stdout.write(self.style.ERROR(f"Project images folder not found: {project_images_media_folder}"))
            return

        project_images_urls = [os.path.join('test_project_images', image) for image in
                               os.listdir(project_images_media_folder)]


        all_contractors = ContractorUserModel.objects.all()

        for contractor in all_contractors:
            num_of_projects_per_contractor = random.choice(potential_number_of_projects_per_contractor)

            for _ in range(num_of_projects_per_contractor):

                curr_project = ContractorProjectModel.objects.create(
                    project_name=project_name,
                    project_description=project_description,
                    average_price_for_similar_project=average_price_for_similar_project,
                    contractor_user=contractor,
                )

                curr_project.save()

                self.stdout.write(self.style.SUCCESS(f"Created project for {contractor.user.first_name}."))

                num_of_images_per_project = random.choice(potential_number_of_images_per_project)

                for _ in range(num_of_images_per_project):

                    curr_image = ImageModel.objects.create(
                        image=random.choice(project_images_urls),
                        image_caption=image_caption,
                        contractor_project=curr_project,
                    )

                    curr_image.save()

                    self.stdout.write(self.style.SUCCESS(f"Uploaded image for project with id: {curr_project.id}."))
