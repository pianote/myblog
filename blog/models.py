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

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = text.slugify(self.title)
            if Post.objects.filter(slug=slug):
                queryset = Post.objects.all()
                slug_list = [post.slug for post in [*queryset]]
                for item in slug_list:
                    if slug in slug_list:
                        last_word = slug.split('-')[-1] #str or int
                        try:
                            slug = '-'.join([slug.rsplit('-',1)[0],str(int(last_word)+1)])
                        except:
                            slug = '-'.join([slug,'1'])
            self.slug = slug
        return super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete = models.CASCADE,related_name="comments")
    author = models.ForeignKey(User, on_delete = models.SET_NULL, null=True)
    comment_content = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    is_approved = models.BooleanField(default=False, verbose_name='Approved')

    class Meta:
        ordering = ['-created_date']

    def approve(self):
        self.approved_comment = True
        self.save()

    def __str__(self):
        return self.comment_content

class Reply(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    reply_content = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    is_approved = models.BooleanField(default=True, verbose_name='Approved')

    class Meta:
        ordering = ['-created_date']
        verbose_name_plural = 'Replies'

    def __str__(self):
        return self.reply_content


class Like(models.Model):
    post = models.ForeignKey(Post,on_delete = models.CASCADE,related_name="choices")
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    choice = models.BooleanField(default=False, verbose_name='like')
    created_date = models.DateTimeField(default=timezone.now)

    class Meta:
        constraints =  [
            models.UniqueConstraint(fields=['post','author','choice'], name='preference'),
        ]
        verbose_name = 'Preference'
    
    def __str__(self):
        return "{} : {} : {}".format(self.post,self.author,'like' if self.choice==True else None)
