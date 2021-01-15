def first_whitespace_position(string: str) -> int:
    """
    Finds the first whitespace and return it's position. If there is no
    whitespaces return string's length.

    :param string: string to look for whitespaces in
    :return: index of the first whitespace within a string
    """
    counter = -1
    for character in string:
        counter += 1
        if character.isspace():
            return counter
    return counter + 1
