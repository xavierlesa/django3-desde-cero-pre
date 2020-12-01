# Curso Django3 Desde Cero


### Puntos del curso:

1. [ ] Boostrap proyecto con Docker

2. [ ] Instalar Django3 + dependencias

3. [ ] Start project (manage.py startproject)

4. [ ] Configuración básica Django Settings

5. [ ] Creación de app (manage.py startapp)

6. [ ] Codeando models, views, urls, admin

7. [ ] Templating (desde un template ya armado)

8. [ ] git push



### 1. Boostrap proyecto con Docker

Asegurate de tener `Docker` instalado y corriendo en entorno. También que tengas la CLI 
instalada ya que vamos a usar comandos como `docker ps` y `docker-compose ...`.


```bash
# verificamos que no tengamos nada corriendo
> docker ps
```

Si es necesario, detener los demás containers corriedo (aunque no es estrictamente necesario, 
solo para no consumir más recursos en tu entorno).

Luego para poder crear el container es neceario primero crear la imagen, para esto
vamos a construir ejecutando:

```bash
> docker-compose build
```

Si todo sale bien la imagen debería estar construida con el nombre que `portfolio_app`.

```bash
# con esto verificamos que la imagen se haya creado con el tag latest
> docker image ls | grep portfolio
```


### 2. Instalar Django3 + dependencias

Creamos el archivo `requirements.txt` e incluimos las dependencias para el proyecto.

Para el proyecto solo vamos a usar lo básico:

- Django v3
- Pillow v7
- psycopg2-binary (el driver binario para conecaar a postgres)

Estas dependencias las agregamos al archivo `requirements.txt` y nos va a quedar así:

```
# requirements.txt
django<3.2,>=3.0.0
Pillow<7.1,>=7.0.0
psycopg2-binary>=2.8,<3
```

Esto es todo, y al momento de hacer el `build` las dependencias se van a instalar desde 
`pip install`.

Para verificar podemos ejecutar:

```bash
> docker run -ti portfolio_app pip freeze
# o
> docker-compose run portfolio_app pip freeze
```


### 3. Start project (manage.py startproject)

Ya tenemos todo listo para crear el proyecto de Django, para esto tenemos que inciar el container
con la imagen que creamos, y con el container corriendo ejecutar el comando `django-admin`.

```bash
> docker-compose run portfolio_app ls -al
``` 

Y para verificar que está corriendo `docker ps`.

El container ahora es accesible y está listo para correr nuestra app. Lo primero que hacemos es
verificar que el container está vacio y que tenemos lo necesario.

Creamos el projecto con `django-admin startproject` y notar que al final hay un `.` esto es para 
indicarle a Django que no cree un nuevo directorio sino que lo haga donde está.


```bash
> docker-compose run portfolio_app django-admin startproject portfolio_app .
```

Esto nos va a dejar el proyecto iniciado (pero sin correr) con una estructura así:

```
.
├── Dockerfile
├── README.md
├── code
│   ├── manage.py
│   └── portfolio_app
│       ├── __init__.py
│       ├── asgi.py
│       ├── settings.py
│       ├── urls.py
│       └── wsgi.py
├── docker-compose.yml
└── requirements.txt
```

Limpiamos los contenemdores que no vamos a usar y dejamos corriendo la app.

```bash
> docker container ls -a | grep portfolio_app
# eliminar por ID si fuere necesario
> docker container rm $(docker container ls --all --filter name=portfolio_app --filter status=exited -q)
# dejamos corriendo la app como daemon -d
> docker-compose up -d
```


### 4. Configuración básica Django Settings

Django ya tiene de fábrica una configuración mínima, pero ésta configuración ya nos
permite dejar corriendo nuestra app con muy pocos cambios. 


#### Configuración de `static` y `media`

Al igual que en versiones anteriores de Django los archivos staticos no son algo que
gestione "bien" django, pero para cuando estamos desarrollando nos sirve lo mínimo y 
la configuración es bien simple.

En `settings.py` solo tenemos que agregar:


```python
STATIC_URL = '/static/'
MEDIA_URL = '/media/'

STATIC_ROOT = BASE_DIR / 'static'
MEDIA_ROOT = BASE_DIR / 'media'
```


#### Configuración de base de datos

Vamos a usar la misma configuración que dejamos en el servicio `db` en `docker-compose.yml`
y la agregamos al settings.

```diff
DATABASES = {
    'default': {
-        'ENGINE': 'django.db.backends.sqlite3',
-        'NAME': BASE_DIR / 'db.sqlite3',
+        'ENGINE': 'django.db.backends.postgresql',
+        'NAME': 'postgres',
+        'USER': 'postgres',
+        'PASSWORD': 'postgres',
+        'HOST': 'db',
+        'PORT': 5432,
    }
}
```


#### First-migration

Con la configuración mínima lista, ya podemos correr nuestra primer migración.

```bash
> docker-compose exec portfolio_app python manage.py migrate
```

Finalmente vamos a crear un `superuser` para acceder al admin.

```bash
> docker-compose exec portfolio_app python manage.py createsuperuser
```


### 5. Creación de app (manage.py startapp)

Ya tenemos todo listo para crear nuestra app y codear un poco ✨.
Vamos a crear la app `portfolio` que es la que va a contner nuestros `models` y `views`
para esta mini aplicación.

Si ya tenes corriendo en background el container podemos simplemente ejecutar:

```bash
> docker-compose exec portfolio_app python manage.py startapp portfolio
```

O bien si aun no está corriendo (es decir no ejecutaste `docker-compose up -d`) podes
correr el comando `docker-compose run`. La diferencia principal entre uno y otro es que
`run` __corre__  dentro de un `container` nuevo y luego lo baja cuando el comando termina 
y `exec` __ejecuta__ dentro del `container` que se esté ejecutando en backgound.


```bash
# Si aun no tenemos el container corriendo
> docker-compose run portfolio_app python manage.py startapp portfolio
```

**startup** nos va a crear una carpeta nueva `portfolio` dentro de `code` con todos los 
archivos necesarios de la app.


### 6. Codeando models, views, urls, admin

Ya tenemos todo listo para comenzar a codear ✨

Pero antes de codear vamos a definir un poco el modelo del portfolio.

#### El portfolio

Cada proyecto debería tener como mínimo:

- Imagen
- Título
- Descrición breve
- Descrición completa
- Estado (en progreso, terminado)
- Tags

Y las "vistas":

- Listado de proyectos
- Una interna con la información detallada del proyecto
- Listado agrupado por tags


#### Models


Vamos a crear solo dos `models` (sí es bien básica nuestra app) uno para `projects` y otro para `tags`.


```python
# portfolio/models.py
from django.db import models

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

    class Meta:
        verbose_name = 'Proyecto'
        verbose_name_plural = 'Proyectos'
        ordering = ('-end_date', 'status')

    def __str__(self):
        return self.title
        

class Tag(models.Model):
    name = models.CharField(
        verbose_name='Nombre',
        max_length=100,
        unique=True
    )

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        return self.name
```

Estos modelos son suficiente para este proyecto demo y minimalista, aunque claro que se 
puede extender hasta donde quieras.

Solo nos queda instalar nuestra app en `settings` y ejecutar una migración.

```diff
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
+    'portfolio.apps.PortfolioConfig',
]
```

```bash
# creamos la migration
> docker-compose exec portfolio_app python manage.py makemigrations
# ejecutamos la migration
> docker-compose exec portfolio_app python manage.py migrate
```


#### Admin

Nuestros modelos nos son accesibles aun en el Administrador porque no los registramos, así
que vamos a registrar la app y los models al admin.

```python
# portfolio/admin.py
from django.contrib import admin
from .models import Project, Tag

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'tag_list')

    def tag_list(self, obj):
        return ", ".join(obj.tags.all().values_list('name', flat=True))

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)

```


### 7. Templating (desde un template ya armado)

### 6. git push

