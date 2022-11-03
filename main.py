#using pygame as main canvas
#import pygame

#using random to generate random points and transversals
import random

#init pygame
#pygame.init()

#create a window(could be full screen)
#screen = pygame.display.set_mode(pygame.display.FULLSCREEN)


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
                grid.append([['t'+str(self.transversalcnt),'t'+str(self.transversalcnt)],((grid[i][1][0]+slope[0],pointLocation+slope[1]),(grid[i][1][0]-slope[0],pointLocation-slope[1])), pointLocation])
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
            #返回slope, slope的两个点, 原点
            return (slope,point,grid[mark][3])


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
            

    def vertical(self,angleOneLoc,angleTwoLoc):
        '''
        Vertical angles就只是两个对角，有因为有两个相同边可以
        直接建造出一个"Quadurant"虽然不是很规范但是基本上就长
        这个样子
        '''

        '''
        但是因为vertical angles是based on two transversals
        所以两个象限的标记数字不一样
        图1：（t1)
        2 1
        3 4
        
        图2：(t2)
        1 4
        2 3
        '''
        if angleOneLoc == 2 and angleTwoLoc == 3:
            return True
        elif angleOneLoc == 3 and angleTwoLoc == 4:
            return True
        elif angleOneLoc == 1 and angleTwoLoc == 2:
            return True
        elif angleOneLoc == 4 and angleTwoLoc == 1:
            return True
        else:
            return False

    def angle_loc(self, A):
        '''

        :param A（角1）: [点1/线1，transversal/线2，[inequality sign1, inequality sign2]]
        :return:
        '''
        slope,points,b = line().get_line_parameters(A[0])
        slope2,points2,b2 = line().get_line_parameters(A[1])

        '''
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
        '''
        #因为y = mx+b
        #所以m2x-m1x = b1-b2
        #b1-b2 = change of y from origin
        #m2x-m1x = x(m2-m1)
        #x(m2-m1) = b1-b2, 那么x = b1-b2/(m2-m1)
        #然后再把这个公式还原出来获取y
        #y = mx+b (默认选择第一个公式因为交错点的位置必须一样)
        ychange = b2-b
        slopechange = slope2-slope
        x = ychange / slopechange
        y = slope*x+b

        #接下来要判断inequality的象限位置
        if A[1][0] == '>':
            if A[1][1] == '>':
                angleOneLoc = 1
            elif A[1][1] == '<':
                angleOneLoc = 4
        if A[1][0] == '<':
            if A[1][1] == '>':
                angleOneLoc = 2
            elif A[1][1] == '<':
                angleOneLoc = 3


        return angleOneLoc


    def alternate_interior(self,A,B):
        '''
        输入的格式

        :param A（角1）: [点1/线1，transversal/线2，[formula1, inequality sign1, formula2, inequality sign2]]
        :param B（角2）: [点1/线1，transversal/线2，[formula1, inequality sign1, formula2, inequality sign2]]
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
                angleOneLoc = theorms().angle_loc(A)
                '''
                这不就是Quadrants嘛
                '''


                angleTwoLoc = theorms().angle_loc(B)


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

        :param A（角1）: [点1/线1，transversal/线2，[formula1, inequality sign1, formula2, inequality sign2]]
        :param B（角2）: [点1/线1，transversal/线2，[formula1, inequality sign1, formula2, inequality sign2]]
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
                angleOneLoc = theorms().angle_loc(A)
                #现在也给角2算一下位置
                '''
                很好，这里的注释也是复制黏贴的
                '''
                angleTwoLoc = theorms().angle_loc(B)

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

        :param A（角1）: [点1/线1，transversal/线2，[formula1, inequality sign1, formula2, inequality sign2]]
        :param B（角2）: [点1/线1，transversal/线2，[formula1, inequality sign1, formula2, inequality sign2]]
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
                angleOneLoc = theorms().angle_loc(A)
                angleTwoLoc = theorms().angle_loc(B)

                return theorms().sameside(angleOneLoc,angleTwoLoc,'interior')


    def sameside_exterior(self, A, B):
        '''
        输入的格式

        :param A（角1）: [点1/线1，transversal/线2，[formula1, inequality sign1, formula2, inequality sign2]]
        :param B（角2）: [点1/线1，transversal/线2，[formula1, inequality sign1, formula2, inequality sign2]]
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
                angleOneLoc = theorms().angle_loc(A)
                angleTwoLoc = theorms().angle_loc(B)

                return theorms().sameside(angleOneLoc, angleTwoLoc, 'exterior')
                



    def vertical_angles(self,A,B):
        '''
        输入的格式

        :param A（角1）: [点1/线1，transversal/线2，[inequality sign1, inequality sign2]]
        :param B（角2）: [点1/线1，transversal/线2，[inequality sign1, inequality sign2]]
        :return: 是否可以使用sameside interior theorm
        '''
        # 如果是一条线的名称
        if 97 <= A[0] <= 122:
            # 如果两个共同线段
            if A[0] == B[0] and A[1] == B[1]:
                #vertical angles 必须要在两条共同边上的对角才可以用
                # 象限判断式
                angleOneLoc = theorms().angle_loc(A)

                angleTwoLoc = theorms().angle_loc(B)

                return theorms.vertical(angleOneLoc,angleTwoLoc)

            elif A[0] == B[0] or A[1] == B[1]:
                #那么就强行输出一个vertical angle
                #因为vertical angles必须在两条相同的线段上
                #所以A[0]=B[0], A[1] = B[1]，默认输出A的对角
                sign = ['>','<']
                #如果A[2][0]='<'，那么就存取sign[1]，否则存入sign[0]。因为true=1,false=0
                return [A[0]+A[1]+[int(sign[A[2][0]=='<']),sign[int(A[2][1]=='<')]]]
            else:
                return False

    def quick_action(self,target,A,B):
        if target == 'Vertical Angles':
            return theorms().vertical_angles(A,B)
        elif target == 'Sameside Interior':
            return theorms().sameside_interior(A,B)
        elif target == 'Sameside Exterior':
            return theorms().sameside_exterior(A,B)
        elif target == 'Alternate Interior':
            return theorms().alternate_interior(A,B)
        elif target == 'Alternate Exterior':
            return theorms().alternate_exterior(A,B)


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

    def calculate(self,nextup,A,B):
        #所有可以使用的步骤
        for i in range(len(nextup)):
            #执行这个步骤
            RAM = theorms().quick_action(list(nextup.keys())[0],A,B)
            #如果执行的结果==（预测的结果），那么就说明这个步骤是对的
            if RAM == B:
                #如果调用下一项内容得到的不是list也不是dictionary,那么就已经运行完成所有步骤了
                if type(nextup[i+1]) == str:
                    #这个证明是对的
                    return True
                else:
                    #如果后面应该还要有步骤，但是已经得到了正确答案，那么就说明使用的方法错误了
                    #输出正确的方法名称
                    return nextup[i]
            #返回一下每一个步骤的内容（如果已经=B那么就不会执行）
            return postulates().calculate(nextup[list(nextup.keys())[0]],RAM,B)
        #如果没有一步能够让RAM=B那么这个方法就是错误的
        return False

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
            Vertical Angles > Sameside Exterior > Def of Supplementary Angles > Vertical Angles
        '''
        #现在就可以开始调用前面的Theorems了
        theorems = theorms()

        #RAM = theorems.vertical_angles(A,B)
        '''
        if RAM:
            #如果可以使用vertical angles
            if RAM = True:
                #如果直接成立就不是corresponding angles postulate
                return 'Definition of Vertical Angles'
            else:
                #那么就是输出了一个Vertical angle角
                if theorems.alternate_interior(RAM,B):
                    #如果返回一个true那么就corresponding angles postulate成立
                    return True
                else:
                    RAM = theorems.sameside_interior(RAM,B)
                    if ... 这样写下去会没完没了而且如果某个人想要炫耀Geometry技巧估计会报错
                
        '''
        #不如直接给个while循环
        nextup = [{'Def of Supplementary Angles':'Sameside Interior'},{'Vertical Angles':
                  ['Alternate Interior',{'Sameside Interior':
                                         ['Def of Supplementary Angles',{'Def of Supplementary Angles':
                                                                         'Vertical Angles'}]}]}]
        
        RAM2 = postulates().calculate(nextup, A=A, B=B)

        return RAM2






'''
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

'''
