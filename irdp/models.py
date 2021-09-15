from django.db import models

class Ahli(models.Model):
  #add variables here
    name = models.TextField()
    state = models.TextField(primary_key=True)
    # add fields for social media, hansard and sessions
    image = models.ImageField(null=True,blank=True, upload_to="profile_images/")
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    #define plural entity
    class Meta:
      verbose_name_plural = "Ahli-ahli"

    def __str__(self):
        return f'{self.name}-{self.state}'

    def get_image(self):
        try:
              # or whatever causes the exception
              return self.image
        except IOError:
              return None