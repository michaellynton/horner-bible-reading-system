from itertools import cycle, zip_longest, count, repeat
import yaml
import pandas as pd
#import pendulum


'''
l1dict =    {'Matthew': 28, 
            'Mark': 16, 
            'Luke': 24, 
            'John': 21}
l2dict =    {'Genesis': 50,
            'Exodus': 40,
            'Leviticus': 27,
            'Numbers': 36,
            'Deuteronomy': 34}
l3dict =    {'Romans': 16,
            '1 Corinthians': 16,
            '2 Corinthians': 13,
            'Galatians': 6,
            'Ephesians': 6,
            'Philippians': 4,
            'Colossians': 4,
            'Hebrews': 13}
l4dict =    {'1 Thessalonians': 5,
            '2 Thessalonians': 3,
            '1 Timothy': 6,
            '2 Timothy': 4,
            'Titus': 3,
            'Philemon': 1,
            'James': 5,
            '1 Peter': 5,
            '2 Peter': 3,
            '1 John': 5,
            '2 John': 1,
            '3 John': 1,
            'Jude': 1,
            'Revelation': 22}
l5dict =    {'Job': 42,
            'Ecclesiastes': 12,
            'Song of Solomon': 8}
l6dict =    {'Psalms': 150}
l7dict =    {'Proverbs': 31}
l8dict =    {'Joshua': 24,
            'Judges': 21,
            'Ruth': 4,
            '1 Samuel': 31,
            '2 Samuel': 24,
            '1 Kings': 22,
            '2 Kings': 25,
            '1 Chronicles': 29,
            '2 Chronicles': 36,
            'Ezra': 10,
            'Nehemiah': 13,
            'Esther': 10}
l9dict =    {'Isaiah': 66,
            'Jeremiah': 52,
            'Lamentations': 5,
            'Ezekiel': 48,
            'Daniel': 12,
            'Hosea': 14,
            'Joel': 3,
            'Amos': 9,
            'Obadiah': 1,
            'Jonah': 4,
            'Micah': 7,
            'Nahum': 3,
            'Habakkuk': 3,
            'Zephaniah': 3,
            'Haggai': 2,
            'Zechariah': 14,
            'Malachi': 4}
l10dict =   {'Acts': 28}
'''

'''

list_1 = [f'Matthew {n}' for n in range(1,25)]\
         + [f'Mark {n}' for n in range(1,17)]
list_2 = [f'Genesis {n}' for n in range(1,53)]\
         + [f'Exodus {n}' for n in range(1,26)]


list_6 = [f'Psalms {n}' for n in range(1,151)]

list_7 = [f'Proverbs {n}' for n in range(1,32)]

cnt = 0

for k,v in list_1.items():
    for chap in range(1,v):
        cnt += 1
        print(f'day: {cnt}/n')
        print(f'{k}: {chap}')

list1 = []
list2 = []

plan = []
for k,v in l1dict.items():
        for chap in range(1,v+1):
    #        cnt += 1
            reading = f'{k} {chap}'
            plan.append(reading)
'''


def build_chapters(book_list):
    chapters = []
    for k,v in book_list.items():
        for chap in range(1,v+1):
            reading = f'{k} {chap}'
            chapters.append(reading)
    return chapters


#var1, var2, var3 = [test_list[i] for i in (1, 3, 5)]


'''
plan = list(zip(list_1, list_6, list_7))

list(zip(list_1, list_2, list_6))


# https://stackoverflow.com/questions/19686533/how-to-zip-two-differently-sized-lists-repeating-the-shorter-list
A = [1,2,3,4,5,6,7,8,9]
B = ["A","B","C"]

from itertools import cycle
zip_list = zip(A, cycle(B)) if len(A) > len(B) else zip(cycle(A), B)
zip_list = zip(list_1, cycle(list_2)) if len(list_1) > len(list_2) else zip(cycle(list_1), list_2)

# another solution


def zip_cycle(*iterables, empty_default=None):
    cycles = [cycle(i) for i in iterables]
    for _ in zip_longest(*iterables):
        yield tuple(next(i, empty_default) for i in cycles)

for i in zip_cycle(range(2), range(5), ['a', 'b', 'c'], []):
    print(i)


for i in count():
    print(i)
    if i > 3:
        break

print(list(zip(count(), list_1, list_2)))

'''


#####


# cycle each list and zip them. print each iteration until the value reaches 50
# could also set the start and end dynamically


def main():

    counter = 0
    start = 1
    end = 99
    reading_plan = []
    books = ['list_1', 
            'list_2',
            'list_3',
            'list_4',
            'list_5',
            'list_6',
            'list_7',
            'list_8',
            'list_9',
            'list_10',]

    with open('lists.yml', 'r') as file:
        lists = yaml.safe_load(file)

#mydict = {'raw':'data', 'code': 500}
#raw, code = [mydict.get(k) for k in ['raw','code']]


    #l1dict, l2dict, l3dict, l4dict, l5dict, l6dict, l7dict, l8dict, l9dict, l10dict = [lists.get(k) for k in books]
    #l1, l2, l3, l4, l5, l6, l7, l8, l9, l10 = [build_chapters(i) for i in (l1dict, l2dict, l3dict, l4dict, l5dict, l6dict, l7dict, l8dict, l9dict, l10dict)]
    
    # Combine the two lines above
    l1, l2, l3, l4, l5, l6, l7, l8, l9, l10 = [build_chapters(i) for i in [lists.get(k) for k in books]]

    for i in zip(count(start), cycle(l1), cycle(l2), cycle(l3), cycle(l4), cycle(l5), cycle(l6), cycle(l7), cycle(l8), cycle(l9), cycle(l10)):
        reading_plan.append(i)
        counter += 1
        if counter > end-1:
            break
    
    #print(reading_plan)

    #for a,b,c,d,e,f,g,h,i,j,k in reading_plan:
        #print(f"{a}\t{b}\t{c}\t{d}\t{e}\t{f}\t{g}\t{h}\t{i}\t{j}\t{k}")


    df = pd.DataFrame(reading_plan, columns = ['Day'] + [b.title().replace('_',' ') for b in books])

    #file_dt = pendulum.now().to_date_string()
    filename = f'reading_{start}_{end}.csv'
    df.to_csv(filename, index=False)

'''
#cycle over the lists, zipped
print(list(zip(cycle(list_1), list_2)))


print(list(zip(repeat(100), list_1)))
'''

"""
# list the products
from itertools import product
list(product(range(2), range(5)))
#[(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 0), (1, 1), (1, 2), (1, 3), (1, 4)]
list(product(range(2), range(2)))
#[(0, 0), (0, 1), (1, 0), (1, 1)]
list(product(range(2), range(2), range(3)))
"""







# --------------------------------------------------
if __name__ == "__main__":
    main()
