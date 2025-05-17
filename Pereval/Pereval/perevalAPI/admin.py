from django.contrib import admin

from .models import (User, SpecificationOfPereval, Coordinates, Level, Images)

admin.site.register([User, SpecificationOfPereval, Coordinates, Level, Images])
