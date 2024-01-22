import django_filters
from django.forms import DateInput
from django_filters import FilterSet
from .models import Post


class SearchFilter(FilterSet):
    heading = django_filters.Filter(
        field_name='heading',
        lookup_expr='icontains'
    )
    author = django_filters.Filter(
        field_name='author',
        lookup_expr='exact'
    )
    pub_date = django_filters.DateFilter(
        field_name='pub_date',
        lookup_expr='gte',
        widget=DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Post
        fields = {
            'category': ['exact'],
        }
