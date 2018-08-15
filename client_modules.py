my_id = ''


def take_id(params):
    global my_id
    my_id = params['my_id']


def show_word(params):
    print params['value']