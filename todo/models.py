from django.db import models
from django.contrib.auth.models import User
import datetime 
from datetime import date


 

PRIORITY_CHOICES = ( 

  ('Low', 'Low'), 

  ('Medium', 'Medium'), 

  ('High', 'High'), 

) 


STATUS_CHOICES = ( 

  ('ToDO', 'ToDO'), 

  ('Doing', 'Doing'),

  ('Done', 'Done'),

) 


class task(models.Model):
    user_name = models.ForeignKey(User)
    title = models.CharField(max_length=100) 
    description = models.CharField(max_length=250)
    created_date = models.DateField(auto_now=True, auto_now_add=True)
    due_date = models.DateField(blank=True, null=True, ) 
    modified_date = models.DateField(auto_now=True, auto_now_add=True)
    priority = models.CharField(max_length=20, choices=STATUS_CHOICES, default='High')
    status  = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ToDO') 
    def __str__(self): 
        return self.title 

    class Meta: 
        ordering = ['-priority','-status' ,'title'] 

    def is_past_due(self):
        if date.today() > self.due_date:
            return True
        return False    

# Create your models here.
