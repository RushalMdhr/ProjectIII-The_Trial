from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0003_chatsession_use_case'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatsession',
            name='current_difficulty',
            field=models.CharField(choices=[('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')], default='easy', max_length=10),
        ),
        migrations.AddField(
            model_name='chatsession',
            name='halted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='chatsession',
            name='interview_difficulty',
            field=models.CharField(choices=[('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')], default='medium', max_length=10),
        ),
        migrations.AddField(
            model_name='chatsession',
            name='interview_role',
            field=models.CharField(blank=True, max_length=150),
        ),
        migrations.AddField(
            model_name='chatsession',
            name='max_questions',
            field=models.PositiveSmallIntegerField(default=8),
        ),
        migrations.AddField(
            model_name='chatsession',
            name='question_count',
            field=models.PositiveSmallIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='chatmessage',
            name='evaluation_feedback',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='chatmessage',
            name='evaluation_rating',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='chatmessage',
            name='question_answer',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='chatmessage',
            name='question_difficulty',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='chatmessage',
            name='question_text',
            field=models.TextField(blank=True, null=True),
        ),
    ]