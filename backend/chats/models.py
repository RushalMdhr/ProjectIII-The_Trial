from django.db import models
from pgvector.django import VectorField


class ChatSession(models.Model):

    DIFFICULTY_CHOICES = [
        ("easy", "Easy"),
        ("medium", "Medium"),
        ("hard", "Hard"),
    ]

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
        choices=DIFFICULTY_CHOICES,
        default="medium",
    )
    current_difficulty = models.CharField(
        max_length=10,
        choices=DIFFICULTY_CHOICES,
        default="easy",
    )
    max_questions = models.PositiveSmallIntegerField(default=8)
    question_count = models.PositiveSmallIntegerField(default=0)
    interview_role = models.CharField(max_length=150, blank=True)
    halted = models.BooleanField(default=False)

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
    question_text = models.TextField(blank=True, null=True)
    question_answer = models.TextField(blank=True, null=True)
    question_difficulty = models.CharField(max_length=10, blank=True, null=True)
    evaluation_rating = models.PositiveSmallIntegerField(blank=True, null=True)
    evaluation_feedback = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Message {self.id} - Session {self.session.id}"


class InterviewFeedback(models.Model):
    session = models.ForeignKey(
        ChatSession,
        on_delete=models.CASCADE,
        related_name='interview_feedbacks'
    )
    message = models.ForeignKey(
        ChatMessage,
        on_delete=models.CASCADE,
        related_name='interview_feedbacks'
    )
    rating = models.PositiveSmallIntegerField()
    feedback = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('session', 'message')

    def __str__(self):
        return f"Feedback {self.id} - Session {self.session_id} - Message {self.message_id}"