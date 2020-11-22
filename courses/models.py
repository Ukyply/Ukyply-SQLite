from django.db import models
# from memberships.models import Membership
from django.contrib.auth.models import User
from django.urls import reverse


class Category(models.Model):
    Title = models.CharField(max_length=150)
    Description = models.TextField(max_length= 200, null=True)
    Image = models.ImageField(upload_to='Category_Images', default='Category_Images/default.jpg')

    def __str__(self):
        return '{}'.format(self.Title)

class Course(models.Model):
    Creator = models.ForeignKey(User,on_delete = models.CASCADE)
    slug = models.SlugField()
    Title = models.CharField(max_length=90)
    Category = models.ForeignKey(Category,on_delete=models.CASCADE)
    Description = models.TextField(max_length=400)
    Time_Created = models.DateTimeField(auto_now=True)
    Image = models.ImageField(upload_to='Course_Images', default='Course_Images/default.jpg')
    Level = models.IntegerField()

    def __str__(self):
        return self.Title

    def get_absolute_url(self):
        return reverse("courses:course_detail", kwargs={"slug": self.slug})

    # def get_courses_related_to_memberships(self):
    #     return self.courses.all()

    @property
    def lessons(self):
        return self.lesson_set.all().order_by('Position')




class Lesson(models.Model):
    slug = models.SlugField()
    Title = models.CharField(max_length=64,default='')
    Course = models.ForeignKey(Course,on_delete=models.CASCADE)
    Video_id = models.FileField(upload_to='video_lessons',default='')
    Position = models.IntegerField()

    def __str__(self):
        return self.Title

    def get_absolute_url(self):
        return reverse("courses:lesson_detail", kwargs={"course_slug": self.Course.slug,'lesson_slug':self.slug})
