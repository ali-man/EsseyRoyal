import re

WORDS = [
    'contact',
    ' me ',
    'email',
    'mail',
    '@',
    'gmail',
    '.com',
    'direct',
    'phone',
    'reach',
    'out',
    'whatsup',
    'telegram',
    'facebook',
    'social network',
    'find me',
    'instagram',
    'hi',
]

if __name__ == '__main__':
    TEXT = 'Find me Alitelegramsher 914266874 Rustamovich me mail'

    # --------- ПОИСК СЛОВ ---------------
    def search_word(x):
        return re.search(x, TEXT.lower())


    b = filter(search_word, WORDS)
    print(list(b))


    # ------------------------------------
    ######################################
    # --------- ПОИСК ЧИСЕЛ --------------
    def search_numbers(txt):
        import re
        re.findall('(\d+)', txt)  # ['914266874']


    def search_numbers2(txt):
        for i in filter(str.isdigit, txt):
            print(i)
    # ------------------------------------
