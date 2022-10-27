#using pygame as main canvas
import pygame

#using random to generate random points and transversals
import random

#init pygame
pygame.init()

#create a window(could be full screen)
screen = pygame.display.set_mode(pygame.display.FULLSCREEN)


#Create a Master grid for simulating the results
grid = []

#Start defining the initial lines and transversal

class line:
    def __init__(self):
        self.points = 65
        self.transversalcnt = 1

    def line(self,A=(0,0),B=(0,0)):
        global grid
        #输入统一的line格式
        grid.append([[chr(self.points),chr(self.points+1)],(A,B)])
        #ASCII码表+2这样可以让每一个点都不一样（不至于一道题用26个点吧）
        self.points += 2
        return True

    def segments(self,A=(0,0),B=(0,0)):
        #因为segments的定义在象限中和line一摸一样所以就直接调用line的操作
        line(A,B)
        return True

    def transversal(self,targetLine=('A','B')):
        #标记是否有可以做transversal的线或者线段
        flag = False
        #查找过程
        for i in range(len(grid)):
            if targetLine in grid[i]:
                #备注不要执行报错过程
                flag = True
                #随便选择一个点范围必须在segment定义域内
                pointLocation = random.randint(grid[i][1][1],grid[i][2][1])
                #一个没有长度的line就是一个点
                #grid.append([[chr(self.points),chr(self.points)],(pointLocation,pointLocation)])
                #生成一个随机的slope（也就是角度）
                slope = (random.randint(0,360),random.randint(0,360))
                grid.append([['t'+str(self.transversalcnt),'t'+str(self.transversalcnt)],((grid[i][1][0]+slope[0],pointLocation+slope[1]),(grid[i][1][0]-slope[0],pointLocation-slope[1]))])
                '''
                有点乱：这个是数据结构
                
                [[定义的点1，定义的点2]，（点一和点二的集合：（点一x轴+slope的run，点一y轴+slope的rise），（点二的x轴-slope的run，点二y轴-slope的rise））]
                '''


        #如果每有这个线段
        if flag == False:
            #报个错得了这个输入肯定有问题
            return SyntaxError

    def get_line_parameters(self,lineName='A'):
        #直接在数据库中找一下就ok了
        mark = -1
        #判断一下这个line是两个点还是一条线的总称
        if type(lineName) == str:
            #枚举grid反正不会超时不然做题的人会直接狂暴
            for i in range(len(grid)):
                if [lineName,lineName] in grid[i]:
                    mark = i
                    break
        else:
            #如果是两个点
            for i in range(len(grid)):
                if lineName in grid[i]:
                    mark = i
                    break
        #如果没有记录
        if mark == -1:
            #不存在这条线
            return False
        else:
            #计算斜率
            slope = (grid[mark][1][0]+grid[mark][2][0])/(grid[mark][1][1]+grid[mark][2][1])
            #买一送一，给两个point得了（省的以后在多做模块）
            point = (grid[mark][1],grid[mark][2])

            '''
            也是一个很烦人的数据点
            return格式：(slope的小数点，(p1x,p1y)，(p2x,p2y))
            '''

            return (slope,point)


#init class line
LINE = line()


#Get all the possible calculations for the theorms
class theorms:
    def __init__(self):
        pass

    def alternate(self,angleOneLoc,angleTwoLoc,mode="Interior"):
        '''
        直接生成一个模块来判断Alternate是否成立得了
        '''
        if mode == "Interior" and angleOneLoc in [3,4] and angleTwoLoc in [1,2]:
            if angleOneLoc == 3 and angleTwoLoc == 1:
                return True
            elif angleOneLoc == 4 and angleTwoLoc == 2:
                return True
            else:
                return False
        elif mode == "Exterior" and angleOneLoc in [1,2] and angleTwoLoc in [3,4]:
            if angleOneLoc == 2 and angleTwoLoc == 3 or angleOneLoc == 1 and angleTwoLoc == 4:
                return True
            else:
                return False
        
                
    def sameside(self,angleOneLoc,angleTwoLoc,mode="Interior"):
        '''
        直接生成一个模块来判断Sameside是否成立得了
        '''
        if mode == "Interior" and angleOneLoc in [3,2] and angleTwoLoc in [1,4]:
            if angleOneLoc == 3 and angleTwoLoc == 2:
                return True
            elif angleOneLoc == 4 and angleTwoLoc == 1:
                return True
            else:
                return False
        elif mode == "Exterior" and angleOneLoc in [1, 2] and angleTwoLoc in [3, 4]:
            if angleOneLoc == 1 and angleTwoLoc == 3 or angleOneLoc == 2 and angleTwoLoc == 4:
                return True
            else:
                return False
            

    def alternate_interior(self,A,B):
        '''
        输入的格式

        :param A（角1）: [点1/线1，transversal/线2，[上减下加--交错点1，上减下加--交错点2]]
        :param B（角2）: [点1/线1，transversal/线2，[上减下加--交错点1，上减下加--交错点2]]
        :return: 是否可以使用alternate_interior theorm
        '''
        #判断是否点1是个线或者一个点
        if 97 <= A[0] <= 122:
            #如果是小写字母那么就是线
            '''
            Alternate Interior Theorm只有在同一个transversal上的点才能够使用
            所以角1和角2的第二个参数：transversal必须不能是同一条
            当然，如果线1是同一条也可以把线1当作transversal看待，那么t就不能是同一条
            '''
            #如果有两条共同线段
            if A[0] == B[0] and A[1] == B[1]:
                #因为Alternate Interior不能在同一个线段上
                return False
            elif A[0] == B[0] or A[1] == B[1]:
                #两个相同的已经排除掉了，所以如果有一个相同则可以使用
                '''
                现在这个步骤比较麻烦，因为要判断某一个角是朝上或者朝下
                调用个线段的参数得了不然输入的数据更麻烦了
                我们只需要两条线的两个点/slope就够了
                
                NOPE
                
                Actually还有一个办法（刚才浪费了5分钟敲代码）
                我们只要知道那个线段的点一线段的正负极就OK了
                '''
                angleOneLoc = 0
                '''
                这不就是Quadrants嘛
                '''

                if '-' in A[2][0] and not '-' in A[2][1]:
                    angleOneLoc = 4
                    #一个y>x一个x>y,在两条交叉线段的时候是右下角
                elif '-' in A[2][0] and '-' in A[2][1]:
                    angleOneLoc = 3
                    #两个y>x,在两条交叉线的是左下角
                elif not '-' in A[2][0] and '-' in A[2][1]:
                    angleOneLoc = 2
                    #一个x>y一个x<y,在两条交叉线的是左上角
                else:
                    angleOneLoc = 1
                    #两个x>，在两条交叉线的右上角

                angleTwoLoc = 0

                #现在也给角2算一下位置
                '''
                很好，这里的注释也是复制黏贴的
                '''
                if '-' in B[2][0] and not '-' in B[2][1]:
                    angleTwoLoc = 4
                    #一个y>x一个x>y,在两条交叉线段的时候是右下角
                elif '-' in B[2][0] and '-' in B[2][1]:
                    angleTwoLoc = 3
                    #两个y>x,在两条交叉线的是左下角
                elif not '-' in B[2][0] and '-' in B[2][1]:
                    angleTwoLoc = 2
                    #一个x>y一个x<y,在两条交叉线的是左上角
                else:
                    angleTwoLoc = 1
                    #两个x>，在两条交叉线的右上角

                '''
                onTop = None
                #判断好了之后我们还需要判断A线段在上面还是B线段在上面
                if A[0] == B[0]:
                    #平行线段没有什么slope会导致两个东西不等的
                    if LINE.get_line_parameters(A[1])[1][1] < LINE.get_line_parameters(B[1])[1][1]:
                        onTop = 'B'
                    else:
                        onTop = 'A'
                        
                    #不可能有个elif如果A==B因为同一条线会被tuple数据格式删除掉
                
                else:
                    # 平行线段没有什么slope会导致两个东西不等的
                    if LINE.get_line_parameters(A[0])[1][1] < LINE.get_line_parameters(B[0])[1][1]:
                        onTop = 'B'
                    else:
                        onTop = 'A'

                    # 不可能有个elif如果A==B因为同一条线会被tuple数据格式删除掉
                '''

                #现在终于判断是否Alt Int了
                #if onTop == 'A': 这行注释掉了因为好像也没必要
                '''
                if angleOneLoc == 3 and angleTwoLoc == 2:
                    return True
                elif angleOneLoc == 4 and angleTwoLoc == 1:
                    return True
                '''

                return theorms.alternate(angleOneLoc,angleTwoLoc,"Interior")
            
                '''
                else:
                    if angleOneLoc == 3 and angleTwoLoc == 2:
                        return True
                    elif angleOneLoc == 4 and angleTwoLoc == 1:
                        return True
                '''
            else:
                #这两条线没有半毛钱关系用不了Alt Int Theorem
                return False
        else:
            #输入的线段是由两个点构造成的
            pass
        

    def alternate_exterior(self,A,B):
        '''
        输入的格式

        :param A（角1）: [点1/线1，transversal/线2，[上减下加--交错点1，上减下加--交错点2]]
        :param B（角2）: [点1/线1，transversal/线2，[上减下加--交错点1，上减下加--交错点2]]
        :return: 是否可以使用alternate_exterior theorm
        '''
         #判断是否点1是个线或者一个点
        if 97 <= A[0] <= 122:
            #如果是小写字母那么就是线
            '''
            Alternate Interior Theorm只有在同一个transversal上的点才能够使用
            所以角1和角2的第二个参数：transversal必须不能是同一条
            当然，如果线1是同一条也可以把线1当作transversal看待，那么t就不能是同一条
            '''
            #如果有两条共同线段
            if A[0] == B[0] and A[1] == B[1]:
                #因为Alternate Exterior必须在两个不同的线段上
                return False
            elif A[0] == B[0] or A[1] == B[1]:
                #两个相同的已经排除掉了，所以如果有一个相同则可以使用
                '''
                现在这个步骤比较麻烦，因为要判断某一个角是朝上或者朝下
                调用个线段的参数得了不然输入的数据更麻烦了
                我们只需要两条线的两个点/slope就够了
                
                NOPE
                
                Actually还有一个办法（刚才浪费了5分钟敲代码）
                我们只要知道那个线段的点一线段的正负极就OK了
                '''
                angleOneLoc = 0
                '''
                这不就是Quadrants嘛
                '''

                if '-' in A[2][0] and not '-' in A[2][1]:
                    angleOneLoc = 4
                    #一个y>x一个x>y,在两条交叉线段的时候是右下角
                elif '-' in A[2][0] and '-' in A[2][1]:
                    angleOneLoc = 3
                    #两个y>x,在两条交叉线的是左下角
                elif not '-' in A[2][0] and '-' in A[2][1]:
                    angleOneLoc = 2
                    #一个x>y一个x<y,在两条交叉线的是左上角
                else:
                    angleOneLoc = 1
                    #两个x>，在两条交叉线的右上角

                angleTwoLoc = 0

                #现在也给角2算一下位置
                '''
                很好，这里的注释也是复制黏贴的
                '''
                if '-' in B[2][0] and not '-' in B[2][1]:
                    angleTwoLoc = 4
                    #一个y>x一个x>y,在两条交叉线段的时候是右下角
                elif '-' in B[2][0] and '-' in B[2][1]:
                    angleTwoLoc = 3
                    #两个y>x,在两条交叉线的是左下角
                elif not '-' in B[2][0] and '-' in B[2][1]:
                    angleTwoLoc = 2
                    #一个x>y一个x<y,在两条交叉线的是左上角
                else:
                    angleTwoLoc = 1
                    #两个x>，在两条交叉线的右上角

                '''
                onTop = None
                #判断好了之后我们还需要判断A线段在上面还是B线段在上面
                if A[0] == B[0]:
                    #平行线段没有什么slope会导致两个东西不等的
                    if LINE.get_line_parameters(A[1])[1][1] < LINE.get_line_parameters(B[1])[1][1]:
                        onTop = 'B'
                    else:
                        onTop = 'A'
                        
                    #不可能有个elif如果A==B因为同一条线会被tuple数据格式删除掉
                
                else:
                    # 平行线段没有什么slope会导致两个东西不等的
                    if LINE.get_line_parameters(A[0])[1][1] < LINE.get_line_parameters(B[0])[1][1]:
                        onTop = 'B'
                    else:
                        onTop = 'A'

                    # 不可能有个elif如果A==B因为同一条线会被tuple数据格式删除掉
                '''

                #现在终于判断是否Alt Int了
                #if onTop == 'A': 这行注释掉了因为好像也没必要
                '''
                if angleOneLoc == 3 and angleTwoLoc == 2:
                    return True
                elif angleOneLoc == 4 and angleTwoLoc == 1:
                    return True
                '''
                return theorms().alternate(angleOneLoc,angleTwoLoc,"Exterior")
            
                '''
                else:
                    if angleOneLoc == 3 and angleTwoLoc == 2:
                        return True
                    elif angleOneLoc == 4 and angleTwoLoc == 1:
                        return True
                '''
            else:
                #这两条线没有半毛钱关系用不了Alt Int Theorem
                return False
        else:
            #输入的线段是由两个点构造成的
            pass
        

    def sameside_interior(self,A,B):
        '''
        输入的格式

        :param A（角1）: [点1/线1，transversal/线2，[上减下加--交错点1，上减下加--交错点2]]
        :param B（角2）: [点1/线1，transversal/线2，[上减下加--交错点1，上减下加--交错点2]]
        :return: 是否可以使用sameside interior theorm
        '''
        #如果是一条线的名称
        if 97 <= A[0] <= 122:
            #如果两个共同线段
            if A[0] == B[0] and A[1] == B[1]:
                return False
            elif A[0] == B[0] or A[1] == B[1]:
                '''
                下一步就是判断是否两个临近transversal的角是否是在同一条边上
                如果不是的话就只能使用alternate exterior/interior Theorms
                '''
                #象限判断式
                if '-' in A[2][0] and not '-' in A[2][1]:
                    angleOneLoc = 4
                    #一个y>x一个x>y,在两条交叉线段的时候是右下角
                elif '-' in A[2][0] and '-' in A[2][1]:
                    angleOneLoc = 3
                    #两个y>x,在两条交叉线的是左下角
                elif not '-' in A[2][0] and '-' in A[2][1]:
                    angleOneLoc = 2
                    #一个x>y一个x<y,在两条交叉线的是左上角
                else:
                    angleOneLoc = 1
                    #两个x>，在两条交叉线的右上角
                if '-' in B[2][0] and not '-' in B[2][1]:
                    angleTwoLoc = 4
                    #一个y>x一个x>y,在两条交叉线段的时候是右下角
                elif '-' in B[2][0] and '-' in B[2][1]:
                    angleTwoLoc = 3
                    #两个y>x,在两条交叉线的是左下角
                elif not '-' in B[2][0] and '-' in B[2][1]:
                    angleTwoLoc = 2
                    #一个x>y一个x<y,在两条交叉线的是左上角
                else:
                    angleTwoLoc = 1
                    #两个x>，在两条交叉线的右上角

                return theorms().sameside(angleOneLoc,angleTwoLoc,'interior')


    def sameside_exterior(self, A, B):
        '''
        输入的格式

        :param A（角1）: [点1/线1，transversal/线2，[上减下加--交错点1，上减下加--交错点2]]
        :param B（角2）: [点1/线1，transversal/线2，[上减下加--交错点1，上减下加--交错点2]]
        :return: 是否可以使用sameside interior theorm
        '''
        # 如果是一条线的名称
        if 97 <= A[0] <= 122:
            # 如果两个共同线段
            if A[0] == B[0] and A[1] == B[1]:
                return False
            elif A[0] == B[0] or A[1] == B[1]:
                '''
                下一步就是判断是否两个临近transversal的角是否是在同一条边上
                如果不是的话就只能使用alternate exterior/interior Theorms
                '''
                # 象限判断式
                if '-' in A[2][0] and not '-' in A[2][1]:
                    angleOneLoc = 4
                    # 一个y>x一个x>y,在两条交叉线段的时候是右下角
                elif '-' in A[2][0] and '-' in A[2][1]:
                    angleOneLoc = 3
                    # 两个y>x,在两条交叉线的是左下角
                elif not '-' in A[2][0] and '-' in A[2][1]:
                    angleOneLoc = 2
                    # 一个x>y一个x<y,在两条交叉线的是左上角
                else:
                    angleOneLoc = 1
                    # 两个x>，在两条交叉线的右上角
                if '-' in B[2][0] and not '-' in B[2][1]:
                    angleTwoLoc = 4
                    # 一个y>x一个x>y,在两条交叉线段的时候是右下角
                elif '-' in B[2][0] and '-' in B[2][1]:
                    angleTwoLoc = 3
                    # 两个y>x,在两条交叉线的是左下角
                elif not '-' in B[2][0] and '-' in B[2][1]:
                    angleTwoLoc = 2
                    # 一个x>y一个x<y,在两条交叉线的是左上角
                else:
                    angleTwoLoc = 1
                    # 两个x>，在两条交叉线的右上角

                return theorms().sameside(angleOneLoc, angleTwoLoc, 'exterior')
                

    def vertical_angles(self,A,B):
        '''
        输入的格式

        :param A（角1）: [点1/线1，transversal/线2，[上减下加--交错点1，上减下加--交错点2]]
        :param B（角2）: [点1/线1，transversal/线2，[上减下加--交错点1，上减下加--交错点2]]
        :return: 是否可以使用sameside interior theorm
        '''
        # 如果是一条线的名称
        if 97 <= A[0] <= 122:
            # 如果两个共同线段
            if A[0] == B[0] and A[1] == B[1]:
                #vertical angles 必须要在两条共同边上的对角才可以用


            elif A[0] == B[0] or A[1] == B[1]:
                return False
            else:
                return False
#Get all the possible calculations for the postulates
class postulates:
    '''
    因为计算机编程来推测数学模型是使用逆向思维的过程，所以不能
    直接使用postulate来给theorems做结论，然而需要使用theorems
    开证明postulates正确
    '''
    def __init__(self):
        self.points = []


    class converse:
        def __init__(self):
            pass


        def corresponding(self):
            pass

    def corresponding(self,A,B):
        '''
        同位角的证明方法：
        Definitions: Supplementary Angles
        Theorms:
            #如果角1是在a//b和t之外
            Vertical Angles > Alternate Interior
            Vertical Angles > Sameside Interior > Def of Supplementary Angles
            Def of Supplementary Angles > Sameside Interior
            Vertical Angles > Samedside Interior > Def of Supplementary Angles > Vertical Angles


            #如果角1是在a//b和t之内
            Vertical Angles > Alternate Exterior
            Vertical Angles > Sameside Exterior > Def of Supplementary Angles
            Def of Supplementary Angles > Sameside Exterior
            Vertical Angles > Samedside Exterior > Def of Supplementary Angles > Vertical Angles
        '''
        #现在就可以开始调用前面的Theorems了






#Init the running bool
running = True


#Start the program

while True:
    #Get the event keys
    for event in pygame.event.get():
        #Mouse clicks


        #if quitting application
        if event == pygame.QUIT or running == False:
            exit(1)


    #Main Program

