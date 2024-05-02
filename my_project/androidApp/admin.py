from django.contrib import admin
from .models import Location
from .models import Data
from .models import Route


# Register your models here.
admin.site.register(Location)
admin.site.register(Data)
admin.site.register(Route)
