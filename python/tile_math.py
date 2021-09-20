from openlocationcode import openlocationcode as olc
from OpenGeoTile import TileSize
from decimal import Decimal
import math
import pprint
pp = pprint.pformat

CODE_ALPHABET = olc.CODE_ALPHABET_
CODE_ALPHABET_LEN = len(CODE_ALPHABET)

OLC_TO_VALUE = {char: index for index, char in enumerate(CODE_ALPHABET)}
VALUE_TO_OLC = dict(map(reversed, OLC_TO_VALUE.items()))

BASE_20_CHARS = '0123456789ABCDEFGHIJ'
OLC_TO_BASE_20 = dict(zip(CODE_ALPHABET, BASE_20_CHARS))
BASE_20_TO_OLC = dict(map(reversed, OLC_TO_BASE_20.items()))

BASE_20_TO_INT = {char: index for index, char in enumerate(BASE_20_CHARS)}
INT_TO_BASE_20 = dict(map(reversed, BASE_20_TO_INT.items()))

def str2int(string):
    integer = 0
    for character in string:
        assert character in OLC_TO_VALUE, 'Found unknown character!'
        value = OLC_TO_VALUE[character]
        assert value < CODE_ALPHABET_LEN, 'Found digit outside base!'
        integer *= CODE_ALPHABET_LEN
        integer += value
    return integer
def olc_2_b20(olc_string):
    integer = int('0', base=20)
    zfill_needed = len(olc_string)
    for char in olc_string:
        assert char in OLC_TO_BASE_20, 'Found unknown character!'
        base_20_digit = int(OLC_TO_BASE_20[char], base=20)
        print('base_20_digit:', base_20_digit)
        assert base_20_digit < int('10', base=20), 'Found digit outside base!'
        integer *= int('10', base=20)
        integer += base_20_digit
    return integer, zfill_needed

def b20_to_olc(base_20_int, zfill_needed):
    array = []
    if base_20_int == 0:
        return "2".zfill(zfill_needed).replace('0', '2')
    while base_20_int:
        base_20_int, base_10_value = divmod(base_20_int, int('10', base=20))
        base_20_value = INT_TO_BASE_20.get(base_10_value)
        print('base_20_int:', base_20_int, 'value:', base_20_value)
        array.append(BASE_20_TO_OLC[base_20_value])
    return ''.join(reversed(array)).zfill(zfill_needed).replace('0', '2')

print(pp(OLC_TO_BASE_20))
print(pp(BASE_20_TO_OLC))
print(pp(INT_TO_BASE_20))

for n in CODE_ALPHABET:
    n = n + n
    x, z = olc_2_b20(n)
    y = b20_to_olc(x, z)
    print('OLC=', n)
    print('b20=', x)
    print('zfill=', z)
    print('OLC=', y)
    print('')


test = '2X2X2X2X2X'
def return_x_axis_address(address):
    return address[::2]
def return_y_axis_address(address):
    return address[1::2]
def return_address_from_xy_address(x_address, y_address):
    assert len(x_address) == len(y_address), 'list need to be the same length'
    address_list = [None]*(len(x_address)+len(y_address))
    address_list[::2] = list1
    address_list[1::2] = list2
    return "".join(address_list)

print(test)
print(return_x_axis_address(test))
print(return_y_axis_address(test))


def int2str(integer):
    array = []
    while integer:
        integer, value = divmod(integer, CODE_ALPHABET_LEN)
        array.append(VALUE_TO_OLC[value])
    return ''.join(reversed(array))


print(list(CODE_ALPHABET[9:]))
def x_axis_overflow(end_x_axis_address, start_x_axis_address):
    if len(start_x_axis_address) != end_x_axis_address:
        return None # overflow
    elif end_x_axis_value[0] in list(CODE_ALPHABET[9:]):
        '''['F', 'G', 'H', 'J', 'M', 'P', 'Q', 'R', 'V', 'W', 'X']'''
        return None # overflow
    return end_x_axis_value

def y_axis_int_overflow(end_y_axis_address, start_y_axis_address):
    '''GLOBAL level, horizontal => 2 - V  =>  0 - 17'''

    '''
    overflow_mapping = {
        18: 0
    }'''
    len_end = len(end_y_axis_address)
    len_start = len(start_y_axis_address)
    if len_end == len_start:
        if end_y_axis_address[0] in list(CODE_ALPHABET[17:]):
            new_y_value = OLC_TO_VALUE[end_y_axis_address[0]] % 18
            new_y_char = VALUE_TO_OLC[new_y_value]
            new_y_
    if len_end > len(end_y_axis_value):
        len_diff = OLC_TO_VALUE()
    int_mod = 18
    return y_axis_int_value % int_mod

# Global Grid is 9 rows and 18 columns # https://en.wikipedia.org/wiki/Open_Location_Code
GLOBAL_MAX_X_DIGIT = VALUE_TO_OLC.get(9-1)  # Zero-based numbering
GLOBAL_MAX_X_VALUE = OLC_TO_VALUE.get(GLOBAL_MAX_X_DIGIT)
GLOBAL_MAX_Y_DIGIT = VALUE_TO_OLC.get(18-1) # Zero-based numbering
GLOBAL_MAX_Y_VALUE = OLC_TO_VALUE.get(GLOBAL_MAX_Y_DIGIT)
print('GLOBAL_MAX_X_DIGIT:', GLOBAL_MAX_X_DIGIT)
##print('GLOBAL_MAX_X_VALUE:', GLOBAL_MAX_X_VALUE)
##print('GLOBAL_MAX_Y_DIGIT:', GLOBAL_MAX_Y_DIGIT)
##print('GLOBAL_MAX_Y_VALUE:', GLOBAL_MAX_Y_VALUE)

GLOBAL_LEN       = 2
REGION_LEN       = 4
DISTRICT_LEN     = 6
NEIGHBORHOOD_LEN = 8
PINPOINT_LEN     = 10
len_list =[GLOBAL_LEN, REGION_LEN, DISTRICT_LEN, NEIGHBORHOOD_LEN, PINPOINT_LEN]

def address_to_value(address):
    address_len = len(address)

    global_digits = address[0: GLOBAL_LEN]
    global_x, global_y = global_digits[0], global_digits[1]
    int_x = Decimal(str(OLC_TO_VALUE.get(global_x)))
    int_y = Decimal(str(OLC_TO_VALUE.get(global_y)))
    #print('int_x:', int_x)
    #print('int_y:', int_y)
    dec_x = Decimal("0")
    dec_y = Decimal("0")
    if address_len > GLOBAL_LEN:
        ''' get the "float" versions of these addresses
            that is, address "CWWW" -> "C.WWW" -> decimal version of that
            decimal version is simply dividing by the max value
            e.g. ".WWW" -> OLC_TO_VALUE(WWW)/symbol_to_Value(max, which isXXX)'''
        float_x, float_y = "", ""
        for index, zone_len in enumerate(len_list):
            if index == 0:
                continue
            if address_len >= zone_len:
                zone_digits = address[len_list[index-1]: zone_len]
            if zone_digits:
                float_x += zone_digits[0]
                float_y += zone_digits[1]
        #print('float_x:', float_x)
        #print('float_y:', float_y)
        #print('Decimal(str(str2int(float_x))):', Decimal(str(str2int(float_x))))
        max_xy = "X" * len(float_x) # max possible value for that number of digits
        #print('max_xy:', max_xy, "int", str2int(max_xy))
        dec_x = (Decimal(str(str2int(float_x)))/Decimal(str(str2int(max_xy))))
        print('dec_x:', dec_x.as_integer_ratio())
        dec_y = Decimal(str(str2int(float_y)))/Decimal(str(str2int(max_xy)))
        print('dec_y:', dec_y.as_integer_ratio())

    x = int_x + dec_x
    y = int_y + dec_y

    return x, y

def value_to_address(x_y_tuple, tile_size):
    x_y_int_tuple = [None, None]
    x_y_code_floats = ['', '']
    for index, n in enumerate(x_y_tuple):
        int_n = Decimal(math.floor(n))
        x_y_int_tuple[index] = int_n
        #print(f'int_{["x","y"][index]}:', int_n, type(int_n))
        dec_n = n - int_n
        #print(f'dec_{["x","y"][index]}', dec_n, type(dec_n))
        float_len = int((tile_size.getCodeLength()/2)-1)
        if dec_n:
            max_xy = "X" * int(tile_size.getCodeLength()/2)
            base_20_max_n = "J" * float_len
            #print(f'max_{["x","y"][index]}:', base_20_max_n, "int:", int(base_20_max_n, 20))
            max_n_value = Decimal(str(int(base_20_max_n, 20)))
            #print(f'max_{["x","y"][index]}_value:', max_n_value, type(max_n_value))
            total_float_n = round(dec_n * max_n_value)
            float_n = int2str(total_float_n).zfill(float_len).replace("0","2")
            #print(f'float_{["x","y"][index]}', float_n, type(float_n))
            x_y_code_floats[index] = float_n
        else:
            x_y_code_floats[index] = "".zfill(float_len).replace("0","2")
    code_float = ""
    for i in range(int((tile_size.getCodeLength()/2)-1)):
        if x_y_code_floats[0]:
            code_float += x_y_code_floats[0][i]
        if x_y_code_floats[1]:
            code_float += x_y_code_floats[1][i]
    #print(code_float)

    #print('x_y_int_tuple:', x_y_int_tuple)
    x_int, y_int = x_y_int_tuple
    if x_int > 8 or x_int < 0:
        '''value is not valid address'''
        return None
    y_int = y_axis_int_overflow(y_int)
    code_int = f'{VALUE_TO_OLC.get(int(x_int))}{VALUE_TO_OLC.get(int(y_int))}'
    address = code_int + code_float
    ##print('code:', address)
    return address

tile_size_list = [
    TileSize.GLOBAL,
    TileSize.REGION,
    TileSize.DISTRICT,
    TileSize.NEIGHBORHOOD,
    TileSize.PINPOINT
]
tile_values  = {
    str(tile_size.getCodeLength()):
    address_to_value(f"{'22' * int(((tile_size.getCodeLength()-2)/2))}23")[1]
    for tile_size in tile_size_list
}
#print(tile_values)
def move(address, cardinal_direction, steps=1):
    if cardinal_direction in ["N", "E"]:
        sign = 1
    else:
        sign = -1
    x_address = return_x_axis_address(address)
    y_address = return_y_axis_address(address)
    b20_steps = int((steps * sign), base=20)

    if cardinal_direction in ["N", "S"]:
        x_address_value, zfill_needed = olc_2_b20(x_address)
        new_x_address_value = x_address_value + b20_steps
        return return_address_from_xy_address(new_x_address_value, y_address)



    address_value = list(address_to_value(address))
    #print('address_value:', address_value)
    value = address_value[xy_index]
    #print('value:', value, type(value))
    new_value = value + (sign * step_size * steps)
    #print('new_value:', new_value, type(new_value))
    address_value[xy_index] = new_value
    #print('address_value:', address_value)
    new_address = value_to_address(address_value, tile_size)
    #print('new_address:', new_address)
    return new_address

###print(address_to_value('CVXXXXXXXX'))
#MAX_X_Y_VALUES = address_to_value("CVXXXXXXXX")
'''
for d in ["N", "E"]:
    print(d)
    for tile_size in tile_size_list:
        code = f"{'22' * int(((tile_size.getCodeLength())/2))}"
        print('code:', code)
        for i in CODE_ALPHABET:
            print(i)
            if code:
                code = move(code, d, tile_size)
                print('code:', code)
'''













