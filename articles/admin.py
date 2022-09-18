from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet

from .models import Article, Scope, Tag

admin.site.register(Tag)
class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        q = []
        for form in self.forms:
            q.append((form.cleaned_data.get("is_main")))

        if q:
            if q.count(True) == 0:
                raise ValidationError('Укажите основной раздел')
        if q:
            if q.count(True) > 1:
                raise ValidationError('Основным может быть только один раздел')
        return super().clean()


class ScopeInline(admin.TabularInline):
    model = Scope
    formset = ScopeInlineFormset


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ScopeInline]
