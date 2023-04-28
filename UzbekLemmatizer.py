from pathlib import Path
from lxml import etree

__this_directory = Path(__file__).parent
__suff_tree = etree.parse(__this_directory/"suffixes.xml")

#global o`zgaruvchilar
__suff_root = __suff_tree.getroot()

# word_info=[maktablarning,maktab,[lar,ning],[fsm_id]]
__word_info=['null','null',[],[]]

def __construktor(word):
    __word_info.clear()
    __word_info.append(word)
    __word_info.append('null')
    __word_info.append([])
    __word_info.append([])

#fsm larni o`qib olish
__fsm=[0,0,0,0,0,0,0,0,0]
__fsm_tree = etree.parse(__this_directory/"fsms.xml")
__fsm_root = __fsm_tree.getroot()

for fsm_id in range(len(__fsm_root)):
    try:
        __fsm[fsm_id] = __fsm_root[fsm_id]
    except:
        print('FSM larni o`qib olishda muammo bor!')

#Main FSM, ways
__ways_number=[[0,1,2,6,7,8],[0,1,2,3,4,5,7,8],[0,3,4,5,7,8]]
__ways_result=[[],[],[]]


def __checkSuffix(local_root):
    suffix=local_root[0].text
    if len(__word_info[1])-len(suffix)<3:
        return False

    #exception_cut ni tekshirish
    if (not(local_root[1].text==None)):
        ex_cut = str(local_root[1].text).split(',')
        for ex in ex_cut:
            l = len(ex + suffix)
            if ((ex + suffix) == __word_info[1][-l:]):
                return True

    #exception_pass ni tekshirish
    if (not(local_root[2].text==None)):
        ex_pass = str(local_root[2].text).split(',')
        for ex in ex_pass:
            l = len(ex + suffix)
            if ((ex + suffix) == __word_info[1][-l:]):
                return False

    if (str(suffix) == __word_info[1][-len(suffix):]):
        return  True
    return False

def __cutSuffix(suffix):
    __word_info[1]=__word_info[1][:-len(suffix)]
    __word_info[2].insert(0,suffix)


def __predictPOS(fsm_list):
    pass

def __rootWord(fsm_id,A):

    root=__suff_root.findall(".//item[@fsm_id='"+str(fsm_id)+"']")
    #print(len(root))
    for suffix_id in A:
        suffix_id=int(suffix_id)-1
        if root[suffix_id].get('active')=='0':
            continue

        # qo`shimchaning allamorfi yo`q bo`lsa
        if (root[suffix_id][0].get('allomorph') == 'false'):
            suffix = root[suffix_id][0][0].text

            if __checkSuffix(root[suffix_id][0]):
                __cutSuffix(suffix)
                #__fsm_list[int(fsm_id)]['fsm'+str(fsm_id)].append(suffix_id)
                __word_info[3].insert(0,fsm_id)
                return True
            else:
                continue

        # qo`shimchaning allamorfi bo`lsa
        elif (root[suffix_id][0].get('allomorph') == 'true'):
            for allomorph in root[suffix_id][0]:
                suffix = allomorph[0].text

                if __checkSuffix(allomorph):
                    __cutSuffix(suffix)
                    #__fsm_list[int(fsm_id)]['fsm'+str(fsm_id)].append(suffix_id)
                    __word_info[3].insert(0, fsm_id)
                    return True
                else:
                    continue
    return False

def __call_fsm(fsm_id):
    #qoshimchalani qaytarib barish garak bolib qolsa
    stack=[]
    current_state = 'A'

    stop = True
    while stop:
        state = __fsm[fsm_id].find(".//state[@name='" + str(current_state) + "']")
        stack.append(state.get('finaly'))

        if (state.get('finaly') == 'stop'):
            break

        havesuffix = False
        for trans in state:

            A = str(trans.text).split(',')
            # print(A)
            if (__rootWord(fsm_id, A)):
                current_state = str(trans.get('to'))
                havesuffix=True
                break
            else:
                continue

        if not havesuffix:
            stop=False

    #xato qirqilgan qo`shimchalarni qaytarib berish.
    while stack.pop()=='false' and len(stack)>0:
        __word_info[1]=__word_info[1]+__word_info[2][0]
        __word_info[2].pop(0)
        #__fsm_list ni ham pop qilish garak
        #__fsm_list[fsm_id].pop()

def Lemma(word):

    if(len(word)>3):
        for w in range(len(__ways_number)):
            sublist=__ways_number[w]
            __construktor(word)
            __word_info[1] = (word)
            for i in sublist:
                __call_fsm(i)

            __ways_result[w]=__word_info.copy()

    #uzunligi 3 harfdan kichik sozlarni tekshirish
    else:
        __construktor(word)
        words=['ol','ur']
        for w in words:
            if word==w:
                __word_info[1]=w

    way_id=0

    #print(__ways_result)
    for i in range(1,len(__ways_result)):
        if len(__ways_result[way_id][1])>len(__ways_result[i][1]):
            way_id=i
    #print(__ways_result[way_id])

    return __ways_result[way_id]

