from django.db import models
from django.utils import timezone

# Create your models here.
class User(models.Model):
    nickname = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.nickname

class Presentation(models.Model):
    title = models.CharField(max_length=100)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="presentations")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'presentations'

    def __str__(self):
        return self.title


from django.db import models

class PresentationUser(models.Model):
    ROLE_CHOICES = [
        ('CREATOR', 'Creator'),
        ('EDITOR', 'Editor'),
        ('VIEWER', 'Viewer'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="presentation_roles")
    presentation = models.ForeignKey(Presentation, on_delete=models.CASCADE, related_name="participants")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'presentation_users'

    def __str__(self):
        return f'{self.user.nickname} - {self.presentation.title} ({self.get_role_display()})'

class Slide(models.Model):
    presentation = models.ForeignKey(Presentation, on_delete=models.CASCADE, related_name='slides')
    order = models.IntegerField() 
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'slides'

    def __str__(self):
        return f"Slide {self.order} - {self.presentation.title}"

class SlideElement(models.Model):
    slide = models.ForeignKey(Slide, on_delete=models.CASCADE, related_name='elements')
    type = models.CharField(max_length=20, choices=[('TEXT', 'Text'), ('IMAGE', 'Image'), ('SHAPE', 'Shape')]) 
    content = models.TextField()  
    position = models.CharField(max_length=100)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'slideelements'

    def __str__(self):
        return f"{self.type} Element for Slide {self.slide.order}"

