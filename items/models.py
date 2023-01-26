from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=50) 
    description = models.TextField(max_length=1000)
    image = models.CharField(max_length=300)  # could be url
    categories = models.ManyToManyField('categories.Category', related_name="items")
    owner = models.ForeignKey(
        'jwt_auth.User', related_name='items', on_delete=models.CASCADE)

    available =  models.BooleanField(default=True)
 
    def __str__(self):
        return f'{self.name} - {self.owner}'
