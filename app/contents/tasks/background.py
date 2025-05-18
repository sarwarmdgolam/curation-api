from celery import shared_task

from app.contents.ai import summarize_with_groq, analyze_sentiment_with_groq, extract_topics_with_groq
from app.contents.models import Content


@shared_task
def process_content(content_id):
    try:
        content = Content.objects.get(id=content_id)
        print('content:', content)
        content.summary = summarize_with_groq(content.body)
        content.sentiment = analyze_sentiment_with_groq(content.body)
        content.topics = extract_topics_with_groq(content.body)
        content.save()
    except Content.DoesNotExist:
        pass