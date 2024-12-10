from django.core.management import BaseCommand

from maistorbox.company.models import CompanyModel


class Command(BaseCommand):
    def handle(self, *args, **options):
        company = CompanyModel.objects.create(
            name='MaistorBox',
            phone_number='089 89 89 889',
            email='maistorbox@gmail.com',
            address='Бул. Източен 101, Пловдив, България',
            instagram_page_url='https://www.instagram.com',
            facebook_page_url='https://www.facebook.com',
            linkedin_page_url='https://www.linkedin.com',
        )

        company.save()

        self.stdout.write(self.style.SUCCESS(f'MaistorBox company was created!'))
