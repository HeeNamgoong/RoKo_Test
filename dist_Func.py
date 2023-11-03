## 거리 측정
    # def distance(object):
    #     f = 450
    #     while True:
    #         is_horizontal_middle, small_ud_temp = Head.small_LR_head(object, small_ud_angle)
    #         if is_horizontal_middle == True: #최종 중앙 맞춰짐 
    #             if object == "holecup":
    #                 #### 홀컵 까지의 대략적인 거리 재기 
    #                 fake_dist = Distance.holecup_dist(f)
    #                 break
    #             elif object == "ball":
    #                 #### 공 까지의 대략적인 거리 재기
    #                 fake_dist = Distance.ball_dist(f)
    #                 break

    #         elif is_horizontal_middle == False:
    #             small_ud_angle = small_ud_temp
    #             continue
 
    #     # 홀컵 거리 인식에서 f값 결정
    #     # 가까운지 먼지
    #     if fake_dist >= 50:
    #         f = 450
    #     else : 
    #         f = 270
    #     # 홀컵 거리
    #     if object == "holecup":
    #         holecup_dist = Distance.holecup_dist(f)
    #         return holecup_dist
    #     else : # object == "ball"
    #         ball_dist = Distance.ball_dist(f)
    #         return ball_dist
