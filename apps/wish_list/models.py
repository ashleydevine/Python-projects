from __future__ import unicode_literals
from datetime import datetime
from django.db import models
from ..login_and_registration.models import User

class WishManager(models.Manager):

    def delete_item(self, user_id, wish_id):
        try:
            item = self.get(id=wish_id)
            if item.created_by.id == user_id:
                item.delete()
                return True
            else:
                return False
        except:
            pass
            return False

    def remove_item(self, user_id, wish_id):
        try:
            user = User.objects.get(id=user_id)
            item = self.get(id=wish_id)
            item.added_by.remove(user)
            return True
        except:
            pass
            return False

    def wish_detail(self, wish_id):
        try:
            wish = self.get(id=wish_id)
            return (True, wish)
        except:
            return (False, 'wish does not exist')

    def my_items(self, user_id):
        items = self.filter(added_by__id=user_id)
        return items

    def others_items(self, user_id):
        items = Wish.objects.exclude(added_by__id=user_id)
        return items

    def adding_item(self, user_id, wish_id):
        errors = []
        try:
            user = User.objects.get(id=user_id)
            item = self.get(id=wish_id)
            item.added_by.add(user)
            return (True, item)
        except:
            errors.append('user or item does not exit')
            return (False, errors)

    def create_item(self, data, user_id):
        errors = []
        item = data['item']
        user = User.objects.filter(id=user_id)

        if len(item) < 3:
            errors.append('item must be more than 3 characters long')

        if not errors:
            try:
                match_item = self.get(item=item)
                errors.append('item already exists')
                return (False, errors)
            except:
                item = self.create(item=item, created_by=user[0])
                item.added_by.add(user[0])
                return (True, item)
        else:
            return (False, errors)

class Wish(models.Model):
    item = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    added_by = models.ManyToManyField(User, related_name='added_items')
    created_by = models.ForeignKey(User, related_name='created_items')
    objects = WishManager()

    def __unicode__(self):
        return self.item
