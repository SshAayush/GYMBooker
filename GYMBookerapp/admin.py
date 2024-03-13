from django.contrib import admin
from .models import Customer,CustomerQuery, Class, Membership, Facility, Days

#used to add custom button in admin panel
from django_object_actions import DjangoObjectActions
from django.urls import reverse
from django.shortcuts import redirect



# Register your models here.
admin.site.register(Customer)


# class MyModelAdmin(DjangoObjectActions, admin.ModelAdmin):
#     def send_mail(self, request, queryset):
#         print("Send Mail button pushed")

#     send_mail.short_description = "Send Mail"
#     changelist_actions = ('send_mail', )

# admin.site.register(Customer, MyModelAdmin)

# class MyModelAdmin(DjangoObjectActions, admin.ModelAdmin):
#     def send_mail(self, request, queryset):
#         url = reverse('send_offerEmail')
#         return redirect(url)

#     send_mail.short_description = "Send Mail"
#     changelist_actions = ('send_mail', )

# admin.site.register(Customer, MyModelAdmin)


admin.site.register(CustomerQuery)

admin.site.register(Class)

admin.site.register(Membership)

admin.site.register(Facility)

# admin.site.register(Days)