from typing import List, Dict
import tweepy
import linkedin_api
from datetime import datetime

class SocialMediaPost(BaseModel):
    platform: str
    content: str
    media: List[str] = []
    schedule: datetime = None

class PromotionEngine:
    def __init__(self, credentials: Dict[str, str]):
        self.twitter = tweepy.Client(
            consumer_key=credentials['twitter']['api_key'],
            consumer_secret=credentials['twitter']['api_secret'],
            access_token=credentials['twitter']['access_token'],
            access_token_secret=credentials['twitter']['access_secret']
        )
        self.linkedin = linkedin_api.LinkedIn(
            credentials['linkedin']['username'],
            credentials['linkedin']['password']
        )

    def schedule_post(self, post: SocialMediaPost) -> bool:
        if post.platform == 'twitter':
            return self._post_twitter(post)
        elif post.platform == 'linkedin':
            return self._post_linkedin(post)
        return False

    def _post_twitter(self, post: SocialMediaPost) -> bool:
        try:
            media_ids = [self.twitter.media_upload(m).media_id for m in post.media]
            self.twitter.create_tweet(
                text=post.content,
                media_ids=media_ids
            )
            return True
        except Exception as e:
            print(f"Twitter error: {str(e)}")
            return False