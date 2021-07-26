def check_access(user_role):
    role_access = {
        'admin': 'Можно всё',
        'moderator': 'Можно модерировать',
        'author': 'Можно писать'
    }
    return role_access.get(user_role, 'Можно читать')


print(check_access(user_role='admin'))
