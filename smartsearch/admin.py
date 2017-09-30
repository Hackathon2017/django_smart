from django.contrib import admin
from django import forms
from django.db.models import TextField
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.utils.translation import ugettext_lazy as _
from django.utils.text import capfirst

# Integrating the model to can import and export the data via admin dashboard.
# See this docs: https://goo.gl/QR3Qqp
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from suit.widgets import AutosizedTextarea
from smartsearch.models import *


class DomainResource(resources.ModelResource):

    class Meta:
        model = Domain

class DomainAdmin(ImportExportModelAdmin, admin.ModelAdmin):

    resource_class = DomainResource

    list_display = ( 'title', 'about', 'imagePath' )
    search_fields = [ 'title', 'about', 'imagePath' ]


class SpecialityResource(resources.ModelResource):

    class Meta:
        model = Speciality

        
class SpecialityAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = SpecialityResource

    list_display = ( 'title', 'domain', 'imagePath' )
    search_fields = [ 'title', 'domain', 'imagePath' ]


class RateResource(resources.ModelResource):

    class Meta:
        model = Rate


class RateAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = RateResource

    list_display = ( 'rate_name', 'rate_value',  'post' )
    search_fields = [ 'rate_name', 'rate_value',  'post' ]


class SpecialistResource(resources.ModelResource):

    class Meta:
        model = Specialist

		
class SpecialistAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = SpecialistResource

    list_display = ( 'name', 'speciality',  'geocode', 'about_website', 'phone' )
    search_fields = [ 'name', 'speciality',  'geocode', 'about_website', 'phone' ]

	
class AuthorResource(resources.ModelResource):

    class Meta:
        model = Author

		
class AuthorAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = AuthorResource
    list_display = ('user', 'website', 'about')
    search_fields = ['user__username', 'user__email', 'about']
    list_filter = ['user__is_active', 'user__is_staff', 'user__is_superuser']


class TagResource(resources.ModelResource):

    class Meta:
        model = Tag


class TagAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = TagResource
    list_display = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}


class TagAdminForm(forms.ModelForm):
    avis = forms.CharField(
        required=False,
        widget=AutosizedTextarea(
            attrs={'rows': 3, 'class': 'input-xlarge'}))

    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        widget=FilteredSelectMultiple(
            verbose_name=_('Tags'),
            is_stacked=False
        )
    )

    class Meta:
        model = Post
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(TagAdminForm, self).__init__(*args, **kwargs)

        if self.instance and self.instance.pk:
            self.fields['tags'].initial = self.instance.tags.all()

    def save(self, commit=True):
        post = super(TagAdminForm, self).save(commit=False)
        if commit:
            post.save()

        if post.pk:
            post.tags = self.cleaned_data['tags']
            self.save_m2m()
        return post


class PostResource(resources.ModelResource):

    class Meta:
        model = Post


class PostAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = PostResource
    form = TagAdminForm
    list_display = ('title', 'author', 'created', 'modified', 'publish', 'specialist', 'ponctualite', 'traitement' )
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', 'avis', 'description', 'author__user__username', 'ponctualite', 'traitement' ]
    list_filter = ['publish', 'author__user__username', 'created']
    list_per_page = 20


# class PageResource(resources.ModelResource):

#     class Meta:
#         model = Page


# class PageAdmin(ImportExportModelAdmin, admin.ModelAdmin):
#     resource_class = PageResource
#     list_display = ('title', 'author', 'created', 'modified', 'publish')
#     prepopulated_fields = {'slug': ('title',)}
#     search_fields = ['title', 'description', 'author__user__username']
#     list_filter = ['publish', 'author__user__username', 'created']
#     list_per_page = 20


class GalleryResource(resources.ModelResource):

    class Meta:
        model = Gallery


class GalleryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = GalleryResource
    list_display = ('check_if_image', 'title', 'created', 'modified')
    search_fields = ['title']
    list_filter = ['created']
    list_per_page = 20


class VisitorResource(resources.ModelResource):

    class Meta:
        model = Visitor


class VisitorAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = VisitorResource
    list_display = ('post', 'ip', 'created', 'modified')


admin.site.register(Speciality, SpecialityAdmin)
admin.site.register(Specialist, SpecialistAdmin)
admin.site.register(Rate, RateAdmin)
admin.site.register(Domain, DomainAdmin)
admin.site.register(Author, AuthorAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Gallery, GalleryAdmin)
admin.site.register(Visitor, VisitorAdmin)
