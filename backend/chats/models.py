from django.db import models
from pgvector.django import VectorField


class ChatSession(models.Model):

    USE_CASE_CHOICES = [
        ("general_chat", "General Chat"),
        ("career_guidance", "Career Guidance"),
        ("interview_assessment", "Interview Assessment"),
    ]

    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='chat_sessions'
    )

    title = models.CharField(
        max_length=255,
        default='New Chat Session'
    )

    use_case = models.CharField(
        max_length=30,
        choices=USE_CASE_CHOICES,
        default="general_chat"
    )

    interview_difficulty = models.CharField(
        max_length=10,
        choices=(
            ("easy", "Easy"),
            ("medium", "Medium"),
            ("hard", "Hard"),
        ),
        default="medium",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    archived = models.BooleanField(default=False)

    def __str__(self):
        return f"Session {self.id} - {self.user.email}"


class ChatMessage(models.Model):
    session = models.ForeignKey(
        ChatSession,
        on_delete=models.CASCADE,
        related_name='messages'
    )
    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='chat_messages'
    )
    user_content = models.TextField(blank=True, null=True)
    assistant_content = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user_content_embedding = VectorField(dimensions=768, null=True, blank=True)

    def __str__(self):
        return f"Message {self.id} - Session {self.session.id}"


class InterviewEvaluation(models.Model):
    session = models.ForeignKey(
        ChatSession,
        on_delete=models.CASCADE,
        related_name="interview_evaluations",
    )
    message = models.OneToOneField(
        ChatMessage,
        on_delete=models.CASCADE,
        related_name="interview_evaluation",
    )
    score = models.PositiveSmallIntegerField()
    difficulty = models.CharField(max_length=10)
    feedback = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Interview evaluation {self.id}: {self.score}/10"