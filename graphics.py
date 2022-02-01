from typing import List
from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GOval, GRect, GLabel
from campy.graphics.gimage import GImage
from campy.gui.events.mouse import onmouseclicked
from data import all_data
import random

WIN_WIDTH=1400
WIN_HEIGHT=800
PLAYER_WIDTH=900
PLAYER_HEIGHT=60

data=all_data()

class graphics:
    def __init__(self):
        self.data=all_data()
        self.window=GWindow(WIN_WIDTH,WIN_HEIGHT,title='Age of War')
        self.dice_image_FILENAME=["age_of_war/image/G.png","age_of_war/image/B.png","age_of_war/image/H.png","age_of_war/image/F.png","age_of_war/image/FF.png","age_of_war/image/FFF.png"]
        self.now_index=0
        #self.random_card()
        self.reorganize()
        self.start()
    
    
    def start(self):
        #當前滿足幾條橫排
        self.satify_number=0
        self.punishment=-1
        self.now=GLabel(f"現在的玩家：{self.data.players[self.now_index%4].name}",x=500,y=700)
        self.now.font="-50"
        self.window.add(self.now)
        #將黑白改成彩色[255,0,0]紅色等顏色
        #[255,255,255]白色,[0,0,0]黑色
        self.color=[["G",[255,0,0]],["B",[130,64,94]],["H",[0,255,0]],["F",[0,0,255]]]

        self.take=0 #判斷手上有沒有拿骰子
        #手上得骰面（image)跟此骰面在dice_list裡面的index
        self.hand_dice=None 
        self.hand_dice_index=None
        #放置當前骰面的list,裡面是image物件地址
        self.dice_list=[]
        #控制當前玩家回合數，turn_put_dice裡面放置每個回合所移動的骰子
        self.turn=-1
        self.turn_put_dice=[]

        self.right_player_icon=[] #right_side big_label_address
        self.right_player_card=[[],[],[],[]] #player[0].name,player[1].name,player[2].name,player[3].name
        self.right_player_icon_build()

        self.player=[]
        self.center_icon=[] #center cards
        self.center_build()


        self.left_info_icon=[] #owner,scord,name,family(left)
        self.left_condition=None #left 

        self.check_button_build()
        self.dice_build()
        self.dice_roll_build()


    class left_condition_icon:
        def __init__(self):
            self.extra_general_image=[]
            self.condition_black_image=[]
            self.condition_dice_in=[]
            self.satisfy_extra_general=None #if not center, extra general in attack condition
            self.satisfy_condition=[]
            self.label=[]

    def check_button_build(self):
        self.check_button=GLabel('check',x=1000,y=750)
        self.check_button.font='-50'
        self.window.add(self.check_button)

    def dice_build(self):
        for i in range(7):
            self.dice_list.append(GImage("age_of_war/image/start.png"))
            self.window.add(self.dice_list[-1],x=50+i*30,y=500+(i%2)*100)

    def dice_roll_build(self):
        self.roll_button=GLabel('ROLL',x=100,y=750)
        self.roll_button.font='-50'
        self.window.add(self.roll_button)

    def right_player_icon_build(self):
        for i in range(len(self.data.players)):
            s=f"{self.data.players[i].name}  scord: {sum(list(map(lambda x:int(x.scord),self.data.players[i].card[0])))+sum(list(map(lambda x:int(x.scord),self.data.players[i].card[1])))}"
            self.right_player_icon.append(GLabel(s))
            self.right_player_icon[-1].font='-40'
            self.window.add(self.right_player_icon[-1],x=PLAYER_WIDTH,y=PLAYER_HEIGHT+i*50)

    def center_build(self):
        #build center card
        center_card_y=0
        for i in range(len(self.data.nobody.card)): #無人區卡片顯示
            s=f"{self.data.nobody.card[i].scord},{self.data.nobody.card[i].family.name},{self.data.nobody.card[i].name}"
            self.player.append(GLabel("擁有者：無人",x=500,y=50))
            self.player[-1].font='-25'
            self.center_icon.append(GLabel(s,x=550,y=80+center_card_y*30))
            self.center_icon[-1].font='-20'
            self.center_icon[-1].color=self.data.nobody.card[i].family.color
            self.window.add(self.player[-1])
            self.window.add(self.center_icon[-1])
            center_card_y+=1
        #build player card
        for i in range(len(self.data.players)):
            self.player.append(GLabel("擁有者："+self.data.players[i].name,x=500,y=50+(i+center_card_y+1)*30))
            self.player[-1].font='-25'
            self.window.add(self.player[-1])
            for j in range(len(self.data.players[i].card[1])):
                s=f"{self.data.players[i].card[1][j].scord},{self.data.players[i].card[1][j].family.name},{self.data.players[i].card[1][j].name}"
                self.center_icon.append(GLabel(s,x=550,y=80+(i+center_card_y+1)*30))
                self.center_icon[-1].font='-20'
                self.center_icon[-1].color=self.data.players[i].card[1][j].family.color
                self.window.add(self.center_icon[-1])
                center_card_y+=1

    def random_card(self):
        for i in range(len(self.data.card)):
            c=self.data.players.copy()
            c.append(0) #加上中央區
            n=random.choice(c)
            if n==0:
                self.data.card[i].owner=None #發到中央區
            else:
                self.data.card[i].owner=n #n代表owner的卡,從中央區到玩家手中
                n.card[1].append(self.data.card[i]) #加入card[1]
                self.data.nobody.card.pop(self.data.nobody.card.index(self.data.card[i]))
        #     a=random.choice(data.players)
        #     data.card[i].owner=a #玩家與牌配對
        #     a.card[1].append(data.card[i]) #a.card為地址 card[1]為散牌
            
    def reorganize(self): #散卡與蒐集完的卡分類
        for i in range(len(self.data.family)): #6次
            len_family_card=len(self.data.family[i].card) #各個家族擁有幾張卡12243
            a=[]
            for j in range(len_family_card):
                a.append(self.data.family[i].card[j].owner) #a為地址(導向owner)
            for k in range(len(a)):
                if a[k]==a[0]:
                    collect=1
                else:
                    collect=0
                    break
            if collect==1 and a[0] is not None: #收集到同家族
                a[0].card[0].append(self.data.family[i])
                for z in range(len(self.data.family[i].card)):
                    a[0].card[1].pop(a[0].card[1].index(self.data.family[i].card[z]))
   
    def card_list_build(self):
        self.card_list=[]

    def attack_card_detail_build(self,s):
        #清除資料
        for a in range(len(self.attack_detail)):
            self.window.remove(self.attack_detail[a])
        self.attack_detail.clear()

        for b in range(len(self.attack_detail)):
            for c in range(len(self.attack_detail[b])):
                self.window.remove(self.attack_detail[b][c])
        self.attack_detail.clear()
        self.window.remove(self.extra_general)
        self.begin()

        card_index=list(map(lambda x:x.name,self.data.card)).index(s.text.split(' ')[2]) #s.text.split('')[2]指的是城池，[1]是{},[0]是家族
        owner=self.data.card[card_index].owner
        if owner is None:
            owner="無人"
        else:
            owner=owner.name
        #卡片屬於
        self.attack_detail.append(GLabel(owner,x=50,y=50))
        self.attack_detail[-1].font='-20'
        self.attack_detail[-1].color='black'
        self.window.add(self.attack_detail[-1])
        #分數
        self.attack_detail.append(GLabel(data.card[card_index].scord,x=50,y=100))
        self.attack_detail[-1].font='-20'
        self.attack_detail[-1].color='black'
        self.window.add(self.attack_detail[-1])
        #城池
        self.attack_detail.append(GLabel(data.card[card_index].name,x=50,y=150))
        self.attack_detail[-1].font='-20'
        self.attack_detail[-1].color='black'
        self.window.add(self.attack_detail[-1])
        #家族
        self.attack_detail.append(GLabel(data.card[card_index].family.name,x=50,y=200))
        self.attack_detail[-1].font='-20'
        self.attack_detail[-1].color='black'
        self.window.add(self.attack_detail[-1])
        #獲取城池條件
        if owner!="無人":
            self.extra_general=GImage("age_fo_war/image/G.png")
            self.extra_general.x=200
            self.extra_general.y=50
            self.extra_general_condition=0
            self.window.add(self.extra_general)
            self.change_black(self.extra_general)

        for i in range(len(self.data.card[card_index].condition)): #條件直行
            self.attack_detail_condition.append([])
            self.satify_condition.append([])
            for j in range(len(self.data.card[card_index].condition[i])): #條件橫向
                condition_name=self.data.card[card_index].condition[i][j] 
                if condition_name[0]=="F": #導入condition第一個位子Ｆ Ｂ...
                    F_number=len(condition_name)
                    condition_name=condition_name[0]
                self.attack_detail_condition[-1].append(GImage(f'age_of_war/image/{condition_name}.png'))
                self.satify_condition[-1].append(0) #為滿足條件為黑色
                self.attack_detail_condition[-1][-1].x=200+j*100
                self.attack_detail_condition[-1][-1].y=100+i*50
                self.window.add(self.attack_detail_condition[-1][-1])
                self.change_black(self.attack_detail_condition[-1][-1])
                
                if condition_name=="F":
                    self.attack_detail_condition[-1].append(GLabel(f'X {F_number}',x=200+j*100+50,y=150+i*50))
                    self.attack_detail_condition[-1][-1].fonr='-50'
                    self.window.add(self.attack_detail_condition[-1][-1])
            
def click(m):
     pass

def main():
    onmouseclicked(click)
if __name__=="__main__":
    main()