#using pygame as main canvas
#import pygame

#using random to generate random points and transversals
import random
import sys
#sys.setrecursionlimit(10**8)

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
        self.linecnt = 97

    def line(self,A=(0,0),B=(0,0)):
        global grid
        #输入统一的line格式
        grid.append([chr(self.linecnt),[chr(self.points),chr(self.points+1)],(A,B),(A[1]+B[1])/2])
        #ASCII码表+2这样可以让每一个点都不一样（不至于一道题用26个点吧）
        self.points += 2
        self.linecnt += 1
        return True

    '''
    def segments(self,A=(0,0),B=(0,0)):
        #因为segments的定义在象限中和line一摸一样所以就直接调用line的操作
        line(A,B)
        return True
    '''

    def transversal(self,targetLine=['A','B']):
        #标记是否有可以做transversal的线或者线段
        flag = False
        #查找过程
        #print(targetLine,grid[0])
        for i in range(len(grid)):
            if targetLine in grid[i]:
                #备注不要执行报错过程
                flag = True
                #随便选择一个点范围必须在segment定义域内
                pointLocation = random.randint(grid[i][2][0][1],grid[i][2][1][1])
                #一个没有长度的line就是一个点
                #grid.append([[chr(self.points),chr(self.points)],(pointLocation,pointLocation)])
                #生成一个随机的slope（也就是角度）
                slope = (random.randint(0,360),random.randint(0,360))
                #print(type(slope[0]),type(grid[i][2][0][0]),grid[i][2][0][0])
                grid.append(['t'+str(self.transversalcnt),['t'+str(self.transversalcnt),'t'+str(self.transversalcnt)],((grid[i][2][0][0]+slope[0],pointLocation+slope[1]),(grid[i][2][1][0]-slope[0],pointLocation-slope[1])), pointLocation])
                '''
                有点乱：这个是数据结构
                
                [[定义的点1，定义的点2]，（点一和点二的集合：（点一x轴+slope的run，点一y轴+slope的rise），（点二的x轴-slope的run，点二y轴-slope的rise））]
                '''

        #如果没有这个线段
        if flag == False:
            #报个错得了这个输入肯定有问题
            return EOFError


#init class line
LINE = line()

#Get line parameters
def get_line_parameters(lineName='A'):
    # 直接在数据库中找一下就ok了
    mark = -1
    # 判断一下这个line是两个点还是一条线的总称
    if type(lineName) == str:
        # 枚举grid反正不会超时不然做题的人会直接狂暴
        for i in range(len(grid)):
            #print(grid[i], '\ngrid[i]\n')
            if [lineName, lineName] in grid[i] or lineName in grid[i]:
                mark = i
                break
    else:
        # 如果是两个点
        for i in range(len(grid)):
            if lineName in grid[i]:
                mark = i
                break
    #print(lineName,'linename')
    #print(mark)
    # 如果没有记录
    if mark == -1:
        # 不存在这条线
        #print('none')
        return False
    else:
        # 计算斜率
        slope = (grid[mark][2][0][1]-grid[mark][2][1][1])/(grid[mark][2][0][0]-grid[mark][2][1][0])
        
        # 买一送一，给两个point得了（省的以后在多做模块）
        point = [grid[mark][2][0], grid[mark][2][1]]
        #print(slope,point)

        '''
        也是一个很烦人的数据点
        return格式：(slope的小数点，(p1x,p1y)，(p2x,p2y))
        '''
        # 返回slope, slope的两个点, 原点
        return [slope, point, grid[mark][3]]


def angle_loc(A):
    '''
    :param A（角1）: [点1/线1，transversal/线2，[inequality sign1, inequality sign2]]
    :return:
    '''
    '''
    print(get_line_parameters(A[0]))
    print(get_line_parameters(A[1]))
    print(data1)
    print(data1[1])
    print(data1[2])
    '''
    slope1, point1, b1 = get_line_parameters(A[0])
    slope2, point2, b2 = get_line_parameters(A[1])
    # print(slope1,point1,b1)

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
    # 因为y = mx+b
    # 所以m2x-m1x = b1-b2
    # b1-b2 = change of y from origin
    # m2x-m1x = x(m2-m1)
    # x(m2-m1) = b1-b2, 那么x = b1-b2/(m2-m1)
    # 然后再把这个公式还原出来获取y
    # y = mx+b (默认选择第一个公式因为交错点的位置必须一样)
    ychange = b2 - b1
    slopechange = slope2 - slope1
    x = ychange / slopechange
    y = slope1 * x + b1

    # 接下来要判断inequality的象限位置
    angleOneLoc = 0

    if A[2][0] == '>':
        if A[2][1] == '>':
            angleOneLoc = 2
        elif A[2][1] == '<':
            angleOneLoc = 1
    if A[2][0] == '<':
        if A[2][1] == '<':
            angleOneLoc = 4
        elif A[2][1] == '>':
            angleOneLoc = 3

    return angleOneLoc


class definition:
    def __init__(self):
        pass

    def supplementary_angles(self,A,B):
        angleOneLoc = angle_loc(A)
        angleTwoLoc = angle_loc(B)
        if abs(angleOneLoc-angleTwoLoc==1):
            return True
        else:
            return False


#Get all the possible calculations for the theorms
class theorms:
    def __init__(self):
        pass

    def parallel(self,A,B):
        slope1 = (A[2][1][0] - A[2][0][0]) / (A[2][1][1] - A[2][0][1])
        slope2 = (B[2][1][0] - B[2][0][0]) / (B[2][1][1] - B[2][0][1])

        return (slope1 == slope2)

    def sameside(self,angleOneLoc,angleTwoLoc,mode="Interior"):
        '''
        直接生成一个模块来判断Alternate是否成立得了
        '''
        #print(angleOneLoc, angleTwoLoc)
        if mode == "Interior" and angleOneLoc in [3,4] and angleTwoLoc in [1,2]:
            if angleOneLoc == 3 and angleTwoLoc == 2:
                return True
            elif angleOneLoc == 4 and angleTwoLoc == 1:
                return True
            else:
                #print(angleOneLoc in [3,4], angleTwoLoc in [1,2])
                if angleOneLoc == 3:
                    return [False, 2]
                elif angleOneLoc == 4:
                    return [False, 1]
                return False

        elif mode == "Exterior" and angleOneLoc in [1,2] and angleTwoLoc in [3,4]:
            if angleOneLoc == 2 and angleTwoLoc == 3 or angleOneLoc == 1 and angleTwoLoc == 4:
                return True
            else:
                #print(angleOneLoc in [1,2], angleTwoLoc in [3,4])
                if angleOneLoc == 1:
                    return [False, 4]
                elif angleOneLoc == 2:
                    return [False, 3]
                return False
        
                
    def alternate(self,angleOneLoc,angleTwoLoc,mode="Interior"):
        '''
        直接生成一个模块来判断Sameside是否成立得了
        '''
        #print(angleOneLoc, angleTwoLoc,mode)
        #print(angleOneLoc,angleTwoLoc)
        if mode == "Interior":
            if angleOneLoc == 3 and angleTwoLoc == 2:
                return True
            elif angleOneLoc == 4 and angleTwoLoc == 1:
                return True
            else:
                if angleOneLoc == 3:
                    return (False, 2)
                elif angleOneLoc == 4:
                    return (False, 1)
                return False
        elif mode == "Exterior":
            if angleOneLoc == 1 and angleTwoLoc == 3 or angleOneLoc == 2 and angleTwoLoc == 4:
                #print('TTT')
                return True
            else:
                #print(angleOneLoc)
                if angleOneLoc == 1:
                    return (False, 3)
                elif angleOneLoc == 2:
                    return (False, 4)
                return False
            

    def vertical(self,angleOneLoc,angleTwoLoc):
        '''
        Vertical angles就只是两个对角，有因为有两个相同边可以
        直接建造出一个"Quadurant"虽然不是很规范但是基本上就长
        这个样子
        '''
        #print(angleOneLoc,angleTwoLoc)
        if angleOneLoc in [2,4] and angleTwoLoc in [2,4] and angleTwoLoc != angleOneLoc:
            return True
        elif angleOneLoc in [1,3] and angleTwoLoc in [1,3] and angleTwoLoc != angleOneLoc:
            return True
        else:
            return False

    def angle_loc(self, A):
        '''

        :param A（角1）: [点1/线1，transversal/线2，[inequality sign1, inequality sign2]]
        :return:
        '''
        
        '''
        print(get_line_parameters(A[0]))
        print(get_line_parameters(A[1]))
        print(data1)
        print(data1[1])
        print(data1[2])
        '''
        slope1,point1,b1 = get_line_parameters(A[0])
        slope2,point2,b2 = get_line_parameters(A[1])
        #print(slope1,point1,b1)

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
        ychange = b2-b1
        slopechange = slope2-slope1
        x = ychange / slopechange
        y = slope1*x+b1

        #接下来要判断inequality的象限位置
        angleOneLoc = 0
        
        if A[2][0] == '>':
            if A[2][1] == '>':
                angleOneLoc = 2
            elif A[2][1] == '<':
                angleOneLoc = 1
        if A[2][0] == '<':
            if A[2][1] == '<':
                angleOneLoc = 4
            elif A[2][1] == '>':
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
        if 97 <= ord(A[0]) <= 122:
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
                angleOneLoc = theorms().angle_loc(A)
                angleTwoLoc = theorms().angle_loc(B)

                #判断是否是Alt Int
                possible = theorms.alternate(angleOneLoc,angleTwoLoc,"Interior")
                sign = [['>', '<'], ['>', '>'], ['<', '<'], ['<', '>']]
                if possible == True:
                    return [True]
                elif possible == None:
                    print('There are no possible Alt Int Angles')
                    return [False, None]
                else:
                    print('Possible Alt Int Angle:',(possible[0], list(B[0]) + list(B[1]) + list(sign[possible[1] - 1])))
                    return (possible[0], list(B[0]) + list(B[1]) + list(sign[possible[1] - 1]))

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
        if 97 <= ord(A[0]) <= 122:
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
                #获取这两个角的位置（坐标轴的第几区）
                angleOneLoc = theorms().angle_loc(A)
                angleTwoLoc = theorms().angle_loc(B)

                #判断是否是Alt Ext
                possible = theorms().alternate(angleOneLoc,angleTwoLoc,"Exterior")
                #print(possible)
                sign = [['>','<'],['>','>'],['<','<'],['<','>']]
                if possible == True:
                    return [True]
                elif possible == None:
                    print('There are no possible Alt Ext Angles')
                    return [False, None]
                else:
                    print(
                        'Possible Alt Ext Angle:',(possible[0], list(B[0]) + list(B[1]) + list(sign[possible[1] - 1])))
                    return (possible[0],list(B[0])+list(B[1])+list(sign[possible[1]-1]))

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
        if 97 <= ord(A[0]) <= 122:
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
                #print(angleOneLoc, angleTwoLoc,'aaaaaaaaa')
                possible = theorms().sameside(angleOneLoc,angleTwoLoc,'Interior')
                sign = [['>', '<'], ['>', '>'], ['<', '<'], ['<', '>']]
                if possible == True:
                    return [True]
                elif possible == None:
                    print('There are no possible Sameside Int Angles')
                    return [False, None]
                else:
                    #print('Possible Sameside Int Angle:',(possible[0], list(B[0]) + list(B[1]) + list(sign[possible[1] - 1])))
                    print(A,B,possible,'posssssssssssssssssssssssiiiiiiiiiibbbbbbbbblllllllllleeeeeeeee')
                    #return (possible[0], list(B[0]) + list(B[1]) + list(sign[possible[1] - 1]))


    def sameside_exterior(self, A, B):
        '''
        输入的格式

        :param A（角1）: [点1/线1，transversal/线2，[formula1, inequality sign1, formula2, inequality sign2]]
        :param B（角2）: [点1/线1，transversal/线2，[formula1, inequality sign1, formula2, inequality sign2]]
        :return: 是否可以使用sameside interior theorm
        '''
        # 如果是一条线的名称
        if 97 <= ord(A[0]) <= 122:
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

                possible = theorms().sameside(angleOneLoc, angleTwoLoc, 'Exterior')
                sign = [['>', '<'], ['>', '>'], ['<', '<'], ['<', '>']]
                if possible == True:
                    return [True]
                elif possible == None:
                    print('There are no possible Sameside Ext Angles')
                    return [False, None]
                else:
                    print(
                        'Possible Sameside Ext Angle:',(possible[0], list(B[0]) + list(B[1]) + list(sign[possible[1] - 1])))
                    return (possible[0], list(B[0]) + list(B[1]) + list(sign[possible[1] - 1]))
                



    def vertical_angles(self,A,B):
        '''
        输入的格式

        :param A（角1）: [点1/线1，transversal/线2，[inequality sign1, inequality sign2]]
        :param B（角2）: [点1/线1，transversal/线2，[inequality sign1, inequality sign2]]
        :return: 是否可以使用sameside interior theorm
        '''
        #print(A[0],B[0],A[1],B[1])
        # 如果是一条线的名称
        if 97 <= ord(A[0]) <= 122:
            
            # 如果两个共同线段
            if A[0] == B[0] and A[1] == B[1]:
                #vertical angles 必须要在两条共同边上的对角才可以用
                # 象限判断式
                angleOneLoc = theorms().angle_loc(A)

                angleTwoLoc = theorms().angle_loc(B)
                print(angleOneLoc, angleTwoLoc)
                return theorms().vertical(angleOneLoc,angleTwoLoc)

            elif A[0] == B[0] or A[1] == B[1]:
                #那么就强行输出一个vertical angle
                #因为vertical angles必须在两条相同的线段上
                #所以A[0]=B[0], A[1] = B[1]，默认输出A的对角
                sign = ['>','<']
                #如果A[2][0]='<'，那么就存取sign[1]，否则存入sign[0]。因为true=1,false=0
                possible = [B[0], B[1], sign[B[2][0] == '>'], sign[int(B[2][1] == '>')]]
                print('possible vertical angle: '+ str(possible))
                return (False, possible)
            else:
                return False

    def triparallel(self,A,B,C):
        '''
        输入格式
        :param A: ['linename', ['pt1', 'pt2'], ((pt1x, pt1y), (pt2x, pt2y)), y-intercept]
        :param B: ['linename', ['pt1', 'pt2'], ((pt1x, pt1y), (pt2x, pt2y)), y-intercept]
        :param C: ['linename', ['pt1', 'pt2'], ((pt1x, pt1y), (pt2x, pt2y)), y-intercept]
        :return: True/False
        '''

        slope1 = (A[2][1][0] - A[2][0][0]) / (A[2][1][1] - A[2][0][1])
        slope2 = (B[2][1][0] - B[2][0][0]) / (B[2][1][1] - B[2][0][1])
        slope3 = (C[2][1][0] - C[2][0][0]) / (C[2][1][1] - C[2][0][1])

        return (slope1==slope2==slope3)



    def perpendicular(self,A,B):
        slope1 = (A[2][1][0] - A[2][0][0]) / (A[2][1][1] - A[2][0][1])
        slope2 = (B[2][1][0] - B[2][0][0]) / (B[2][1][1] - B[2][0][1])
        if slope1 == -(1 / slope2):
            return True

    def duoperpendicular(self,A,B,C):
        slope1 = (A[2][1][0] - A[2][0][0]) / (A[2][1][1] - A[2][0][1])
        slope2 = (B[2][1][0] - B[2][0][0]) / (B[2][1][1] - B[2][0][1])
        slope3 = (C[2][1][0] - C[2][0][0]) / (C[2][1][1] - C[2][0][1])
        if slope1 == slope2:
            if slope3 == -(1/slope1):
                return True

        if slope2==slope3:
            if slope1 == -(1/slope2):
                return True

        if slope3==slope1:
            if slope2 == -(1/slope1):
                return True

        return False





def quick_action(target,A,B):
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
    elif target == 'Def of Supplementary Angles':
        return definition().supplementary_angles(A,B)
        











a = {1:[{2:3},4,5]}
total = 0
steps = []





#Get all the possible calculations for the postulates
class postulates:
    '''
    因为计算机编程来推测数学模型是使用逆向思维的过程，所以不能
    直接使用postulate来给theorems做结论，然而需要使用theorems
    开证明postulates正确
    '''

    class converse:
        def __init__(self):
            pass


        def corresponding(self):
            pass



    def __init__(self):
        self.points = []
        
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
        #不如直接给个while循环
        nextup = [['Def of Supplementary Angles','Sameside Interior'],['Vertical Angles',
                  ['Alternate Interior',['Sameside Interior',
                                         ['Def of Supplementary Angles',['Def of Supplementary Angles',
                                                                         'Vertical Angles']]]]]]
        '''
        至于写的那么乱...
        同位角=同个quadrant...
        额...ok...
        '''

        angleOneLoc = theorems.angle_loc(A)
        angleTwoLoc = theorems.angle_loc(B)
        sign = [['>', '<'], ['>', '>'], ['<', '<'], ['<', '>']]

        return [(angleOneLoc == angleTwoLoc),(angleOneLoc!=angleTwoLoc)*sign[angleOneLoc-1]]


    class triangles:
        def __init__(self):
            pass






line = line()
theorems = theorms()
line.line((0,0),(10,0))
line.line((0,10),(10,10))
line.line((-5,-5),(5,5))
line.transversal(['A','B'])
A = ['a','t1',['>','>']]
B = ['b','t1',['<','<']]
C = ['c','b',['<','<']]
torf = ['not ','']
print('they are '+torf[int(bool(theorems.alternate_exterior(A,B)[0]))]+'alternate exterior angles')
print('they are '+torf[int(bool(theorems.alternate_interior(A,B)[0]))]+'alternate interior angles')
print('they are '+torf[int(bool(theorems.sameside_exterior(A,B)[0]))]+'sameside exterior angles')
print('they are '+torf[int(bool(theorems.sameside_interior(A,B)[0]))]+'sameside interior angles')
print('they are '+torf[int(bool(theorems.vertical_angles(A,B)[0] and theorems.vertical_angles(A,B)[1]))]+'vertical angles')

postulates = postulates()
print('they are '+torf[int(bool(postulates.corresponding(A,B)[0]))]+'corresponding angles')