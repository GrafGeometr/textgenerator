import argparse
import os
from textgenerator import TextGenerator


def get_words(text, bad, end):
    res = []
    i = 0
    n = len(text)
    while i < n:
        if text[i] in end:
            res.append(text[i])
            i += 1
        elif text[i] not in bad:
            word = []
            j = i
            while j < n:
                if text[j] in end or text[j] in bad:
                    break
                word.append(text[j])
                j += 1
            i = j
            res.append(''.join(word).lower())
        else:
            i += 1
    return res


def go_on_files(folder, name):
    model = TextGenerator(name)
    if folder:
        file_names = os.listdir(folder)

        for file_name in file_names:
            print(f"Working on {file_name}")
            print("Loading")
            location = os.getcwd() + f'/{folder}/' + file_name
            try:
                with open(location, 'r', encoding='utf-8') as file:
                    bad_chars = """-\t\n,/–*-+«;»\\…|]qwertyuiopasdfghjklzxcvbnm[{}=)( @"#$%':^&~`<>"""
                    ends = '.!?'
                    text = get_words(file.read(), bad_chars, ends)
            except:
                with open(location, 'r') as file:
                    bad_chars = """-\t\n,/–*-+«;»\\…|]qwertyuiopasdfghjklzxcvbnm[{}=)( @"#$%':^&~`<>"""
                    ends = '.!?'
                    text = get_words(file.read(), bad_chars, ends)
            model.fit(text)
    else:
        text1 = input()
        bad_chars = """-\t\n,/*-+;\\…|–][«{}=)( »@"#$%':^&~`<>"""
        ends = '.!?'
        text = get_words(text1, bad_chars, ends)
        model.fit(text)


parser = argparse.ArgumentParser()
parser.add_argument("--input-dir")
parser.add_argument("--model")
args = parser.parse_args()

go_on_files(args.input_dir, args.model)

'py train.py --input-dir=data/ --model=model.pickle'
'py train.py --model=model.pickle'
