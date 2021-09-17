from django.contrib import admin
from .models import RestroomVisitData, Restroom, PrivateRestroom, Building, Review

# Register your models here.
admin.site.register(RestroomVisitData)
admin.site.register(PrivateRestroom)
admin.site.register(Restroom)
admin.site.register(Building)
admin.site.register(Review)