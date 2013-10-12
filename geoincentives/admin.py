from django.contrib import admin
from geoincentives.models import User, EventType, Event, Reward

class UserAdmin(admin.ModelAdmin):
    list_display = (
        'email',
        'first_name',
        'last_name'
    )
    search_fields = (
        'email',
        'first_name',
        'last_name',
    )



    EVENT_STATUS = (
        (1, 'student'),
        (2, 'business')
    )

class EventAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'type'
    )

class EventTypeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'max_checkin'
    )

class RewardAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )

admin.site.register(User, UserAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(EventType, EventTypeAdmin)
admin.site.register(Reward, RewardAdmin)