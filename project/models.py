from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import datetime

#########################  UserProfile  ################################

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile_phone = models.CharField(max_length=15)  
    profile_picture = models.ImageField(upload_to='profile_pictures/%Y/%m/%d', null=True, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    facebook_profile = models.URLField(null=True, blank=True)
    country = models.CharField(max_length=100, null=True, blank=True)


#########################  Tag  ################################

class Tag(models.Model):
    name = models.CharField(max_length=50)


#######################   Category  ################################

class Category(models.Model):
    name = models.CharField(max_length=100)


##########################   Project #######################################################
class Project(models.Model):
    title = models.CharField(max_length=255)
    details = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    pictures = models.ImageField(upload_to='project_pictures/%Y/%m/%d')
    total_target = models.DecimalField(max_digits=10, decimal_places=2)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    is_cancelled = models.BooleanField(default=False)
    tags = models.ManyToManyField(Tag)
    country = models.CharField(max_length=100, null=True, blank=True) 

    def total_donations(self):
        return self.donation_set.aggregate(models.Sum('amount'))['amount__sum'] or 0

    def total_ratings(self):
        return self.rating_set.aggregate(models.Sum('rating'))['rating__sum'] or 0

    def remaining_time(self):
        now = timezone.now()
        time_left = self.end_time - now
        days = time_left.days
        hours, remainder = divmod(time_left.seconds, 3600)
        months = days // 30
        remaining_days = days % 30
        remaining_time_msg = f"{months} months, {remaining_days} days, {hours} hours"
        return remaining_time_msg

    @staticmethod
    def top_rated_projects():
        top_projects = Project.objects.annotate(total_rating=models.Sum('rating__rating')).order_by('-total_rating')
        return top_projects


    @property
    def progress_percentage(self):
        if self.total_target > 0:
            return (self.total_donations() / self.total_target) * 100
        else:
            return 0 

############################  Donation  ####################################################

class Donation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    donated_at = models.DateTimeField(auto_now_add=True)

#################################   Comment  ################################################

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    text = models.TextField()
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


#################################   Reply   #################################################

class Reply(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

###########################    ProjectCancellation    ################################

class ProjectCancellation(models.Model):
    project = models.OneToOneField(Project, on_delete=models.CASCADE)
    cancellation_reason = models.TextField()
    cancelled_at = models.DateTimeField(auto_now_add=True)

##########################   Rating   #########################################    

class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    rating = models.IntegerField()

##############################  Report   ####################################    

class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True)
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

