from django import template

register = template.Library()

bad_words = [
    'лучшие', 'Стоянка', 'металл', 'lara'
]


@register.filter()
def censor(message: str):
    global string2
    ln = len(bad_words)
    censor = ''
    string = ''
    pattern = '*'
    for i in message:
        string += i
        string2 = string.lower()

        flag = 0
        for j in bad_words:
            if not string2 in j:
                flag += 1
            if string2 == j:
                censor += pattern * len(string)
                flag -= 1
                string = ''

        if flag == ln:
            censor += string
            string = ''

    if string2 != '' and string2 not in bad_words:
        censor += string
    elif string2 != '':
        censor += pattern * len(string)

    return censor
