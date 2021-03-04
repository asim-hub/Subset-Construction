import sys
from typing import List, Tuple, Set

State = int
Word = str
Configuration = Tuple[State, Word]
Transition = Tuple[State, Word, List[State]]
EPSILON = ""


class State:
    def __init__(self, nr_st, my_list):
        self.nr_st: int = nr_st
        self.my_list = my_list.copy()
        self.my_list.sort()


class NFA:
    def __init__(self, numberofstates: int, my_alphabet: Set[chr], finalstates, my_delta):
        self.numberOfStates = numberofstates
        self.states = set(range(self.numberOfStates))
        self.alphabet = my_alphabet
        self.initialState = 0
        self.finalStates = finalstates
        self.delta = my_delta


def func_del(my_nfa: NFA, st: int, c: chr):
    if (st, c) in my_nfa.delta:
        return my_nfa.delta[(st, c)]
    else:
        return []


def eps_clos(my_nfa: NFA, st: int):
    new_set = [st]
    len_list = 0
    # tratez si cazul in care pot avea n epsilon consecutivi
    while len_list < len(new_set):
        if (new_set[len_list], EPSILON) in my_nfa.delta:
            for st in my_nfa.delta[(new_set[len_list], EPSILON)]:
                if st not in new_set:
                    new_set.append(st)
        len_list += 1
    return new_set


if __name__ == '__main__':

    with open(sys.argv[1]) as file:
        numberOfStates = int(file.readline().rstrip())
        finalStates = set(map(int, file.readline().rstrip().split(" ")))
        delta = dict()
        while True:
            transition = file.readline().rstrip().split(" ")
            if transition == ['']:
                break
            if transition[1] == "eps":
                transition[1] = EPSILON

            delta[(int(transition[0]), transition[1])] = set(map(int, transition[2:]))
        list_of_char = ""
        for (a, b) in delta:
            list_of_char += b + " "
        alphabet = set(list_of_char)

        nfa = NFA(
            numberofstates=numberOfStates,
            my_alphabet=alphabet,
            finalstates=finalStates,
            my_delta=delta
        )

    # new dictionar (out)
    new_numberOfStates = []
    new_finalStates = []
    new_delta = dict()
    new_alphabet = alphabet
    new_alphabet.remove(' ')

    # lista de stari
    L = []
    # id noua stare
    id_st = 0
    # starea initiala

    # lista de satri ale DFA-ului create pana acum (contine doar starea initiala)
    L.append(State(id_st, eps_clos(nfa, 0)))

    s_idex = 0

    # descopar noi stari ale dfa-ului si construiesc matricea de tranzitii (delta)
    while s_idex < len(L):
        for a in new_alphabet:
            # lista de stari posibile dintr-o stare a nfa-ului
            new_list = []
            for s in L[s_idex].my_list:
                n = func_del(nfa, s, a)
                for b in n:
                    if b not in new_list:
                        new_list.append(b)
            # lista cu inchiderile pe epsilon ale listei de mai sus
            eps_list = []
            for t in new_list:
                n = eps_clos(nfa, t)
                for b in n:
                    if b not in eps_list:
                        eps_list.append(b)
            # acesta lista v-a reprezenta o stare in dfa
            eps_list.sort()

            # verific daca lista obtinuta este deja intr-o stare din lista
            # daca nu creez o stare nou
            j = 0
            ok = 0
            # cazul in care exista o stare asociata pentru acea lista
            for lst in L:
                if lst.my_list == eps_list:
                    new_delta[(L[s_idex].nr_st, a)] = lst.nr_st
                    ok = 1
                    break
            # cazul in care nu ezista o stare asociata si creez una noua
            if ok == 0:
                id_st += 1
                L.append(State(id_st, eps_list))
                new_delta[(L[s_idex].nr_st, a)] = id_st

        s_idex += 1

    # scriu in fisierul de iesire
    f_out = open(sys.argv[2], "w")
    result = ""
    # numarul de stari din dfa
    result += str(len(L)) + '\n'

    # starile finale
    s_final = []
    for lst in L:
        for k in nfa.finalStates:
            if k in lst.my_list:
                s_final.append(lst.nr_st)
                break
    # sortez starile finale
    s_final.sort()

    # tranzitiile din dfa
    k = 0
    while k < len(s_final) - 1:
        result += str(s_final[k]) + ' '
        k += 1
    result += str(s_final[len(s_final) - 1]) + '\n'

    for new_s in new_delta:
        (a, b) = new_s
        result += str(a) + ' ' + str(b) + ' ' + str(new_delta[new_s]) + '\n'

    # scriu rezultatul in fisierul de iesire
    f_out.write(result)
