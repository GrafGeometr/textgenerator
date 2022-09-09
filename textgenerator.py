import pickle
import random


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


class TextGenerator:
    def __init__(self, name):
        self.name = name
        self.fit_mode_on = False
        self.dist = 5
        try:
            with open(name, 'rb') as file:
                self.data = pickle.load(file)
                self.links = {}
        except Exception as e:
            self.data = {}
            self.links = {}

    def turn_fit_mode_on(self):
        if not self.fit_mode_on:
            for x in self.data.keys():
                self.links[x] = {}
                self.links[x]['sum'] = 0
                self.links[x]['words'] = {}
                self.links[x]['left'] = {}
                for i in range(len(self.data[x])):
                    self.links[x]['sum'] += self.data[x][i][1]
                    self.links[x]['words'][self.data[x][0]] = i
                    if i == 0 or self.data[x][i - 1][1] != self.data[x][i][1]:
                        self.links[x]['left'][self.data[x][i][1]] = i
            self.fit_mode_on = True

    def fit(self, text):
        self.turn_fit_mode_on()
        print("Analyzing")
        n = len(text)
        percents = 0
        for i in range(n):
            if int(i / (n + 1) * 100) > percents + 9:
                percents = int(i / (n + 1) * 100)
                print(f'{percents}% completed')
                self.save(self.name)
            for k in range(self.dist):
                if i + k + 1 >= n:
                    break
                comb = tuple(text[i:i + k + 1])
                word = text[i + k + 1]
                self.data[comb] = self.data.get(comb, [])
                self.links[comb] = self.links.get(comb, {'sum': 0, 'words': {}, 'left': {}})
                self.links[comb]['sum'] = self.links[comb]['sum'] + 1
                pos = self.links[comb]['words'].get(word, None)
                if pos is None:
                    self.data[comb].append((word, 0))
                    pos = len(self.data[comb]) - 1
                    self.links[comb]['words'][word] = pos
                reit = self.data[comb][pos][1]
                self.links[comb]['left'][reit] = self.links[comb]['left'].get(reit, pos)
                self.data[comb][pos] = (word, self.data[comb][pos][1] + 1)
                self.data[comb][pos], self.data[comb][self.links[comb]['left'][reit]] = self.data[comb][
                                                                                            self.links[comb][
                                                                                                'left'][reit]], \
                                                                                        self.data[comb][pos]
                self.links[comb]['words'][word] = self.links[comb]['left'][reit]
                self.links[comb]['words'][self.data[comb][pos][0]] = pos
                if self.links[comb]['left'][reit] != pos:
                    self.links[comb]['left'][reit] += 1
                    if self.links[comb]['left'][reit] >= len(self.data[comb]) or \
                            self.data[comb][self.links[comb]['left'][reit]][1] != reit:
                        self.links[comb]['left'].pop(reit)
                self.links[comb]['left'][reit + 1] = self.links[comb]['left'].get(reit + 1,
                                                                                  self.links[comb]['words'][
                                                                                      word])
        self.save(self.name)

    def generate(self, prefix, length):

        words = [x[0] for x in list(self.data.keys()) if len(x) == 1]
        if not prefix:
            res = [random.choice(words)[0]]
            prefix = []
        else:
            res = get_words(' '.join(prefix.copy()), bad="""-\t\n,/–*-+«;»\\…|]qwertyuiopasdfghjklzxcvbnm[{}=)( @"#$%':^&~`<>""", end='.!?')
        x = 0
        while x < length:
            candidates = []
            for t in range(self.dist - 1, -1, -1):
                i = len(res) - 1 - t
                if t < 0:
                    continue
                group = tuple(res[i:])
                candidates.extend(self.data.get(group, [])[:2])
            # print(res[-1], candidates)
            if not candidates:
                res.append(random.choice(words)[0])
            else:
                res.append(candidates[random.randrange(len(candidates) // 2 + 1)][0])
            x += 1
        return ' '.join(res[len(prefix):])

    def save(self, name):
        with open(name, 'wb') as file:
            pickle.dump(self.data, file)
