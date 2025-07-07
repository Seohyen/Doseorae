from .models import Hashtag

def create_or_get_hashtags(hashtag_names):
    hashtags = []
    for name in hashtag_names:
        hashtag, created = Hashtag.objects.get_or_create(name=name)
        hashtags.append(hashtag)
    return hashtags

def process_hashtags(input_str):
    if not input_str.strip():
        return []
    tags = input_str.strip().split()
    hashtag_names = [tag.lstrip('#') for tag in tags if tag.strip() != '']
    return create_or_get_hashtags(hashtag_names)
