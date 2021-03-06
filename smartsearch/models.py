from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from redactor.fields import RedactorField
from picklefield.fields import PickledObjectField
import json

class Domain(models.Model):
    title = models.CharField(max_length=200)
    about = models.TextField(null=True, blank=True)
    imagePath = models.CharField(max_length=200,null=True, blank=True)

    def __str__(self):
        return json.dumps({ "id":self.id , "title":self.title , "about": str(self.about), "imagePath": str(self.imagePath) })

    def get_absolute_url(self):
        return reverse('domain-detail', args=[str(self.id)])
       

class Speciality(models.Model):
    title = models.CharField(max_length=200) 
    domain = models.ForeignKey(Domain, related_name='speciality_domain')
    imagePath = models.CharField(max_length=200,null=True, blank=True)

    def __str__(self):
        return json.dumps({ "title":self.title , "domain": str(self.domain), "imagePath": str(self.imagePath) })

    def get_absolute_url(self):
        return reverse('speciality-detail', args=[str(self.id)])

class Specialist(models.Model):
    name = models.CharField(max_length=200) 
    speciality = models.ForeignKey(Speciality, related_name='speciality')
    geocode = models.CharField(max_length=200)
    about_website = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=200)
    global_rate = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
      return reverse('specialist-detail', args=[str(self.id)])



class TimeStampedModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True



class Author(models.Model):
    user = models.ForeignKey(User, related_name='author')
    avatar = models.ImageField(upload_to='gallery/avatar/%Y/%m/%d',
                               null=True,
                               blank=True,
                               help_text="Upload your photo for Avatar")
    about = models.TextField()
    website = models.URLField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.user.username

    def get_absolute_url(self):
        return reverse('author_posts_page',
                       kwargs={'username': self.user.username})

    class Meta:
        verbose_name = 'Detail Author'
        verbose_name_plural = 'Authors'


class Tag(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.title

    @property
    def get_total_posts(self):
        return Post.objects.filter(tags__pk=self.pk).count()

    class Meta:
        verbose_name = 'Detail Tag'
        verbose_name_plural = 'Tags'


class PostQuerySet(models.QuerySet):

    def published(self):
        return self.filter(publish=True)


class Post(TimeStampedModel):
    author = models.ForeignKey(Author, related_name='author_post')
    specialist = models.ForeignKey(Specialist, related_name='specialist_avis', null=True, blank=True)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    cover = models.ImageField(upload_to='gallery/covers/%Y/%m/%d',
                              null=True,
                              blank=True,
                              help_text='Optional cover post')
    avis = models.TextField(null=True, blank=True)
    description = RedactorField()
    tags = models.ManyToManyField('Tag')
    keywords = models.CharField(max_length=200, null=True, blank=True,
                                help_text='Keywords sparate by comma.')

    ponctualite = models.IntegerField(null=True, blank=True) 
    traitement = models.IntegerField(null=True, blank=True) 

    publish = models.BooleanField(default=True)
    objects = PostQuerySet.as_manager()

    def get_absolute_url(self):
        return reverse('detail_post_page', kwargs={'slug': self.slug})

    @property
    def total_visitors(self):
        return Visitor.objects.filter(post__pk=self.pk).count()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Detail Post'
        verbose_name_plural = 'Posts'
        ordering = ["-created"]


class Rate(models.Model):
    rate_name = models.CharField(max_length=200,null=True, blank=True)
    rate_value = models.IntegerField(null=True, blank=True)
    post = models.ForeignKey(Post, related_name='post', blank=True)

    def __str__(self):
        return json.dumps({ "rate_name":self.rate_name , "rate_value": str(self.rate_value), "post": str(self.post) })

    def get_absolute_url(self):
        return reverse('rate-detail', args=[str(self.id)])
        



class Page(TimeStampedModel):
    author = models.ForeignKey(Author, related_name='author_page')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = RedactorField()
    publish = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    # this will be an error in /admin
    # def get_absolute_url(self):
    #    return reverse("page_detail", kwargs={"slug": self.slug})

    class Meta:
        verbose_name = "Detail Page"
        verbose_name_plural = "Pages"
        ordering = ["-created"]


class Gallery(TimeStampedModel):
    title = models.CharField(max_length=200)
    attachment = models.FileField(upload_to='gallery/attachment/%Y/%m/%d')

    def __str__(self):
        return self.title

    def check_if_image(self):
        if self.attachment.name.split('.')[-1].lower() \
                in ['jpg', 'jpeg', 'gif', 'png']:
            return ('<img height="40" width="60" src="%s"/>' % self.attachment.url)
        return ('<img height="40" width="60" src="/static/assets/icons/file-icon.png"/>')
    check_if_image.short_description = 'Attachment'
    check_if_image.allow_tags = True

    class Meta:
        verbose_name = 'Detail Gallery'
        verbose_name_plural = 'Galleries'
        ordering = ['-created']


class Visitor(TimeStampedModel):
    post = models.ForeignKey(Post, related_name='post_visitor')
    ip = models.CharField(max_length=40)

    def __str__(self):
        return self.post.title

    class Meta:
        verbose_name = 'Detail Visitor'
        verbose_name_plural = 'Visitors'
        ordering = ['-created']

