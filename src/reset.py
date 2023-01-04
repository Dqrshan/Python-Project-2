def reset(id, name, price):
    for i in ['id', 'name', 'price']:
        exec(f'{i}.set("")')
    return
