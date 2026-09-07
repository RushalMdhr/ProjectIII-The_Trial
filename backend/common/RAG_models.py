from django.db import models
from pgvector.django import VectorField
from chats.models import ChatSession, ChatMessage


class Document_Source(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class InterviewQuestions(models.Model):
    question = models.TextField()
    answer = models.TextField()
    role = models.CharField(max_length=255, db_index=True)
    experience = models.CharField(max_length=50, choices=[
        ('none', 'None'),
        ('intern', 'Intern'),
        ('junior', 'Junior'),
        ('mid_level', 'Mid-level'),
        ('senior', 'Senior'),
        ('any', 'Any')
    ],db_index=True)
    difficulty = models.CharField(max_length=50, choices=[
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard')
    ])
    keywords = models.JSONField(default=list)  # or ArrayField
    source = models.ForeignKey(Document_Source, on_delete=models.CASCADE, related_name='questions')
    embedding = VectorField(dimensions=768, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question[:50]

class AskedQuestions(models.Model):
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='asked_questions')
    question = models.ForeignKey(InterviewQuestions, on_delete=models.CASCADE)
    asked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('session', 'question')

    def __str__(self):
        return f"Session {self.session.id} - Question {self.question.id}"