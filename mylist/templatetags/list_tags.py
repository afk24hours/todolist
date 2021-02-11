from django import template
from django.db.models import Count, F
from mylist.models import Category, Point

register = template.Library()

@register.simple_tag(name='get_list_categories')
def get_categories():
    return Category.objects.all()

@register.inclusion_tag('mylist/todolistview.html')
def show_details():
    details = Point.objects.select_related('')
    return {"details":details,}