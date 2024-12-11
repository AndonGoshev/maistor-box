from django.core.management import BaseCommand, call_command

from maistorbox.common.management.commands import populate_region_and_specialization_models, populate_base_user_model, \
    populate_contractor_user_model, populate_projects_for_all_of_the_contractor_model_instances, \
    populate_feedbacks_for_all_of_the_contractor_public_instances, create_company, create_groups


class Command(BaseCommand):
    help = 'Run all start-up commands'

    def handle(self, *args, **options):
        commands_to_run = [
            'populate_region_and_specialization_models',
            'populate_base_user_model',
            'populate_contractor_user_model',
            'populate_projects_for_all_of_the_contractor_model_instances',
            'populate_feedbacks_for_all_of_the_contractor_public_instances',
            'create_company',
            'create_groups',
        ]

        for command in commands_to_run:
            self.stdout.write('fRunning command: {command}')
            try:
                call_command(command)
                self.stdout.write(self.style.SUCCESS(f'Successfully ran {command}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error running {command}: {e}'))