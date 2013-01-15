from django import forms
from django.contrib import admin

from preferences import preferences
from jmbo.admin import ModelBaseAdmin, ModelBaseAdminForm

from show.models import Appearance, Credit, CreditOption, RadioShow, \
    Contributor, ShowPreferences


class CreditOptionInline(admin.TabularInline):
    model = CreditOption


class ShowPreferencesAdmin(admin.ModelAdmin):
    inlines = [CreditOptionInline]


class CreditInlineAdminForm(forms.ModelForm):

    class Meta:
        model = Credit
    

class CreditInline(admin.TabularInline):
    form = CreditInlineAdminForm
    model = Credit


class ShowAdminForm(ModelBaseAdminForm):

    def clean(self, *args, **kwargs):
        data = super(ShowAdminForm, self).clean(*args, **kwargs)
        # check that the start is earlier than the end
        if 'start' in data and 'end' in data and \
            data['start'] and data['end'] and data['start'] >= data['end']:
            raise forms.ValidationError('''The show's start date needs
                    to be earlier than its end date''')
        # check that repeat_until is after the end of the first show rep
        if 'repeat_until' in data and 'end' in data and \
            data['repeat_until'] and data['end'] and \
                data['repeat_until'] < data['end'].date():
            raise forms.ValidationError('''An show cannot have a repeat
                    cutoff earlier than the actual show''')

        return data


class ShowAdmin(ModelBaseAdmin):
    form = ShowAdminForm
    list_display =  ModelBaseAdmin.list_display + ('start', 'end', 'next', 'repeat', 'repeat_until')
    list_filter = ('repeat',)
    inlines = [CreditInline]


class AppearanceInline(admin.TabularInline):
    model = Appearance


class ContributorAdmin(ModelBaseAdmin):
    inlines = [AppearanceInline]


admin.site.register(RadioShow, ShowAdmin)
admin.site.register(Contributor, ContributorAdmin)
admin.site.register(ShowPreferences, ShowPreferencesAdmin)
