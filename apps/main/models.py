from django.db import models
import bcrypt
import re
from datetime import *


class UserManager(models.Manager):
    def validate_user(self, postData):
        EMAIL_REGEX = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        error = {}

        if postData['form'] == 'reg':

            if not postData['fname'].isalpha():
                error['fname_alpha'] = "First Name must be letters"
            if not postData['lname'].isalpha():
                error['lname_alpha'] = "Last Name must be letters"
            if len(postData['fname']) < 3:
                error['fname'] = "First Name must be longer than 2 characters"
            if len(postData['lname']) < 3:
                error['lname'] = "Please provide a last name of at least 2 two characters"
            if not EMAIL_REGEX.match(postData['email']):
                error['email'] = "Invalid email format"
            if postData['password'] != postData['confirmpass']:
                error['passcomp'] = "Passwords do not match"
            if len(postData['password']) < 8:
                error['passlen'] = "Password must be at least 8 characters"

            try:
                User.objects.get(email=postData['checkemail'])
                error['emailexist'] = "Email already exists"
            except:
                pass

            return error

        if postData['form'] == 'login':
            try:
                hash = User.objects.get(email=postData['checkemail'])
                
            except:
                error['baddata'] = "Invalid Password or email"
                return error

            if not bcrypt.checkpw(postData['checkpass'].encode(), hash.password.encode()):
                error['baddata'] = "Invalid Password or email"
                return error
            else:
                return error

class TripManager(models.Manager):
    def validate_trip(self, postData):
        
        start = postData['start']
        now = date.today().strftime('%Y-%m-%d')

        error = {}

        if len(postData['dest']) < 3:
            error['dest'] = "A destination of at least 3 characters is required"
        if len(postData['plan']) < 3:
            error['plan'] = "Plan must be at least 3 characters"
        if start < now:
            error['starttime'] = "Trip cannot start in the past"
        if postData['start'] > postData['end']:
            error['timemismatch'] = "Start date must be before the end date"
        if postData['start'] == postData['end']:
            error['badend'] = "Return date cannot be the same as the start date"
        
        return error

class User(models.Model):
    first_name = models.CharField(max_length=455)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=60)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Trip(models.Model):
    dest = models.CharField(max_length=255)
    plan = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, related_name='created_by')
    join = models.ManyToManyField(User, related_name="join")
    objects = TripManager()


