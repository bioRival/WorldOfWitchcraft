from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField


POST_CATEGORY = [
    ("TK", "Танки"),                # Tank
    ("HL", "Хилы"),                 # Healer
    ("DD", "ДД"),                   # Damage Dealer
    ("MT", "Торговцы"),             # Merchant
    ("GL", "Гилдмастеры"),          # Guildmaster
    ("QT", "Квестгиверы"),          # Questgiver
    ("SM", "Кузнецы"),              # Smith
    ("TN", "Кожевники"),            # Tanner
    ("AL", "Зельевары"),            # Alchemist
    ("MG", "Мастера Заклинаний"),   # Mage
]


class Author(models.Model):
    """
    Author. Model seems redundant rn, but would be needed for possible future features such as rating or statistics
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Post(models.Model):
    """
    Post - main content type, which consists of text, images and video
    """

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.CharField(max_length=2, choices=POST_CATEGORY)
    publication_date = models.DateField(auto_now_add=True)
    title = models.CharField(max_length=100)
    content = RichTextUploadingField(blank=True, null=True)
    reply_count = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    def preview(self):
        return self.content[:124] + "..."

class PostReply(models.Model):
    """
    Reply - a comment that any logged in user can leave under a post and any user can see
    Author has an option to 'accept' the reply
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='replies')
    content = models.TextField(max_length=255)
    publication_date = models.DateTimeField(auto_now_add=True)
    is_accepted = models.BooleanField(default = False)

    def __str__(self):
        return f"{self.post.title[:15]} ({self.user.username}) - {self.content[:20]}..."

    def accept(self):
        self.is_accepted = True
        self.save()