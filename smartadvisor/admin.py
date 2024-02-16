from django.contrib import admin
from .models import *
from django import forms

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.forms import TextInput, PasswordInput
# Register your models here.
admin.site.register(University)
class LevelRequirementInline(admin.StackedInline):
    model = LevelRequirement

class LevelAdmin(admin.ModelAdmin):
    inlines = [LevelRequirementInline]
admin.site.register(Level, LevelAdmin)

class CollegeAdminForm(forms.ModelForm):
    class Meta:
        model = College
        fields = '__all__'

class CollegeAdmin(admin.ModelAdmin):
    list_display = ('name', 'number_of_required_optional_course', 'university', 'number_of_levels')

    form = CollegeAdminForm

    def get_form(self, request, obj=None, **kwargs):
        # إذا كان هناك مستوى محدد، أضف حقول الإدخال بناءً على هذا المستوى
        if obj and obj.number_of_levels:
            for i in range(obj.number_of_levels):
                self.form.base_fields[f'custom_field_{i + 1}'] = forms.CharField(max_length=50, label=f'Custom Field {i + 1}')

        return super().get_form(request, obj, **kwargs)

admin.site.register(College, CollegeAdmin)
admin.site.register(Course)
admin.site.register(Student)
admin.site.register(University_Courses)
# تعديل موديل المستخدم لإضافة InlineModelAdmin

# ModelAdmin لنموذج المشرف
class AdvisorInline(admin.StackedInline):
    model = Advisor
    can_delete = False

class CustomUserAdmin(UserAdmin):
    inlines = (AdvisorInline,)

# إزالة تسجيل نموذج المستخدم الافتراضي
admin.site.unregister(User)
class AdvisorAdmin(admin.ModelAdmin):
    # ... أي إعدادات إضافية لنموذج المشرف إذا لزم الأمر

    def has_add_permission(self, request):
        # تعيين هذه الدالة إلى False لتعطيل زر الإضافة
        return False

# سجل نموذج المشرف مع واجهة المشرف المخصصة
admin.site.register(Advisor, AdvisorAdmin)
# سجل نموذج المستخدم مع واجهة مخصصة
admin.site.register(User, CustomUserAdmin)
admin.site.register(Major)