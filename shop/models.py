from django.db import models
from django.utils.translation import gettext as _

class Category(models.Model):
    name = models.CharField(_("name category"), max_length=150, db_index=True, unique=True)
    description = models.TextField(_("description"), blank=True, null=True)
    image = models.ImageField(_("image"), upload_to='cover/', blank=True, null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
    