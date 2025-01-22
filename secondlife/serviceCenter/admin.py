from django.contrib import admin

# Register your models here.

from .models import (Worker,User,State_applic,TypeDevice_applic,
                     Manufacturer_applic,Application,PriceList,
                     Report,Feedbackcol_number,Feedback,Publications,Chat)

# Регистрируем каждую модель
admin.site.register(Worker)
admin.site.register(User)
admin.site.register(State_applic)
admin.site.register(TypeDevice_applic)
admin.site.register(Manufacturer_applic)
admin.site.register(Application)
admin.site.register(PriceList)
admin.site.register(Report)
admin.site.register(Feedbackcol_number)
admin.site.register(Feedback)
admin.site.register(Publications)
admin.site.register(Chat)
