import struct
import sys

def serialize_signed_int(value):
  if -127 <= value <= 127:
    return bytes([0xd0|value])
  elif -32768 <= value <= 32767:
    big_indian=struct.pack('>h', value)
    return b'\xd1' + big_indian
  elif -2147483648 <= value <= 2147483647:
    big_indian=struct.pack('>i', value)
    return b'\xd2' + big_indian
  elif -9223372036854775808 <= value <= 9223372036854775808:
    big_indian=struct.pack('>q', value)
    return b'\xd3' + big_indian
  
def serialize_unsigned_int(value):
  if 0 <= value <= 255:
    return bytes([0xcc|value])
  elif 0 <= value <= 65535:
    big_indian=struct.pack('>H', value)
    return b'\xcd' + big_indian
  elif 0 <= value <= 4294967295:
    big_indian=struct.pack('>I', value)
    return b'\xce' + big_indian
  elif -0 <= value <= 18446744073709551615:
    big_indian=struct.pack('>Q', value)
    return b'\xcf' + big_indian

def serialize_boolean(value):
  if value:
    return b'\xc3'
  else:
    return b'\xc2'
  
def serialize_float(value):
  if sys.getsizeof(value) <= 32:
    big_indian = struct.pack('>f', value)
    return b'\xca' + big_indian
  else:
    big_indian = struct.pack('>d', value)
    return b'\xcb' + big_indian

def serialize_str(value):
    size = len(value)
    if size <= 255:
        prefix = b'\xd9'
        length_field = struct.pack('B', size)  
    elif size <= 65535:
        prefix = b'\xda'
        length_field = struct.pack('>H', size)  
    elif size <= 4294967295:
        prefix = b'\xdb'
        length_field = struct.pack('>I', size)  

    return prefix + length_field + bytes(value)

if __name__== "__main__":
  print('----------------------')
  print(serialize_str("1"))
  print('-----------------------------')