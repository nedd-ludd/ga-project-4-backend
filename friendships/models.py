from django.db import models

class Friendship(models.Model):
    user_one = models.IntegerField()
    user_two = models.ForeignKey(
        'jwt_auth.User', related_name='friendships', on_delete=models.CASCADE)
    user_two_items = models.ManyToManyField('items.Item', related_name="friendships")

    def __str__(self):
        return f'User{self.user_one} - User{self.user_2} friendship' 