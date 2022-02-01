from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GOval, GRect, GLabel
from campy.gui.events.mouse import onmouseclicked, onmousemoved
from campy.graphics.gimage import GImage
from random import choice
from graphics import graphics
graphics=graphics()

def main():
    #print(list(map(lambda x:x.index, graphics.data.card)))
    onmouseclicked(click)
    

def click(event): 
    click_point=graphics.window.get_object_at(event.x, event.y)
    
    if graphics.take==0:
        if click_point is None:
            pass
        #沒拿東西，按右邊玩家資訊
        elif click_point in graphics.right_player_icon:
            click_right_player_icon(click_point)
        #沒拿東西，按中間城池
        elif click_point in graphics.center_icon:
            #佔領時不可更換城池
            if sum(list(map(lambda x:len(x), graphics.turn_put_dice)))==0:
                click_center_icon(click_point)
        
        elif click_point is graphics.roll_button:
            dice_rolling()
        #沒拿東西，按骰面
        elif click_point in graphics.dice_list:
            if click_point.filename !="age_of_war/image/start.png":
                graphics.take=1
                graphics.hand_dice_index=graphics.dice_list.index(click_point)
                graphics.hand_dice=graphics.dice_list[graphics.hand_dice_index]
                graphics.window.remove(graphics.hand_dice)
                graphics.window.add(graphics.hand_dice)
                onmousemoved(move)
            else:
                pass
        #點擊到額外的將軍
        elif graphics.left_condition is not None and graphics.left_condition.satisfy_extra_general is not None and click_point is graphics.left_condition.extra_general_image[0]:
            click_take_dice_to_origin(click_point)
        #點擊到非額外的將軍
        
        elif graphics.left_condition is not None and sum(list(map(lambda x: click_point in x,graphics.left_condition.condition_black_image)))==1:
            click_take_dice_to_origin(click_point)

    #有拿東西
    else:
        graphics.window.remove(graphics.hand_dice)
        click_point=graphics.window.get_object_at(event.x, event.y)
        graphics.window.add(graphics.hand_dice)
        if click_point is None:
            click_image_back(click_point)
        else:
            #偵測extra_general與手上物件的filename[17]一樣,extra general的滿足條件沒達成
            #有人已佔領但還沒滿足條件
            if graphics.left_condition.satisfy_extra_general is not None and graphics.left_condition.satisfy_extra_general==0 and click_point is graphics.left_condition.extra_general_image[0] and click_point.filename[17]==graphics.hand_dice.filename[17]:
                #將圖片放入extra使滿足＝1,手上沒東西take變成0,move(stop),將這回合動作放入此回合(list),移除圖片,檢查下個回合
                #在left_condition.extra_general_image[1]放入graphics.hand_dice(物件)
                graphics.left_condition.extra_general_image.append(graphics.hand_dice)
                graphics.left_condition.satisfy_extra_general=1
                change_image_black_to_other(graphics.left_condition.extra_general_image[0])
                graphics.take=0
                onmousemoved(stop)
                #把圖片放進去儲存在第幾回合
                graphics.turn_put_dice[graphics.turn].append(graphics.hand_dice)
                #print(graphics.turn_put_dice[graphics.turn].index(graphics.hand_dice))
                graphics.window.remove(graphics.hand_dice)
                #check
                check_next_turn()
            #偵測到條件 裡面成立則出來是1
            elif sum(list(map(lambda x:sum(list(map(lambda y:click_point is y,x))), graphics.left_condition.condition_black_image))):
                #先找偵測得條件是在啊個i,j
                for i in range(len(graphics.left_condition.condition_black_image)):
                    for j in range(len(graphics.left_condition.condition_black_image[i])):
                        if graphics.left_condition.condition_black_image[i][j] is click_point:
                            condition_i=i
                            condition_j=j
                #偵測兩張圖相同,且條件還未滿足
                if click_point.filename[17]==graphics.hand_dice.filename[17] and graphics.left_condition.satisfy_condition[condition_i][condition_j]==0:
                    #放入condition_dice_in
                    graphics.left_condition.condition_dice_in[condition_i][condition_j].append(graphics.hand_dice)
                    #把圖片加入這回合（turn 0,1,2...）
                    graphics.turn_put_dice[graphics.turn].append(graphics.hand_dice)
                    #print(graphics.turn_put_dice[graphics.turn].index(graphics.hand_dice))
                    #觀察是否滿足條件
                    #如果是步兵
                    if graphics.hand_dice.filename[17]=="F":
                        #計算步兵數量
                        F_num=graphics.hand_dice.filename.count("F")
                        #找出label的位置**** (只可能為1或2 第一行是步兵 第二行是步兵)
                        for i in range(len(graphics.left_condition.label)):
                            if graphics.left_condition.label[i][1]==condition_i and graphics.left_condition.label[i][2]==condition_j:
                                label=graphics.left_condition.label[i]
                        remind=int(label[3].text[2:])-F_num #X代表0,空格代表1,2後面為數字
                        label[3].text=f'X {remind}'
                        if remind<1:
                            graphics.left_condition.satisfy_condition[condition_i][condition_j]=1
                            change_image_black_to_other(graphics.left_condition.condition_black_image[condition_i][condition_j])           
                    #如果不是步兵
                    else:
                        graphics.left_condition.satisfy_condition[condition_i][condition_j]=1
                        change_image_black_to_other(graphics.left_condition.condition_black_image[condition_i][condition_j])
                    #移除圖片
                    graphics.window.remove(graphics.hand_dice)
                    #讓變數變為初始
                    graphics.hand_dice=None
                    graphics.hand_dice_index=None
                    #停止move, take回到0
                    onmousemoved(stop)
                    graphics.take=0
                    #check
                    check_next_turn()
                else:
                    click_image_back(click_point)
            else:
                click_image_back(click_point)

def click_right_player_icon(click_point):
    #right_player_icon_build
    right_player_index=graphics.right_player_icon.index(click_point)
    if len(graphics.right_player_card[right_player_index])==0:
        #family
        for i in range(len(graphics.data.players[right_player_index].card[0])):
            s=f"{graphics.data.players[right_player_index].card[0][i].scord},{graphics.data.players[right_player_index].card[0][i].name}"
            graphics.right_player_card[right_player_index].append(GLabel(s))
            graphics.right_player_card[right_player_index][-1].font="-20"
            graphics.right_player_card[right_player_index][-1].color=graphics.data.players[right_player_index].card[0][i].color
            graphics.window.add(graphics.right_player_card[right_player_index][-1],x=900,y=click_point.y+30*(len(graphics.right_player_card[right_player_index])))
        #card
        for i in range(len(graphics.data.players[right_player_index].card[1])):
            s=f'{graphics.data.players[right_player_index].card[1][i].scord},{graphics.data.players[right_player_index].card[1][i].name},{graphics.data.players[right_player_index].card[1][i].family.name}'
            graphics.right_player_card[right_player_index].append(GLabel(s))
            graphics.right_player_card[right_player_index][-1].font="-20"
            graphics.right_player_card[right_player_index][-1].color=graphics.data.players[right_player_index].card[1][i].family.color
            graphics.window.add(graphics.right_player_card[right_player_index][-1],x=950,y=click_point.y+30*(len(graphics.right_player_card[right_player_index])))
        #right_player_icon_down
        for i in range(len(graphics.data.players)-1-right_player_index):
            graphics.right_player_icon[right_player_index+i+1].y+=30*len(graphics.right_player_card[right_player_index])
            for j in range(len(graphics.right_player_card[right_player_index+i+1])):
                graphics.right_player_card[right_player_index+i+1][j].y+=30*len(graphics.right_player_card[right_player_index])

    else:
        #remove
        for i in range(len(graphics.right_player_card[right_player_index])):
            graphics.window.remove(graphics.right_player_card[right_player_index][i]) #地址仍在graph.right_player_icon[click_players_index]
        #right_player_icon up
        for i in range(len(graphics.data.players)-1-right_player_index):
            graphics.right_player_icon[right_player_index+i+1].y-=30*len(graphics.right_player_card[right_player_index])
            #right_player_card_icon up
            for j in range(len(graphics.right_player_card[right_player_index+i+1])):
                graphics.right_player_card[right_player_index+i+1][j].y-=30*len(graphics.right_player_card[right_player_index])
        #clear
        graphics.right_player_card[right_player_index].clear()

def click_center_icon(click_point):
    #如果左邊有東西要先清除
    if len(graphics.left_info_icon)!=0: #因沒有東西所以不會先跑這段
        #刪除info
        for i in range(4):
            graphics.window.remove(graphics.left_info_icon[i])
        graphics.left_info_icon.clear()
        #刪除image
        for i in range(len(graphics.left_condition.condition_black_image)):
            for j in range(len(graphics.left_condition.condition_black_image[i])):
                graphics.window.remove(graphics.left_condition.condition_black_image[i][j])
        for i in range(len(graphics.left_condition.label)):
            graphics.window.remove(graphics.left_condition.label[i][-1])
        #刪除extra_general
        if graphics.left_condition.satisfy_extra_general is not None:
            graphics.window.remove(graphics.left_condition.extra_general_image[0])
        del graphics.left_condition
    #呼叫中央卡牌資訊 right_icon_index為card第幾個第一個為0
    right_icon_index=list(map(lambda x:x.name,graphics.data.card)).index(click_point.text.split(',')[2]) 
    s=[graphics.data.card[right_icon_index].owner,graphics.data.card[right_icon_index].scord,graphics.data.card[right_icon_index].family.name,graphics.data.card[right_icon_index].name]
    if s[0] is None:
        s[0]="無人"
    else:
        s[0]=s[0].name
    #加入左邊info
    for i in range(4):
        graphics.left_info_icon.append(GLabel(s[i]))
        graphics.left_info_icon[-1].font='-20'
        graphics.window.add(graphics.left_info_icon[-1],x=50,y=100+i*50)
    #把條件放上去(把地址放進left_condition)
    graphics.left_condition=graphics.left_condition_icon()

    if s[0] !="無人":
        graphics.left_condition.satisfy_extra_general=0
        graphics.left_condition.extra_general_image.append(GImage("age_of_war/image/G.png"))
        graphics.window.add(graphics.left_condition.extra_general_image[0],x=200,y=50)
        image_to_black(graphics.left_condition.extra_general_image[0])

    #condition
    #condition_dice_in加入[[]]
    #satisfy_condition[0]
    #condition_black_image[image1,image2...7]
    #i由上往下 j由左往右
    for i in range(len(graphics.data.card[right_icon_index].condition)): #條件
        graphics.left_condition.condition_dice_in.append([])
        graphics.left_condition.satisfy_condition.append([])
        graphics.left_condition.condition_black_image.append([])
        for j in range(len(graphics.data.card[right_icon_index].condition[i])):
            graphics.left_condition.condition_dice_in[i].append([])
            graphics.left_condition.satisfy_condition[i].append(0) #當有兩個東西時（同一行）原始為兩個0 同時滿足時則為1
            graphics.left_condition.condition_black_image[i].append(GImage(f'age_of_war/image/{graphics.data.card[right_icon_index].condition[i][j][0]}.png')) #condition[i][j][0]判斷兵種 [i][j]可能有很多ＦＦＦＦ
            graphics.window.add(graphics.left_condition.condition_black_image[i][-1],x=200+j*100,y=100+i*50)
            #圖片先加進來再轉顏色
            image_to_black(graphics.left_condition.condition_black_image[i][-1])
            if graphics.data.card[right_icon_index].condition[i][j][0]=="F":
                
                graphics.left_condition.label.append([])
                graphics.left_condition.label[-1].append(len(graphics.data.card[right_icon_index].condition[i][j])) #有很多Ｆ
                graphics.left_condition.label[-1].append(i) #由上往下i放[0,1]
                graphics.left_condition.label[-1].append(j) #由左往右j放[0,2]
                graphics.left_condition.label[-1].append(GLabel(f'X {len(graphics.data.card[right_icon_index].condition[i][j])}')) #[0,3]放GLabel可能有兩個步兵情況因此用-1較好不要寫0否則會重複讀取前一個
                graphics.left_condition.label[-1][-1].font="-50"
                graphics.left_condition.label[-1][-1].color="black"
                graphics.window.add(graphics.left_condition.label[-1][-1],x=200+j*100+50,y=100+i*50+50)
            
def image_to_black(image):
    for i in range(50):
        for j in range(50):
            s=[image.get_pixel(i,j).red,image.get_pixel(i,j).green,image.get_pixel(i,j).blue]
            if s!=[255,255,255]:
                image.set_pixel(i,j,(0,0,0))
    return image      

def change_image_black_to_other(image):
    #找尋屬於對的顏色
    rgb=graphics.color[list(map(lambda x:x[0],graphics.color)).index(image.filename[17])][1]
    for i in range(50):
        for j in range(50):
            #若為黑色部分
            if image.get_pixel(i,j).red==0 and image.get_pixel(i,j).green==0 and image.get_pixel(i,j).blue==0:
                image.set_pixel(i,j,rgb)

def dice_rolling():
    #把一行使用骰子計算出來 list後面可能是[1 2 0 1]
    dice_use_number=sum(list(map(lambda x:len(x),graphics.turn_put_dice)))
    #當沒有left資料時
    if  graphics.left_condition==None:
        now_satisfy=0
    else:
        #滿足一行條件 
        ##0:沒滿足，1:滿足
        #a=[[1,1],[0],[0],[1,0,0]]
        #[0,0],[1],[1],[0,1,1]
        #0+1+1+2=4
        #1+0+0+0=1
        #now_satisfy=sum(list(map(lambda x:sum(list(map(lambda y:y==0,x)))==0,a)))
        #print(now_satisfy)
        #satisfy condition為個別滿足資格
        #裡面的lambda==0出來是true但sum==0找false條件（滿足一行條件的），外面lambda解開外層[],出來找到幾行滿足條件
        now_satisfy=sum(list(map(lambda x:sum(list(map(lambda y:y==0,x)))==0,graphics.left_condition.satisfy_condition)))-graphics.satify_number
    if now_satisfy==0:
        graphics.punishment+=1
    
    if now_satisfy<=1:
        if 7-graphics.punishment-dice_use_number==0:
            #下一個回合
            graphics.now_index+=1
            remove_all()
        else:
            for i in range(len(graphics.dice_list)):
                graphics.window.remove(graphics.dice_list[i])
            graphics.dice_list.clear()
            for i in range(7-graphics.punishment-dice_use_number): #7個骰子
                random_surface=choice(graphics.dice_image_FILENAME) #6個面
                graphics.dice_list.append(GImage(random_surface))
                graphics.window.add(graphics.dice_list[i],x=50+i*30,y=500+(i%2)*100)
            graphics.turn+=1
            #每個回合在（turn_put_dice)加一個[]=>[[]]
            graphics.turn_put_dice.append([])
            if graphics.left_condition is None:
                graphics.satify_number=0
            else:
                graphics.satify_number=sum(list(map(lambda x:sum(list(map(lambda y:y==0,x)))==0,graphics.left_condition.satisfy_condition)))

def click_take_dice_to_origin(click_point):
    #extra_general滿足＝1且點擊到那個位置
    if graphics.left_condition.satisfy_extra_general==1 and click_point is graphics.left_condition.extra_general_image[0]:
        #這回合滿足條件才能動作 #turn為第幾回合
        if sum(list(map(lambda x:x is graphics.left_condition.extra_general_image[1],graphics.turn_put_dice[graphics.turn])))==1:
            #拿出後不滿足
            graphics.left_condition.satisfy_extra_general=0
            #放下時黑變彩，此時要變回黑色
            image_to_black(graphics.left_condition.extra_general_image[0])
            #將有顏色的圖片加回來
            graphics.window.add(graphics.left_condition.extra_general_image[1])
            #尋找原本圖片的位置(在dice_list的位置)
            i=graphics.dice_list.index(graphics.left_condition.extra_general_image[1])
            graphics.left_condition.extra_general_image[1].x=50+i*30
            graphics.left_condition.extra_general_image[1].y=500+(i%2)*100
            #刪除這回合的move
            graphics.turn_put_dice[graphics.turn].remove(graphics.left_condition.extra_general_image[1])
            #刪除黑色image的彩色位置
            graphics.left_condition.extra_general_image.pop()
    else:
        #找出偵測圖片在哪個i(上到下),j(左到右)
        for i in range(len(graphics.left_condition.condition_black_image)):
            for j in range(len(graphics.left_condition.condition_black_image[i])):
                if graphics.left_condition.condition_black_image[i][j] is click_point:
                    condition_i=i
                    condition_j=j
        #print(graphics.left_condition.condition_dice_in[condition_i])
        #print(len(graphics.left_condition.condition_dice_in[condition_i][condition_j]))
        #print(list(map(lambda x:x==graphics.left_condition.condition_dice_in[condition_i][condition_j][-1],graphics.turn_put_dice[graphics.turn])))
        if len(graphics.left_condition.condition_dice_in[condition_i][condition_j])!=0 and sum(list(map(lambda x:x==graphics.left_condition.condition_dice_in[condition_i][condition_j][-1],graphics.turn_put_dice[graphics.turn])))==1:
            #點擊的物件
            ob=graphics.left_condition.condition_dice_in[condition_i][condition_j][-1]
            #拿出後不滿足
            graphics.left_condition.satisfy_condition[condition_i][condition_j]=0
            image_to_black(graphics.left_condition.condition_black_image[condition_i][condition_j])
            graphics.window.add(ob)
            i=graphics.dice_list.index(ob)
            ob.x=50+i*30
            ob.y=500+(i%2)*100
            #刪除這回合的move
            graphics.turn_put_dice[graphics.turn].remove(ob)
            #刪除黑色image的彩色位置
            graphics.left_condition.condition_dice_in[condition_i][condition_j].pop()
            if ob.filename[17]=="F":
                F_number=ob.filename.count("F")
                #找出label的位置**** (只可能為1或2 第一行是步兵 第二行是步兵)
                for i in range(len(graphics.left_condition.label)):
                    if graphics.left_condition.label[i][1]==condition_i and graphics.left_condition.label[i][2]==condition_j:
                        label=graphics.left_condition.label[i]
                plus=int(label[3].text[2:])+F_number #X代表0,空格代表1,2後面為數字
                label[3].text=f'X {plus}'

def click_image_back(click_point):
    graphics.take=0
    onmousemoved(stop)
    i=graphics.hand_dice_index
    graphics.hand_dice.x=50+i*30
    graphics.hand_dice.y=500+(i%2)*100
    graphics.hand_dice=None
    graphics.hand_dice_index=None

def move(event):
    graphics.hand_dice.x=event.x-graphics.hand_dice.width/2
    graphics.hand_dice.y=event.y-graphics.hand_dice.height/2     

def stop(event):
    pass

def check_next_turn(): #####
    if graphics.left_condition==None:
        now_satisfy=0
    else:
        now_satisfy=sum(list(map(lambda x:sum(list(map(lambda y:y==0,x)))==0,graphics.left_condition.satisfy_condition)))-graphics.satify_number
    if now_satisfy<=1:
        #當extra符合且其他行未滿足的條件（!=0）==0
        if (graphics.left_condition.satisfy_extra_general==1 or graphics.left_condition.satisfy_extra_general is None) and (sum(list(map(lambda x:sum(list(map(lambda y:y==0,x)))!=0,graphics.left_condition.satisfy_condition)))==0):
            #尋找完成條件卡牌地址(城池名)
            card_address=graphics.data.card[list(map(lambda x:x.name, graphics.data.card)).index(graphics.left_info_icon[3].text)]
            #將無人的城池從nobody移出
            if card_address.owner is None:
                graphics.data.nobody.card.remove(card_address)
            #若有人的要從那人位置移除(card[1]為散卡區)
            else:
                card_address.owner.card[1].remove(card_address)
            #存入佔領的玩家
            card_address.owner=graphics.data.players[graphics.now_index%len(graphics.data.players)]
            card_address.owner.card[1].append(card_address)

            #判斷此卡是否湊齊家族
            own_player=card_address.owner
            if sum(list(map(lambda x:x.owner!=own_player,card_address.family.card)))==0: ####
                card_address.family.owner=card_address.owner
                card_address.owner.card[0].append(card_address.family)
                for i in range(len(card_address.family.card)):
                    card_address.owner.card[1].remove(card_address.family.card[i])

            if len(graphics.data.nobody.card)==0:
                call_game()
            else:
                graphics.now_index+=1 #換下一個人
                remove_all()
        #未全部滿足繼續跑
        else:
            pass

def remove_all():
    #右
    for i in range(len(graphics.right_player_icon)):
        graphics.window.remove(graphics.right_player_icon[i])
    for i in range(len(graphics.right_player_card)):
        for j in range(len(graphics.right_player_card[i])):
            graphics.window.remove(graphics.right_player_card[i][j])
    #中
    for i in range(len(graphics.center_icon)):
        graphics.window.remove(graphics.center_icon[i])
    for i in range(len(graphics.player)):
        graphics.window.remove(graphics.player[i])
    #左
    if graphics.left_condition.satisfy_extra_general is not None:
        graphics.window.remove(graphics.left_condition.extra_general_image[0])
    for i in range(len(graphics.left_info_icon)):
        graphics.window.remove(graphics.left_info_icon[i])
    for i in range(len(graphics.left_condition.condition_black_image)):
        for j in range(len(graphics.left_condition.condition_black_image[i])):
            graphics.window.remove(graphics.left_condition.condition_black_image[i][j])
    for i in range(len(graphics.left_condition.label)):
        graphics.window.remove(graphics.left_condition.label[i][3]) #:號後

    #骰子
    for i in range(len(graphics.dice_list)):
        graphics.window.remove(graphics.dice_list[i])
    graphics.window.remove(graphics.now)
    graphics.window.remove(graphics.dice_roll_build)
    graphics.start()
    click_right_player_icon(graphics.right_player_icon[graphics.now_index%len(graphics.data.players)])
    
def call_game():
    pass

if __name__=="__main__":
    main()
