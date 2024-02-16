from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.forms import TextInput, PasswordInput
# Register your models here.
admin.site.register(University)
admin.site.register(College)
admin.site.register(Course)
admin.site.register(Student)
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