
class player:
    def __init__(self,name):
        self.name=name
        self.index=None
        self.card=[[],[]] #[]第一個擁有家族 []第二個散卡
        self.scord=0

class nobody:
    def __init__(self):
        self.card=[]

class card:
    def __init__(self):
        self.index=0
        self.family=None #family為object跑到下面
        self.name=None
        self.scord=None
        self.condition=[] #卡牌獲取條件
        self.owner=None

class family: #顯示出想要的值
    def __init__(self):
        self.name=None 
        self.scord=None
        self.color=None
        self.card=[] #連到class card
        self.owner=None

FILE="age_of_war/data.txt"

class all_data:
    def __init__(self):
        l=[self.family,self.card,self.dice,self.players]=[],[],[],['玩家一','玩家二','玩家三','玩家四']
        self.data_in_tree(l)
        self.card_connect_family(l)
        self.player_in_tree(l)
        self.nobody_list(l)
        
        
    def data_in_tree(self,l):
        def family_in_data(s):
            s=s.split(',')
            family_id=family()
            family_id.name=s[0]
            family_id.scord=s[1]
            family_id.color=s[2]
            return family_id

        def card_in_data(s):
            s=s.split(',')
            card_id=card()
            card_id.family=s[0]
            card_id.name=s[1]
            card_id.scord=s[2]
            card_id.condition=list(map(lambda x:list(map(lambda y:y[0]*int(y[1:]), x.split('+'))), s[3].split('&')))
            return card_id

        def dice_in_data(s):
                return s[0]*int(s[1:])

        index=['f','c','d']
        with open(FILE,'r') as f:
            for line in f:
                if line.strip()[0] in index:
                    n=index.index(line.strip()[0])
                    continue
                else:
                    s=line.strip()
                    if n==0:
                        l[n].append(family_in_data(s))
                    elif n==1:
                        l[n].append(card_in_data(s))
                    elif n==2:
                        l[n].append(dice_in_data(s))

    # def card_connect_family(self,l):
    #     for i in range(len(l[1])):
    #         l[0][list(map(lambda x:x.name, l[0])).index(l[1][i].family)].card.append(l[1][i]) 
    #         l[1][i].family=l[0][list(map(lambda x:x.name, l[0])).index(l[1][i].family)]

    def card_connect_family(self,l):
        for i in range(len(l[1])): #l[1] card
            for j in range(len(l[0])): #l[0] family
                if l[1][i].family==l[0][j].name:
                    l[1][i].family=l[0][j]
                    l[0][j].card.append(l[1][i])


    def player_in_tree(self,l):
        for i in range(len(l[3])):
            n=player(l[3][i])
            l[3][i]=n
            l[3][i].index=i

    def nobody_list(self,l):
        self.nobody=nobody()
        for i in range(len(self.card)):
            self.nobody.card.append(self.card[i])
            
def main():
    print(all_data().players[1].name)

if __name__=="__main__":
    main()
