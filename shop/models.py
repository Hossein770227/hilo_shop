from django.db import models
from django.urls import reverse
from django.utils.translation import gettext as _
from django.core.exceptions import ValidationError

from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(_("name category"), max_length=150, db_index=True, unique=True)
    description = models.TextField(_("description"), blank=True, null=True)
    image = models.ImageField(_("image"), upload_to='cover/', blank=True, null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
    

class Food(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name=_("category"), related_name='foods')
    title = models.CharField(_("title"), max_length=255, db_index=True,)
    slug = models.SlugField(_("slug"))
    description = models.TextField(_("description"))
    short_description = models.CharField(_("short description"), max_length=350)
    price_main = models.PositiveIntegerField(_("price main"))
    price_discount = models.PositiveIntegerField(_("price discount"), blank=True, null=True)
    image = models.ImageField(_("image"), upload_to='foods/')
    inventory = models.IntegerField(_("inventory"), default=1)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    class Meta:
        verbose_name = _("food")
        verbose_name_plural = _("foods")
        ordering = ['-created_at']

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def clean(self):
        if self.price_discount and self.price_discount >= self.price_main:
            raise ValidationError(_("Discount price must be less than price main."))
        
    def get_absolute_url(self):
        return reverse('shop:food_detail', args=[self.slug])
    