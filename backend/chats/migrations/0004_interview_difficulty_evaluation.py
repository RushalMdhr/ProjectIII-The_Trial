from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("chats", "0003_chatsession_use_case"),
    ]

    operations = [
        migrations.AddField(
            model_name="chatsession",
            name="interview_difficulty",
            field=models.CharField(
                choices=[
                    ("easy", "Easy"),
                    ("medium", "Medium"),
                    ("hard", "Hard"),
                ],
                default="medium",
                max_length=10,
            ),
        ),
        migrations.CreateModel(
            name="InterviewEvaluation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("score", models.PositiveSmallIntegerField()),
                ("difficulty", models.CharField(max_length=10)),
                ("feedback", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "message",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="interview_evaluation",
                        to="chats.chatmessage",
                    ),
                ),
                (
                    "session",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="interview_evaluations",
                        to="chats.chatsession",
                    ),
                ),
            ],
        ),
    ]
