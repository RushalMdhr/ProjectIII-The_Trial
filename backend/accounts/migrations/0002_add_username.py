import django.contrib.auth.validators
from django.db import migrations, models
from django.utils.translation import gettext_lazy as _


def populate_usernames(apps, schema_editor):
    User = apps.get_model('accounts', 'User')
    used_usernames = set(
        User.objects.exclude(username__isnull=True).values_list('username', flat=True)
    )

    for user in User.objects.filter(username__isnull=True).order_by('id'):
        base = user.email.split('@', 1)[0] or f'user{user.id}'
        username = base[:150]
        suffix = 1
        while username in used_usernames:
            suffix_text = str(suffix)
            username = f'{base[:150 - len(suffix_text)]}{suffix_text}'
            suffix += 1
        user.username = username
        user.save(update_fields=['username'])
        used_usernames.add(username)


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.CharField(
                error_messages={'unique': 'A user with that username already exists.'},
                help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
                max_length=150,
                null=True,
                validators=[django.contrib.auth.validators.UnicodeUsernameValidator()],
                verbose_name=_('username'),
            ),
        ),
        migrations.RunPython(populate_usernames, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(
                error_messages={'unique': 'A user with that username already exists.'},
                help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
                max_length=150,
                unique=True,
                validators=[django.contrib.auth.validators.UnicodeUsernameValidator()],
                verbose_name=_('username'),
            ),
        ),
    ]