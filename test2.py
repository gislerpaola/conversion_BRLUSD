spam = ['apples', 'bananas', 'tofu', 'cats']

def items_list(list_):
    for index, item in enumerate(list_):
        if index == len(list_) - 2:  # Second-to-last item
            print(item, end=" and ")
        elif index == len(list_) - 1:  # Last item
            print(item + ".")
        else:
            print(item, end=", ")


items_list(spam)
