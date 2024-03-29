# -*- coding: utf-8 -*-
from ImageProcessor import ImageProcessor
import time
from Robo import Robo
from Head import Head
from Motion import Motion
import Distance


class Act:
    TEESHOT = 1          # 1. 맨 처음 티샷  
    WALK_BALL = 2        # 2. 공까지 걸어가기 (걸음수)
    PUTTING_POS = 3      # 3. 퍼팅 위치에 서기
    PUTTING = 4          # 4. 퍼팅
    HOLEIN = 5           # 5. 홀인

class Controller:

    def __init__(self):
        #act = Act.TEESHOT
        pass
    
    act  = Act.PUTTING_POS
    robo = Robo()


    @classmethod  
    def start(self):

        act = self.act
        robo = self.robo
        is_object_in_frame = False
        
        head = Head()
        
        
           
                  
        
        go_to = "small"
        
        #=======================================================#
        #                        Head def                       #         
        #=======================================================#
        def big_UD(object="ball"):
            big_ud_angle = 100
            # big UD head
            while True:
                is_object_in_frame, Distance.Head_ud_angle = head.big_UD_head(object, big_ud_angle)
                if is_object_in_frame == True:
                    return "Success"
                elif is_object_in_frame == False:
                    big_ud_angle = Distance.Head_ud_angle
                
                    if Distance.Head_ud_angle == 55: # Distance.Head_UD_Middle_Value_Measures - 100 + 10 + 45:  # big ud 한 사이클이 끝남. / 9는 바뀔 수 있는 값
                        Distance.Head_ud_angle = Distance.Head_UD_Middle_Value_Measures # 고개값을 다시 정면100으로 
                        #go_to = "big_lr"  # LR로 갈지 구분
                        return "Except"
                    else: 
                        continue
                        
                        
        def big_LR(object="ball"):
            big_lr_angle = 100
            max_right_flag = 0
            print("THis is ", object)
            # big LR head
            while True:
                is_object_in_frame, big_lr_temp, max_right_flag = head.big_LR_head(object, big_lr_angle, max_right_flag)
                if is_object_in_frame == True:
                    break
                elif is_object_in_frame == False:
                    big_lr_angle = big_lr_temp
                    print("big_lr_angle : ", big_lr_angle)
                    continue
                #if big_lr_angle == -90: #왼쪽 max까지 갔는데 공 못찾으면 
                    #head.big_UD_head()
                    # 예외처리 : big up down 코드
            #고개 정면 코드 추가하기

        def small_LR(object="ball"):
            Distance.small_lr_angle = 100
            while True:
                print("---------start small lr head")
                is_vertical_middle, small_lr_temp = head.small_LR_head(object, Distance.small_lr_angle)
                if is_vertical_middle == True:
                    return "Success" #break
    
                elif is_vertical_middle == False:
                    Distance.small_lr_angle = small_lr_temp
                    continue
                else : # is_vertical_middle == Except_
                    return "Except"


        def small_UD(object="ball"):
            small_ud_angle = Distance.Head_UD_Middle_Value_Measures
            #small ud head
            while True:
                is_horizontal_middle, Distance.Head_ud_angle = head.small_UD_head(object, small_ud_angle)
                if is_horizontal_middle == True: #최종 중앙 맞춰짐 
                    #act = Act.PUTTING_POS 
                    return "Success"
                elif is_horizontal_middle == False:
                    small_ud_angle = Distance.Head_ud_angle
                    continue  
                else: # is_horizontal_middle == Except_
                    return "Except"
                         

        def UD_for_dist(object="ball"): # small ud head 변형
            small_ud_angle = Distance.Head_UD_Middle_Value_Measures
            # 거리를 위한 고개 각도 내리기 
            while True:
                print("---------start ud for dist")
                is_horizontal_middle, small_ud_temp = head.head_for_dist(object, small_ud_angle)
                if is_horizontal_middle == True: #최종 중앙 맞춰짐 
                    #act = Act.PUTTING_POS 
                    #variable.Head_ud_angle = 
                    Distance.Head_ud_angle = small_ud_temp
                    print(Distance.Head_ud_angle)
                    break
                elif is_horizontal_middle == False:
                    small_ud_angle = small_ud_temp
                    Distance.Head_ud_angle = small_ud_temp
                    continue

        def holecup_UD_for_dist(): # small ud head 변형
            small_ud_angle = 10
            
            #현재 고개 55도에서 10도로
            # robo._motion.head("DOWN", 30) # 고개 10도로 내리고 공 detect 시작 !
            # robo._motion.head("DOWN", 9) 
            # robo._motion.head("DOWN", 6) 
            
            # 거리를 위한 고개 각도 올리기 
            while True:
                print("---------start HOlECUP ud for dist")
                is_horizontal_middle, small_ud_temp = head.head_for_dist("holecup", small_ud_angle)
                if is_horizontal_middle == True: #최종 중앙 맞춰짐 
                    #act = Act.PUTTING_POS 
                    #variable.Head_ud_angle = 
                    Distance.Head_ud_angle = small_ud_temp
                    print("holecup ud angle : ",Distance.Head_ud_angle)
                    break
                elif is_horizontal_middle == False:
                    small_ud_angle = small_ud_temp
                    Distance.Head_ud_angle = small_ud_temp
                    continue
            

       #=======================================================#
        #                      1. Teeshot                       #         
        #=======================================================#
        
        if act == Act.TEESHOT:                 ##### 1. 시작 및 티샷 #################
            print("ACT: ", act) # Debug
            
            ######## act == Act.WALK_BALL에 Big UD 추가 ########


            ### big UD & LR 할까말까 결정 T / F
            is_ball = robo._image_processor.detect_ball()

            ### False면, big UD LR 해라
            if is_ball == False:                
                while True:
                    # big UD head
                    is_big_UD = big_UD("ball")

                    #if go_to == "big_lr" :
                    if is_big_UD == "Except" :  # big UD 검출안됨 -> big LR 로 넘어감
                        big_LR("ball")  # big은 알아서 고개 디폴트 함 
                    
                    is_small_LR = small_LR("ball")
                    
                    if is_small_LR == "Except" :
                        robo._motion.head("DEFAULT", 2) # small_LR 한 후 고개 디폴트
                        # big 알고리즘으로 넘어감
                        # is_big_LR = big_LR("ball") 하러 처음으로 올라감 
                        big_LR("ball") # 이거 한번만 실행하면 무조건 찾을 거라고 생각해서 while로 안 돌아감.
                    else:
                        break
                    
            else:
                small_LR("ball") # small lr 함으로써 중앙 맞춰짐

            # ud_for_dist 하기전에 고개 세팅
            robo._motion.head("DEFAULT", 2) # 고개 디폴트
            Distance.Head_ud_angle = Distance.Head_UD_Middle_Value_Measures
            robo._motion.head("DEFAULT", 1) # 고개 디폴트
            
            UD_for_dist("ball")
            robo._motion.head("DEFAULT", 1) # ud for dist 이후 고개 상하 디폴트
            time.sleep(2)
            

            # length = 거리 
            ball_dist = Distance.Length_ServoAngle_dict.get(Distance.Head_ud_angle)
            print(Distance.Length_ServoAngle_dict)
            print("=====================================")
            print(ball_dist , "======HEE=====", Distance.Head_ud_angle)
            print("=====================================")

            
 
            # 거리 측정 후 걷기
            if ball_dist >= 18:
                # 걷는 횟수(loop) = (d - 15) / 한발자국 걷는 센치(5cm)
                if 18 <= ball_dist <= 20:
                    walk_loop = int((ball_dist - 18) // 3)
                    print(walk_loop)
                    robo._motion.walk("JFORWARD", walk_loop)
                else:
                    ball_dist = 110
                    walk_loop = int((ball_dist - 18) // 8)
                    print(walk_loop)
                    robo._motion.walk("FORWARD", walk_loop)


                # walk_loop = (ball_dist - 18) // 8 # 나중에 값 바꿔야됨.
                # walk_loop = int(walk_loop)
                # print("walk_loop", walk_loop)
                # robo._motion.walk("FORWARD", walk_loop, 2)
            else :      # 최소 거리 18보다 더 가까이 있을 경우: 뒷걸음질
                walk_loop = (18 - ball_dist) // 8
                walk_loop = int(walk_loop)  
                print(walk_loop)
                robo._motion.walk("BACKWARD", walk_loop)

            

            ######### 퍼팅 위치에 서고 ########
            ## 아직 옆에 설지, 정면으로 보고 설지 모름. 그래서 지금은 옆에 서는 걸로 했음
            ###### act == Act.PUTTING_POS
            ###### 원래라면 퍼팅 포즈로 가서 << 원프레임, 스트레이트, 거리 재기 >> 해야하는데
            ######------------------> 이거 지금 테스트 용으로 바로 퍼팅함
            ######### 퍼팅한다 ########
            time.sleep(3)
            robo._motion.putting("left", 3, 3)
            print("putting")
            time.sleep(3)

            # 아래 모션 좌퍼팅기준으로 썼네..
            # turn body left, 몸을 왼쪽으로 90도 돌림. / 고개는 이미 정면을 바라보고 있음.(바꿀 필요 없단 뜻)
            robo._motion.turn("LEFT", 60)
            time.sleep(3)
            robo._motion.turn("LEFT", 45)
            time.sleep(3)
            print("turn LEFT")

            self.act = Act.WALK_BALL
            
            #return True
        
        #=======================================================#
        #                        2. Walk                        #         
        #=======================================================#
        
        elif act == Act.WALK_BALL: 
        ##### 2. 공을 향해 걸어간다 #################

            print("^^^^222222")
            print("^^^^222222")
            print("^^^^222222")
            print("^^^^222222")
            # robo._motion.head("DEFAULT", 1)
            # robo._motion.head("DOWN", 45) # 고개 45도로 내리고 공 detect 시작 !
            # time.sleep(5)
            
            is_ball = robo._image_processor.detect_ball()

            ### False면, big UD LR 해라
            if is_ball == False:                
                while True:
                    # big UD head
                    is_big_UD = big_UD("ball")
                    print("controller === big ud ")

                    #if go_to == "big_lr" :
                    if is_big_UD == "Except" :  # big UD 검출안됨 -> big LR 로 넘어감
                        # big LR 시행하기전에 UD 45도로
                        robo._motion.head("DOWN", 45)
                        big_LR("ball")  # big은 알아서 고개 디폴트 함 
                    
                    is_small_LR = small_LR("ball")
                    
                    if is_small_LR == "Except" :
                        robo._motion.head("DEFAULT", 2) # small_LR 한 후 고개 디폴트
                        # big 알고리즘으로 넘어감
                        # is_big_LR = big_LR("ball") 하러 처음으로 올라감 
                        big_LR("ball") # 이거 한번만 실행하면 무조건 찾을 거라고 생각해서 while로 안 돌아감.
                    else:
                        break
            else:
                small_LR("ball") # small lr 함으로써 중앙 맞춰짐
            
            # ud_for_dist 하기전에 고개 세팅
            robo._motion.head("DEFAULT", 2) # 고개 디폴트
            Distance.Head_ud_angle = Distance.Head_UD_Middle_Value_Measures
            robo._motion.head("DEFAULT", 1) # 고개 디폴트
            time.sleep(1)
            
            print("ball detected")
            UD_for_dist("ball")
            robo._motion.head("DEFAULT", 1) # ud for dist 이후 고개 상하 디폴트
            time.sleep(2)

            # length = 거리 
            ball_dist = Distance.Length_ServoAngle_dict.get(Distance.Head_ud_angle)
            print("ball distance :", ball_dist)
            # 인자 값으로 서보모터 값 들어가야함 (원래 값 + 변한 값)
            #length = variable.Length_ServoAngle_dict.get(variable.Head_ud_angle +  small_ud_angle)
            
            

            # 거리 측정 후 걷기
            if ball_dist >= 18:
                if 18 <= ball_dist <=28:
                    walk_loop = int((ball_dist - 18) // 3)
                    print(walk_loop)
                    robo._motion.walk("JFORWARD", walk_loop)
                else:
                    walk_loop = int((ball_dist - 18) // 5)
                    print(walk_loop)
                    robo._motion.walk("FORWARD", walk_loop)
                # 걷는 횟수(loop) = (d - 15) / 한발자국 걷는 센치(5cm)
                # walk_loop = (ball_dist - 18) // 3 # 나중에 값 바꿔야됨.
                # walk_loop = int(walk_loop)
                # print("walk_loop", walk_loop)
                # robo._motion.walk("FORWARD", walk_loop, 2)
            else :      # 최소 거리 18보다 더 가까이 있을 경우: 뒷걸음질
                walk_loop = (18 - ball_dist) // 5
                walk_loop = int(walk_loop)
                print(walk_loop)
                robo._motion.walk("BACKWARD", walk_loop)
                
            
            
            self.act = Act.PUTTING_POS
            
            #return True
            
        #=======================================================#
        #                     3. Putting Pos                    #         
        #=======================================================#
            
        elif act == Act.PUTTING_POS:             ##### 3. 퍼팅 위치에 서기 #################
            ###### 홀컵 중앙 맞추기 #######################
            
            print("^^^^333333")
            print("^^^^333333")
            print("^^^^333333")
            print("^^^^333333")

            robo._motion.head("DOWN", 30) # 고개 45도로 내리고 공 detect 시작 !
            robo._motion.head("DOWN", 9)
            robo._motion.head("DOWN", 6)
            time.sleep(1)
            robo._motion.head("DOWN", 9)
            time.sleep(1)
            Distance.Head_UD_Angle = 55
            
            
            is_holecup_in_frame = robo._image_processor.detect_holecup()
            
            robo._motion.head("DEFAULT", 1) # 고개 상하 디폴트
            
            if is_holecup_in_frame == False:    
                print("holecup NONONONONONO")
                # big UD head
                while True:
                    is_big_UD = big_UD("holecup")
                    if is_big_UD == "Except" :  # big UD 검출안됨 -> big LR 로 넘어감
                        print("holecup big UD except")
                        big_LR("holecup")
                        
                    is_small_LR = small_LR("holecup")
                    print("small lr finished")

                    if is_small_LR == "Except" :
                        robo._motion.head("DEFAULT", 2) # small_LR 한 후 고개 디폴트
                        
                        big_LR("holecup") # 이거 한번만 실행하면 무조건 찾을 거라고 생각해서 while로 안 돌아감.
                    else:
                        break

                # !! 근데, is_holecup_in_frame==True인 경우에 
                # LR head값 어차피 안바뀌니까 여기에 넣어도 될듯 ??
                ## 아니면 tab 한 번 더 줘서 고개 한 번당 sidewalk 한 번 해도됨

                #====== holecup 고개 방향만큼 꽃게 걸음 ======#
                side_walk = int(abs(100-Distance.Head_ud_angle)//10) # 식은 시행착오거치면서 변경예정

                print("**flower dog start**")
                # side walk 방향 설정 
                if  Distance.small_lr_angle < 100:
                    # 고개가 왼쪽L이면 오른쪽R으로 side walk해라
                    print("꽃게 걸음 오른쪽")
                    side_lr = "RIGHT"
                elif Distance.small_lr_angle > 100 : 
                    # 고개가 오른쪽R이면 왼쪽L으로 side walk해라
                    print("꽃게 걸음 왼쪽")
                    side_lr = "LEFT"

                print("side walk -------", side_walk)
                # motion.py에 walk_side for문이 없어서 임시로 여기다 넣음
                for _ in range(side_walk):
                    robo._motion.walk_side(side_lr)
                
            robo._motion.head("DEFAULT", 2) # LR 한 후 고개 디폴트
                    
            print("holecup YES")
            ###### 홀컵 찾음, 중앙 맞췄음. 일직선 맞추고, 이제 거리 재야됨

            
 
            while True:
                # 공 홀컵 일직선 맞추기
                print("!!call straight ")
                check_straight = head.straight()
                if check_straight == True: # 거리 알고리즘으로 넘어감
                    print("straight true!!")
                    break
                elif check_straight == "Except":
                    print("straight except")
                    while True:
                        robo._motion.head("DEFAULT", 1)
                        is_big_UD = big_UD("ball")
                        
                        if is_big_UD == "Except":
                            big_LR("ball")
                        is_small_LR = small_LR("ball")
                        
                        if is_small_LR == "Except" :
                            robo._motion.head("DEFAULT", 2) # small_LR 한 후 고개 디폴트
                            # big 알고리즘으로 넘어감
                            # is_big_LR = big_LR("ball") 하러 처음으로 올라감 
                            big_LR("ball") # 이거 한번만 실행하면 무조건 찾을 거라고 생각해서 while로 안 돌아감.
                        else:
                            break
                else:
                    continue                  
                    
                
            ##### straight 알고리즘하다가 중앙이 흐트려졌을 거라 판단하여 -> 중앙 맞추기 시작
            
            ### field 블랙 판별 => 좌우 퍼팅 결정   
            Distance.field = robo._image_processor.field() #return left, right
            Distance.field = "left" ##temp
            #몸 퍼팅 위치에 서기
            if Distance.field == "left" :
                print("field left!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                robo._motion.pose("LEFT")
            elif Distance.field == "right" :
                print("field right!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                robo._motion.pose("RIGHT")

            time.sleep(7)
            
            ########################################    
            ############# 거리 알고리즘 #############
            
            # 홀컵 middle 맞추기
            
            # ud_for_dist 하기전에 고개 세팅
            robo._motion.head("DEFAULT", 2) # 고개 디폴트
            Distance.Head_ud_angle = Distance.Head_UD_Middle_Value_Measures
            robo._motion.head("DEFAULT", 1) # 고개 디폴트
            
            robo._motion.head("DOWN", 45)
            
            # ud_for_dist 하기전에 holecup 찾기
            # holecup찾기 (고개 O, 몸 X)
            while True:
                big_LR("holecup")
                is_small_LR = small_LR("holecup")

                if is_small_LR == "Except" :
                    print("holecup small lr except")
                    robo._motion.head("DEFAULT", 2) # small_LR 한 후 고개 디폴트
                    
                    big_LR("holecup") # 이거 한번만 실행하면 무조건 찾을 거라고 생각해서 while로 안 돌아감.
                else:
                    break
            
            
            
            robo._motion.head("DOWN", 45)
            Distance.Head_UD_Angle = 10
            holecup_UD_for_dist() # 홀컵 거리 재기
            robo._motion.head("DEFAULT", 1) # ud for dist 이후 고개 상하 디폴트
            time.sleep(2)
                            
            # 홀컵 거리 재기
            Distance.holecup_dist = Distance.Length_ServoAngle_dict.get(Distance.Head_ud_angle)
            
            print("holecup dist : ", Distance.holecup_dist)
            # 이 length를 퍼팅 파워로 바꿔주는 코드 필요 -> 직접해보면서 조절
            power = Distance.holecup_dist
            
            if Distance.holecup_dist < 0: # 20 값 바꾸기
                self.act = Act.HOLEIN
                print("거리가 너무 작아서 HOLEIN으로!!!")
            else:
                self.act = Act.PUTTING

            # 공 거리는 Act 4(PUTTING)에서 재기
            '''
            else:   #================= 공 거리 재기 =================#    
                # 공 middle 맞추기
                robo._motion.head("DEFAULT", 2) # 고개 정면 LR으로
                
                ### 이연이 포즈 모션 정확하면 필요없긴함 
                while True:
                    big_LR("ball")
                    is_small_LR = small_LR("ball")

                    if is_small_LR == "Except" :
                        print("ball small lr except")
                        robo._motion.head("DEFAULT", 2) # small_LR 한 후 고개 디폴트
                        
                        big_LR("ball") # 이거 한번만 실행하면 무조건 찾을 거라고 생각해서 while로 안 돌아감.
                    else:
                        break
                ###
                
                #small ud head
                Distance.Head_ud_angle = Distance.Head_UD_Middle_Value_Measures
                UD_for_dist("ball")
                robo._motion.head("DEFAULT", 1) # ud for dist 이후 고개 상하 디폴트
                time.sleep(2)
    
                # 공 거리 재기 => 15cm 거리 미세조정
                ball_dist = Distance.Length_ServoAngle_dict.get(Distance.Head_ud_angle)
                Distance.Head_ud_angle = Distance.Head_UD_Middle_Value_Measures
                
                self.act = Act.PUTTING
                
                print("ball dist : ", ball_dist)'''
                
            return True

            
        
        
        
        
        #=======================================================#
        #                      4. Putting                       #         
        #=======================================================#
        
        elif act == Act.PUTTING:             ##### 4. 퍼팅 #################
            ##################### 2.의 중간 맞추는 코드 가져옴
            ### 거리 알고리즘
            # 홀컵 middle 맞추기
            # 홀컵 거리 재기
            ######## 홀컵 거리 재기 위해
            
            print("^^^^444444")
            print("^^^^444444")
            print("^^^^444444")
            print("^^^^444444")


            robo._motion.head("DOWN", 45) # 고개 45도로 내리고 공 detect 시작 !
            # robo._motion.head("DOWN", 30) # 고개 45도로 내리고 공 detect 시작 !
            # robo._motion.head("DOWN", 9) # 고개 45도로 내리고 공 detect 시작 !
            # robo._motion.head("DOWN", 6) # 고개 45도로 내리고 공 detect 시작 !
            time.sleep(1)

            Distance.Head_UD_Angle = 55


            # print("ball not detected")
            # # big UD head
            # while True:
            #     big_LR("ball")
            #     is_small_LR = small_LR("ball")

            #     if is_small_LR == "Except" :
            #         print("ball small lr except")
            #         robo._motion.head("DEFAULT", 2) # small_LR 한 후 고개 디폴트
                    
            #         big_LR("ball") # 이거 한번만 실행하면 무조건 찾을 거라고 생각해서 while로 안 돌아감.
            #     else:
            #         break
                         
            # print("ball YESYES")

            # ud_for_dist 하기전에 고개 세팅
            robo._motion.head("DEFAULT", 2) # 고개 디폴트
            Distance.Head_ud_angle = Distance.Head_UD_Middle_Value_Measures
            robo._motion.head("DEFAULT", 1) # 고개 디폴트

            UD_for_dist("ball")
            robo._motion.head("DEFAULT", 1) # ud for dist 이후 고개 상하 디폴트
            time.sleep(2)

            # length = 거리 
            ball_dist = Distance.Length_ServoAngle_dict.get(Distance.Head_ud_angle)
            print(Distance.Length_ServoAngle_dict)
            print("=====================================")
            print(ball_dist , "======HEE=====", Distance.Head_ud_angle)
            print("=====================================")
            
            while True:
                print("ball dist :", ball_dist)
                if 16 <= ball_dist <= 20: # 거리 값 조정 필요!
                    break
                elif ball_dist < 16:
                    robo._motion.walk("JBACKWARD")
                    ball_dist += 3
                elif ball_dist > 20:
                    robo._motion.walk("JFORWARD")
                    ball_dist -= 3

            time.sleep(2)

            ### 진짜 퍼팅
            ###### 홀 컵 거리에 따라 퍼팅 강도 조절하기
            if 0 < Distance.holecup_dist <= 10:
                # Motion.putting() # 나중에 robo의 motion변수를 없애고 아래 코드가 아닌 이 코드로 변경할 예정
                robo._motion.putting(Distance.field, 1) # def putting 짜야함 + 방향과 강도를 넘겨줌
            elif 10 < Distance.holecup_dist <= 30:
                # Motion.putting() 
                robo._motion.putting(Distance.field, 1) 
            elif 30 < Distance.holecup_dist <= 40:
                robo._motion.putting(Distance.field, 1) 
            elif 40 < Distance.holecup_dist <= 50:
                robo._motion.putting(Distance.field, 4) 
            else:
                robo._motion.putting(Distance.field, 1) 
                print("거리 50cm 이상")
                
            #self.act = Act.WALK_BALL
            robo._motion.turn("LEFT", 60)
            robo._motion.turn("LEFT", 45 )

            #return True

            

        
        elif act == Act.HOLEIN:             ##### 5. 홀인 #################
            
            print("^^^^^^^^5555555")
            print("^^^^^^^^5555555")
            print("^^^^^^^^5555555")
            print("^^^^^^^^5555555")

            robo._motion.turn("LEFT", 45)
            time.sleep(1)
            robo._motion.turn("LEFT", 45)

            time.sleep(3)

            

            robo._motion.head("DOWN", 30)
            robo._motion.head("DOWN", 9)
            robo._motion.head("DOWN", 6)
            time.sleep(2)
            oneframe = robo._image_processor.ball_hole_oneframe()
            print("is oneframe?")
            if oneframe == True:
                check_holein = robo._image_processor.detect_hole_in()
                if check_holein == True:
                    print("ceremony hehehehehe")
                    # 세레모니
                    robo._motion.ceremony()
                else:
                    print("holein fail")
                    # 몰라. 3번을 더 간단히?
                    pass

            else:   
                print('go putting pos')
                # 퍼팅준비로 돌아감
                act = Act.PUTTING_POS

            
            return True
            
            
            
            
           

        
