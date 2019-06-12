from django.db import models


class Service(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Package(models.Model):
    name = models.CharField(max_length=100, blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=6)

    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['name', 'service']

    def __str__(self):
        return self.name or self.service.name


class Channel(models.Model):
    name = models.CharField(max_length=100, unique=True)

    packages = models.ManyToManyField(Package, related_name='channels')

    def __str__(self):
        return self.name