import django_filters
from django import forms
from ..models import News
from django import template

class NewsFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(field_name='title', lookup_expr='icontains', label='Название')
    author__name = django_filters.CharFilter(field_name='author__name', lookup_expr='icontains', label='Автор')
    created_at__gt = django_filters.DateFilter(
        field_name='created_at',
        lookup_expr='gt',
        label='Позже даты',
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = News
        fields = ['title', 'author__name', 'created_at__gt']
        
        


register = template.Library()

@register.filter
def in_group(user, group_name):
    return user.groups.filter(name=group_name).exists()