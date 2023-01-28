from django_filters import FilterSet, CharFilter, ModelChoiceFilter, DateTimeFilter
from django.forms import DateTimeInput
from .models import Post, Category


class NewsFilter(FilterSet):
    title = CharFilter(
        field_name='title',
        lookup_expr='icontains',
        label='Заголовок содержит:'
    )

    postCategory = ModelChoiceFilter(
        field_name='postCategory',
        queryset=Category.objects.all(),
        label='Категория',
        empty_label='Все категории'
    )

    dateCreation = DateTimeFilter(
        field_name='dateCreation',
        lookup_expr='gt',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'},
        ),
        label='Дата позже:'
    )

    class Meta:
        model = Post
        fields = {
            'title', 'postCategory', 'dateCreation'
        }
