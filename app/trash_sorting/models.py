from django.db import models
# Create your models here.

class ContentType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Content(models.Model):
    name = models.CharField(max_length=50)
    type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    description = models.CharField(max_length=200, null=True)
    def __str__(self):
        return "{} ({})".format(self.name, str(self.type))


class SortSystem(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Address(models.Model):
    address = models.CharField(max_length=1000)# json
    parent_system = models.ForeignKey(SortSystem, on_delete=models.DO_NOTHING, null=True)

    def __str__(self):
        return self.address

class Bin(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    parent_system:SortSystem = models.ForeignKey(SortSystem, on_delete=models.CASCADE)
    contents = models.ManyToManyField(Content, blank=True)

    def __str__(self):
        return "{}, {}".format(str(self.name), str(self.parent_system))