import os
import random

from django.conf.urls.static import static
import django

from maistorbox.settings import STATICFILES_DIRS

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'maistorbox.settings')
django.setup()

# static_dir = STATICFILES_DIRS[0]
#
# profile_pictures_static_folder = os.path.join(static_dir, 'testing_media', 'profile_pictures')
# project_pictures_static_folder = os.path.join(static_dir, 'testing_media', 'project_pictures')
#
# profiles_pictures_absolute_path = os.path.abspath(profile_pictures_static_folder)
# project_pictures_absolute_path = os.path.abspath(project_pictures_static_folder)
#
# profile_pictures_urls = [os.path.join(profiles_pictures_absolute_path, image) for image in os.listdir(profiles_pictures_absolute_path)]
# project_pictures_urls = [os.path.join(project_pictures_absolute_path, image) for image in os.listdir(project_pictures_absolute_path)]

a = [1, 4, 5, 2, 7]

# Select a random item
random_num = random.choice(a)
print(type(random_num))