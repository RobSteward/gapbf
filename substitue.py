def substitute(path):
  # See https://twrp.me/faq/openrecoveryscript.html
  # print(f"Received path '{path}'")
  # Define a dictionary with the substitutions
  substitutions = {
    9: ':',
    10: ';',
    11: '<',
    12: '=',
    13: '>',
    14: '?',
    15: '@',
    16: 'A',
    17: 'B',
    18: 'C',
    19: 'D',
    20: 'E',
    21: 'F',
    22: 'G',
    23: 'H',
    24: 'I'
  }
    
  # Replace the elements in the path using the dictionary
  substituted_path = [str(substitutions.get(item, item)) for item in path]
  # print(f"Substituted path '{substituted_path}'")
  return substituted_path

#  0 - 1 - 2 - 3 - 4
#  |   |   |   |   |
#  5 - 6 - 7 - 8 - 9
#  |   |   |   |   |
#  10 11  12  13  14
#  |   |   |   |   |
#  15 16  17  18  19
#  |   |   |   |   |
#  20 21  22  23  24 

#  1 - 2 - 3 - 4 - 5
#  |   |   |   |   |
#  6 - 7 - 8 - 9 - :
#  |   |   |   |   |
#  ;   <  =    >   ?
#  |   |   |   |   |
#  @   A   B   C   D
#  |   |   |   |   |
#  E   F   G   H  I