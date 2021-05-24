from django.db import models
from django.utils import timezone
import re


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def registration_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name'] = "Your first name must be at least 2 characters"
        if len(postData['first_name']) == 0:
            errors['first_name'] = "You must provide a first name"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Your last name must be at least 2 characters"
        if len(postData['last_name']) == 0:
            errors['last_name'] = "You must provide a last name"    
        if not EMAIL_REGEX.match(postData['email']):   
            errors['email'] = "Invalid email address!"
        users_with_email = User.objects.filter(email = postData['email'])
        if len(users_with_email) >= 1:
            errors['duplicate'] = "Email already exists."
        if len(postData['password']) < 5:
            errors['password'] = "Your password must be at least 5 characters"
        if postData['password'] != postData['confirm_password']:
            errors['pw_match'] = "Password must match!"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    profile_image = models.ImageField(null=True, blank=True, upload_to="images/")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    profile_pic = models.ImageField(null=True, blank=True)
    objects = UserManager()

class Post(models.Model):
    user_post = models.ForeignKey(User, related_name="user_post", on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    post_image = models.ImageField(null=True, blank=True, upload_to="images/")
    liked = models.ManyToManyField(User,blank=True, related_name='liked')
    created_at = models.DateTimeField(default=timezone.now)

class Comment(models.Model):
    post_comment = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    user_comment = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    #approved_comment = models.BooleanField(default=True)
