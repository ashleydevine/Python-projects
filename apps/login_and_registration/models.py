from __future__ import unicode_literals
from datetime import datetime
from django.db import models
import re, bcrypt

regex_pattern_email = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
regex_pattern_password = re.compile(r'[A-Za-z0-9@#$%^&+=]{8,}')

class UserManager(models.Manager):

    def login_validation(self, data):

        errors = []
        username = data['username']
        password = data['password'].encode()

        try:
            user = User.objects.get(username=username)
            hashed_pw = user.password.encode()

            if hashed_pw == bcrypt.hashpw(password, hashed_pw):
                return (True, user)
        except:
                errors.append("Incorrect username or password")
        return (False, errors)

    def registration_validation(self, data):

        errors = []
        first_name = data['first_name']
        last_name = data['last_name']
        username = data['username']
        email = data['email']
        password = data['password']
        confirm_password = data['confirm_password']
        birthdate = data['birthdate']

        if len(first_name) < 2:
            errors.append('first name must be at least two characters')

        if len(last_name) <2:
            errors.append('last name must be at least two characters')

        if len(username) <2:
            errors.append('username must be at least two characters')

        if len(email) < 1:
            errors.append('email must be filled out')
        elif not regex_pattern_email.match(email):
            errors.append('email must be valid')

        if len(password) < 8:
            errors.append('password must be at least 8 characters')
        elif not regex_pattern_password.match(password):
            errors.append('password must contain valid characters')

        if len(confirm_password) <= 1:
            errors.append('confirm password must not be blank')
        if confirm_password != password:
            errors.append('confirm password does not match')

        if len(birthdate) > 0:
            try:
                birth_date_format = datetime.strptime(data['birthdate'], '%Y-%m-%d')
            except:
                errors.append("birthdate is invalid")
        if len(birthdate) < 1:
            errors.append('birthdate must not be empty')

        if not errors:
            try:
                match_email = self.get(email=email)
                errors.append('email already exists')
                match_username = self.get(username=username)
                erros.append('username already exists')
                return (False, errors)
            except:
                password = password.encode()
                pw_hash = bcrypt.hashpw(password, bcrypt.gensalt())
                user = self.create(first_name=first_name, last_name=last_name, username=username, email=email, password=pw_hash, birthdate=birth_date_format)
                return (True, user)
        else:
            return (False, errors)

    def delete_user(self, id):
        user = User.objects.filter(id=id)
        user.delete()
        print '*************'
        print user
        return (True)

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    birthdate = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __unicode__(self):
        return self.username
