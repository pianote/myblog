from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone, text
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.

User = get_user_model()

class Post(models.Model):
    slug = models.SlugField(primary_key=True, unique=True, max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=100)
    content = RichTextUploadingField()
    created_date = models.DateTimeField(auto_now_add=True)
    date_posted = models.DateTimeField(default=timezone.now)
    is_published = models.BooleanField(default=False, verbose_name='Published')
    photo_main = models.ImageField(default='article.jpg', upload_to='photos/%Y/%m/%d/', blank=True)
    photo_1 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_2 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_3 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    
    def publish(self):
        self.is_published = True
        self.date_posted = timezone.now()
        self.save()
        pass

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = text.slugify(self.title)
        return super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete = models.CASCADE,related_name="comments")
    comment_author = models.ForeignKey(User, on_delete = models.SET_NULL, null=True)
    comment_content = models.TextField(max_length = 500)
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_date']

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.comment_content
    