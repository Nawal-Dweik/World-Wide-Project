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

class MessageManager(models.Manager):
    def msg_basic_validator(self, postData):
        errors = {}
        if len(postData['content']) < 1:
            errors["content"] = "Content should be at least 1 characters"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BlogManager()


    ################################################################################################

class Group(models.Model):
    planner = models.ForeignKey(User, related_name="groupsPlannedByUser", on_delete = models.CASCADE)
    destination = models.TextField()
    description = models.TextField()
    users = models.ManyToManyField(User, related_name="groups")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Message(models.Model):
    context = models.TextField()
    sender = models.ForeignKey(User, related_name= 'messages_sent', on_delete = models.CASCADE )
    group = models.ForeignKey(Group, related_name= 'messages_group', on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = MessageManager()

def addMessage(msg_info,user_id,group_id):
    context = msg_info['content']
    sender = User.objects.get(id=user_id)
    group = Group.objects.get(id=group_id)
    Message.objects.create(context=context,sender=sender, group=group)
    Message.objects.last()
    return Message1

def addGroup(postedRequest, currentUserId):
    destination = postedRequest['destination']
    description = postedRequest['description']
    this_user = User.objects.get(id= currentUserId)
    this_group = Group.objects.create(destination=destination,description=description, planner=this_user)
    this_user.groups.add(this_group)

def all_groups_for_user(id):
    this_user = User.objects.get(id=id)
    groups = this_user.groups.all()
    return groups

def other_groups(id):
    this_user = User.objects.get(id=id)
    otherGroups = Group.objects.exclude(users=this_user)
    return otherGroups

def join(user_id, group_id):
    this_user = User.objects.get(id=user_id)
    this_group = Group.objects.get(id=group_id)
    this_user.groups.add(this_group)

def selected_group(group_id):
    group=Group.objects.get(id=group_id)
    return group

def users_joining_the_group(user_id,group_id):
    this_group = Group.objects.get(id=group_id)
    allGroupJoiners = User.objects.filter(groups=this_group)
    return allGroupJoiners

def msg_errors(check_info):
    errors = Message.objects.msg_basic_validator(check_info)
    return errors