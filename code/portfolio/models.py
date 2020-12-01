from django.db import models
from django.utils.text import slugify

class Project(models.Model):
    STATUS_COMPLETED = 'completed'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_DEPRECATED = 'deprecated'
    STATUS_CHOICES = (
            (STATUS_COMPLETED, 'Completado'),
            (STATUS_IN_PROGRESS, 'En Progreso'),
            (STATUS_DEPRECATED, 'Abandonado'),
        )

    title = models.CharField(
            verbose_name='Proyecto',
            max_length=100
        )

    short_description = models.CharField(
            verbose_name='Descripción corta',
            max_length=500
        )

    full_description = models.TextField(
            verbose_name='Descripción'
        )

    image = models.ImageField(
            verbose_name='Imagen',
            upload_to='projects/'
        )

    status = models.CharField(
            verbose_name='Estado',
            max_length=20,
            choices=STATUS_CHOICES,
            default=STATUS_IN_PROGRESS
        )


    start_date = models.DateField(
            verbose_name='Fecha de incio'
        )

    end_date = models.DateField(
            verbose_name='Fecha de entrega',
            blank=True,
            null=True
        )

    tags = models.ManyToManyField('Tag')

    slug = models.SlugField(blank=True)

    class Meta:
        verbose_name = 'Proyecto'
        verbose_name_plural = 'Proyectos'
        ordering = ('-end_date', 'status')

    def __str__(self):
        return self.title

    def save(self, **kwargs):
        self.slug = slugify(self.title)
        return super().save(**kwargs)


class Tag(models.Model):
    name = models.CharField(
        verbose_name='Nombre',
        max_length=100,
        unique=True
    )

    slug = models.SlugField(blank=True)

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        return self.name

    def save(self, **kwargs):
        self.slug = slugify(self.name)
        return super().save(**kwargs)
