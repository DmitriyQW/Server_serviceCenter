from django.contrib import admin

# Register your models here.

from .models import (CustomUser,State_applic,TypeDevice_applic,
                     Manufacturer_applic,Application,PriceList,
                     Feedbackcol_number,Feedback,Publications)

# Регистрируем каждую модель
admin.site.register(CustomUser)
admin.site.register(State_applic)
admin.site.register(TypeDevice_applic)
admin.site.register(Manufacturer_applic)
admin.site.register(Application)
admin.site.register(PriceList)
admin.site.register(Feedbackcol_number)
admin.site.register(Feedback)
admin.site.register(Publications)

