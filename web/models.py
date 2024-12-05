from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='categories')
    
    
    
    class meta:
           db_table = "category"
           verbose_name = "category"
           verbose_name_plural = "categories"
           ordering = ['-id']
    
    
    def __str__(self):
          return self.name
