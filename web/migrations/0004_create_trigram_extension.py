from django.contrib.postgres.operations import TrigramExtension
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [('web', '0003_create_text_search_trigger')]
    operations = [TrigramExtension()]
