'''
Created on Mar 13, 2015

@author: Alice
'''
import string
def base36encode(number):
    '''
    Base 36 encoder, for ids
    :param number: number to encode
    :type number: long or int
    :return string
    '''
    """Converts an integer to a base36 string."""
    alphabet= string.digits + string.lowercase
    if not isinstance(number, (int, long)):
        raise TypeError('number must be an integer')

    base36 = ''
    sign = ''

    if number < 0:
        sign = '-'
        number = -number

    if 0 <= number < len(alphabet):
        return sign + alphabet[number]

    while number != 0:
        number, i = divmod(number, len(alphabet))
        base36 = alphabet[i] + base36

    return sign + base36

def base36decode(number):
    '''
    just a simple wrapper
    :param number: number to decode
    :type number: string
    :return long
    '''

    return long(number, 36)



