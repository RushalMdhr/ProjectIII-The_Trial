# In your app's migrations/0002_enable_pgvector.py
from django.db import migrations
from pgvector.django import VectorExtension

class Migration(migrations.Migration):
    dependencies = [
        ('common', '0004_alter_simpletextembedding_embedding'),
    ]
    operations = [
        VectorExtension(),  # Runs CREATE EXTENSION IF NOT EXISTS vector
    ]