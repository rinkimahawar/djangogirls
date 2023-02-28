from django.contrib import admin
from .models import Post, User,Category,Tags,Comment
import csv
from django.http import HttpResponse



def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

export_as_csv.short_description = "Export Selected"

class PostAdmin(admin.ModelAdmin):
    search_fields = ['title','text','user','tag']
    list_filter = ['tag','user','title',]
    list_display = ('title','published_date', 'created_date',)
    actions = [export_as_csv]
    filter_horizontal = ('tag',)
    autocomplete_fields =['user','category']



class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['name',]
class UserAdmin(admin.ModelAdmin): 
    search_fields = ['email','city','country','PhoneNumber','image',]
class TagsAdmin(admin.ModelAdmin):
    search_fields = ['name',] 
class CommentAdmin(admin.ModelAdmin):
    search_fields = ['name','content','email','post','date_posted',]     




admin.site.register(Post, PostAdmin)
admin.site.register(User,UserAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Tags,TagsAdmin)
admin.site.register(Comment,CommentAdmin)







