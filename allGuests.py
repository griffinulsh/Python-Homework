
allGuests = {'Alice': {'apples': 5, 'pretzels': 12},
    'Bob': {'ham sandwiches': 3, 'apples': 2},
    'Carol': {'cups': 3, 'apple pies': 1}}

def totalBrought(guests, item):
    numBrought = 0
    for k, v in guests.items():
        numBrought = numBrought + v.get(item, 0)
    return numBrought

print('Number of things being brought:')
print('  Apples           ' + str(totalBrought(allGuests, 'apples')))
print('  Cups             ' + str(totalBrought(allGuests, 'cups')))
print('  Ham Sandwiches   ' + str(totalBrought(allGuests, 'ham sandwiches')))
print('  Apple Pies       ' + str(totalBrought(allGuests, 'apple pies')))
print('  Pretzels         ' + str(totalBrought(allGuests, 'pretzels')))
print('  Cookies          ' + str(totalBrought(allGuests, 'cookies')))

"""
Practice Questions:
-What does the code for an empty dictionary look like? - {}

-What does a dictionary value with a key 'foo' and value '42' look like? - {'foo': 42}

-What is the main difference between a list and a dictionary? - Lists are ordered, dictionaries are not.

-What happens if you try to access spam['foo'] if spam is {'bar': 100}? - KeyError

-If a dictionary is stored in spam, what is the difference between the expressions 'cat' in spam and 'cat' in spam.keys()? - The first
will raise a KeyError, the second will return False

-If a dictionary is stored in spam, what is the difference between the expressions 'cat' in spam and 'cat' in spam.values()? - The first
will raise a KeyError, the second will return True

-What is a shortcut for the following code?

if 'color' not in spam:
    spam['color'] = 'black'

spam.setdefault('color', 'black')

-What module and function can you use to "pretty print" dictionary values? - pprint
"""

#Practice Assignment: Fantasy Game Inventory

playerInventory = {
    'arrow' : 12,
    'gold coin' : 42,
    'rope' : 1,
    'torch' : 6,
    'dagger' : 1
}

def displayInventory(inventory):
    print("Inventory: ")
    item_total = 0
    for k, v in inventory.items():
        print(f" {k.capitalize()}: {v}")
        item_total += v
    print("Total number of items: " + str(item_total))

displayInventory(playerInventory)