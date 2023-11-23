from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
    

class Category(BaseModel):
    title = models.CharField(max_length=250)
    slug = models.SlugField()

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Category, self).save(*args, **kwargs)


class Author(BaseModel):
    full_name = models.CharField(max_length=150)
    bio = models.TextField(null=True)
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, related_name="users")

    def __str__(self):
        return self.full_name


    # def save(self, *args, **kwargs):
        # if not self.slug:
        #     self.slug = slugify(self.)
        # super(Author, self).save(*args, **kwargs)


class Post(BaseModel):
    title = models.CharField(max_length=250)
    content = models.TextField()
    slug = models.SlugField()
    image = models.ImageField(upload_to="posts/")
    publish_date = models.TimeField()
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE, related_name="posts")
    author = models.ForeignKey(to=Author, on_delete=models.CASCADE, related_name="authors", null=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)


# class User(models.Model):
#     user = models.OneToOneField(to=User, on_delete=models.CASCADE)
#     # address = models.CharField(max_length=250, null=True)
#     bio = models.TextField(null=True, blank=True)
#     age = models.PositiveSmallIntegerField(null=True)
#     image = models.ImageField(null=True, blank=True, upload_to="user/profiles/")

