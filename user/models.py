from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
import uuid
from djongo import models

# Django Model Custom Fields
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField

class Profile(models.Model):
    # Unique ID for each profile, other than user_id of user
    id = models.UUIDField(
        primary_key=True, 
        default=uuid.uuid4, 
        editable=False,
        db_index=True)

    class Gender(models.TextChoices):
        MALE   = 'M'
        FEMALE = 'F'
        OTHER  = 'O'

    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE)

    gender = models.CharField(
        _("Gender"),
        max_length=1,
        choices=Gender.choices)

    country = CountryField(blank=True)

    address= models.CharField(max_length=150,blank=True)
    state= models.CharField(max_length=25,blank=True)
    city = models.CharField(max_length=25,blank=True)

    zip_code = models.CharField(
                _("zip code"), 
                max_length=5,
                blank=True,
                null=True)
    
    phone_number = PhoneNumberField(
                    unique=True,
                    null=True)

    profile_image = models.ImageField(
                        default='/static/images/default_profile_image.jpg',
                        upload_to='profile_pic')

    class Meta:
        abstract = True

    def __str__(self):
        return self.user.username
    
class Student(Profile):

    class StudentGrades(models.TextChoices):
        JUNIOR = 'J'
        MIDDLE = 'M'
        HIGHSCHOOL = 'H'
        SENIOR = 'S'

    school_name = models.CharField(
        _("School Name"), 
        max_length=50,
        blank=True)

    grade = models.CharField(
        _("Grade"),
        choices=StudentGrades.choices, 
        max_length=1)

    dob = models.DateField(_("Date of Birth"))
    parent_name = models.CharField(_("Parent Name"), max_length=50)

class Teacher(Profile):
    qualification = models.CharField(_("Qualification"), max_length=50)
    charges = models.DecimalField(
        _("Charges Per Class"), 
        max_digits=3, 
        decimal_places=2)
        
class Manager(Profile):
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.user.is_staff= True
        self.user.save()
        return super().save(force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)

    class Meta:
        pass