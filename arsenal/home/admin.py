from django.contrib import admin
from home.models import *


# Register your models here.
admin.site.register(knowledge_base, knowledge_base_admin)
admin.site.register(user_extension, user_extension_admin)
admin.site.register(repository, repository_admin)
admin.site.register(trendingidea, trendingidea_admin)
admin.site.register(inventory,inventory_admin)
