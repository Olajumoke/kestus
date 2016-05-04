from __future__ import unicode_literals
from django.utils.timezone import utc
from django.db import models
from django.utils import timezone
from markdown import markdown
from django.template.defaultfilters import slugify
import datetime
# Create your models here.

STATUS_A = (
        ("New","New"),
        ("Draft", "Draft"),
        ("Published", "Published"),
        ("Archived", "Archived"),
    )


def present_datetime():
    return datetime.datetime.now().utcnow().replace(tzinfo=utc)

class JobOpeningManager(models.Manager):
    def published(self):
        return (self).get_queryset().filter(status = "Published")

class JobOpenings(models.Model):
    title 			= models.CharField(max_length=300)
    pretext 		= models.TextField(max_length=300)
    slug            = models.SlugField(max_length=200, editable=False)
    body 			= models.TextField()
    created_date	= models.DateTimeField(default=timezone.now)
    expires_on      = models.DateField()
    published_date 	= models.DateTimeField(blank=True, null=True)
    modified_date   = models.DateTimeField(blank=True, null=True)
    status          = models.CharField(choices=STATUS_A, max_length=100, default="new")
    views           = models.IntegerField(default=0, editable=False)
    
    objects         = JobOpeningManager()
    
    class Meta:
        verbose_name_plural = "Job Openings"
        ordering = ['-published_date']
        
    def __unicode__(self):
        return self.title
    
    def has_expired(self):
        return datetime.date.today() > self.expires_on
    
    
    def save(self, *args, **kwargs):
        self.body = markdown(self.body)
        self.slug = slugify(self.title)
        if self.id is None:
            self.published_date = present_datetime()
        super(JobOpenings, self).save(*args, **kwargs)
        
        
    def modified(self):
        return self.modified_on > self.created_on