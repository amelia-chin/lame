from time import strftime, localtime

def a_remove(string: str) -> str:
    output = ""
    skip_next = False
    for char in string:
        if skip_next:
            skip_next = not skip_next
            continue
        if char == "'":
            skip_next = True
        output += char
    return output

def convert(arr: list) -> list:
    return [list(item) for item in arr]

def a_clean(string: str) -> str:
    output = ""
    for char in string:
        if char == "'":
            output += "'"
        output += char
    return output

# "cleans up" data structure returned from sql query
def tup_clean(arr: list) -> list:
    return [item[0] for item in arr]


def get_greeting(name: str) -> str:
    curr_time = strftime("%H:%M:%S", localtime())
    hour_time = int(curr_time[:2])
    message_time = 0

    if hour_time >= 12 and hour_time <= 18:
        message_time = 1

    if hour_time > 18:
        message_time = 2

    greetings = ["Good morning", "Good afternoon", "Good evening"]
    for greeting in greetings:
        greeting += ", " + name
    
    return greeting