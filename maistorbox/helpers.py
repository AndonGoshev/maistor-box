from maistorbox.accounts.models import BaseUserModel


def last_model_instance_created(model):
    last_model_instance = model.objects.last()
    if last_model_instance:
        return last_model_instance.id

    return 0


def select_all_option_instance_id(model):
    return model.objects.filter(name='Изберете всички').first()