from django import template


register = template.Library()


@register.filter(name='censor')
def Censor(value):
    STRONG_WORDS = ["лучше", "плюсы"]
    if not isinstance(value, str):
        raise ValueError('Нельзя зацензурить строку')
    for word in STRONG_WORDS:
        value = value.replace(word[1:], '*' * (len(word)-1))
    return value
