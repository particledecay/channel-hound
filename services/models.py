from django.core.exceptions import ValidationError
from django.db import models


class Service(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Package(models.Model):
    name = models.CharField(max_length=100, blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=6)

    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='packages')

    def __str__(self):
        return ' '.join(filter(lambda x: x, [self.service.name, self.name]))

    def validate_unique(self, exclude=None):
        """Performs a "unique together" check across the 'service' ForeignKey."""
        super().validate_unique(exclude=exclude)
        qs = Package.objects.filter(name=self.name)
        if qs.filter(service__name=self.service.name).exists():
            raise ValidationError({'name': ['Package must be unique per service']})



class Channel(models.Model):
    name = models.CharField(max_length=100, unique=True)

    packages = models.ManyToManyField(Package, related_name='channels')

    def __str__(self):
        return self.name