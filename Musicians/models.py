from django.db import models
from Accounts.models import Users
import uuid
from django.utils import timezone
# Create your models here.
class MusicSkillChoices(models.Model):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    name=models.CharField(max_length=255)
    def __str__(self):
        return self.name
    def get_related_musicians(self):
        return MusicianModel.objects.filter(skills__id=self.id)

class MusicianModel(models.Model):
    Skill_Choice=(
        ('pianist','Pianist'),
        ('Singer','Singer'),
        ('conductor','Conductor'),
        ('Organist','Organist'),
        ('Vocalist','Vocal Coach'),
        ('Soloist','Soloist')
    )
    id=models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    user=models.OneToOneField(to=Users,on_delete=models.CASCADE,unique=True)
    skills=models.ManyToManyField(to=MusicSkillChoices,related_name='musician')
    description=models.TextField()
    recommended=models.BooleanField(default=False)
    location=models.CharField(max_length=255)
    phone_number=models.CharField(max_length=255)
    verified=models.BooleanField(default=False)
    joined_at=models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.username

