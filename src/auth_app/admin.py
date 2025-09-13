from django.contrib import admin

from auth_app.models import User


class UserAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if form.cleaned_data.get("password") and not change:
            obj.set_password(form.cleaned_data["password"])
        elif form.cleaned_data.get("password") and change:
            if "password" in form.changed_data:
                obj.set_password(form.cleaned_data["password"])
        super().save_model(request, obj, form, change)


admin.site.register(User, UserAdmin)
