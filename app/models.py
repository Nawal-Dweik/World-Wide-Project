from django.db import models
import re

class BlogManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors["first_name"] = "first name should be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "last name should be at least 2 characters"
        if len(postData['password']) < 8:
            errors["password"] = "password should be at least 8 characters"
        if postData['password'] != postData["confirm_password"]:
            errors["confirm_password"] = "passwords should matching"
        if re.match(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$', postData['email']) == None:               
            errors['email'] = "Invalid email address!"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BlogManager()

class Message(models.Model):
    context = models.TextField()
    sender_id = models.ForeignKey(User, related_name= 'messages_sent', on_delete = models.CASCADE )
    recipient_id = models.ForeignKey(User, related_name= 'messages_received', on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


   