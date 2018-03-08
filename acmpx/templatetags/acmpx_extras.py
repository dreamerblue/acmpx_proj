# coding:utf-8

from django import template

register = template.Library()


@register.filter
def date_en(value):
	return value.strftime('%b. %d, %Y')
