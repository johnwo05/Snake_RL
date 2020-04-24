import pygame as pg
from settings import *
import random
import numpy as np
import math
import sys

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(ORANGE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.dx = 1
        self.dy = 0

        self.ate_food = False
        self.moved = False
        self.has_body = False
        self.hit_wall = False

        self.last_x = 0
        self.last_y = 0

        self.food_x = 0
        self.food_y = 0

        self.initial = True

        self.state_0 = True
        self.state_1 = False
        self.state_2 = False
        self.state_3 = False

        self.state_0_index = 0
        self.state_1_index = 1
        self.state_2_index = 2
        self.state_3_index = 3

        self.reward_matrix = np.array([[1, 1, 1, -1000],[1,1,-1000,1],[1, -1000, 1, 1], [-1000, 1, 1, 1]])


    def look_for_wall(self):
        a = np.array([[10000],[10000]])

        for wall in self.game.walls:
            for i in range(0,48):
                if wall.x == self.game.vision_field[0][i] and wall.y == self.game.vision_field[1][i]:
                    wall_point = np.array([[wall.x], [wall.y]])
                    a = np.append(a, wall_point, axis=1)

        return a


    def look_for_food(self):
        a = np.array([[10000],[10000]])

        for i in range(0,48):
            if self.game.food.x == self.game.vision_field[0][i] and self.game.food.y == self.game.vision_field[1][i]:
                food_point = np.array([[self.game.food.x], [self.game.food.y]])
                a = np.append(a, food_point, axis=1)
        return a

    def distance_formula(self,x1, y1, x2, y2):
        distance = abs(math.sqrt(((x2 - x1)**2) +((y2-y1)**2) ))
        return distance

    def check_distance_value(self,A):
        if A == 0:
            additional_reward = -1000
        elif A == 1:
            additional_reward = -9
        elif A == (math.sqrt(2)):
            additional_reward = -8
        elif A == 2:
            additional_reward = -7
        elif A == math.sqrt(5):
            additional_reward = -6
        elif A == 3:
            additional_reward = -5
        elif A == math.sqrt(10):
            additional_reward = -4
        elif A == (2*math.sqrt(2)):
            additional_reward = -3
        elif A == math.sqrt(13):
            additional_reward = -2
        elif A == (3*math.sqrt(2)):
            additional_reward = -1
        else:
            additional_reward = 0
        return additional_reward

    def check_food_distance_value(self, B):
            if B == 0:
                additional_reward = 2000
            elif B == 1:
                additional_reward = 900
            elif B == (math.sqrt(2)):
                additional_reward = 800
            elif B == 2:
                additional_reward = 700
            elif B == math.sqrt(5):
                additional_reward = 600
            elif B == 3:
                additional_reward = 500
            elif B == math.sqrt(10):
                additional_reward = 400
            elif B == (2*math.sqrt(2)):
                additional_reward = 300
            elif B == math.sqrt(13):
                additional_reward = 200
            elif B == (3*math.sqrt(2)):
                additional_reward = 100
            else:
                additional_reward = 0
            return additional_reward


    def update_reward_matrix(self):
        self.reward_matrix = np.array([[1, 1, 1, -1000],[1,1,-1000,1],[1, -1000, 1, 1], [-1000, 1, 1, 1]])
        Food_Points = self.look_for_food()
        Wall_Points = self.look_for_wall()

        additional_reward = 0


        #Calculate Player position at next State for each possible move
        #Assign reward values based on distance from walls and distance from FOOD_LEFT
        #If no walls are food are in players vision field, generic reward matrix is used



        if self.state_0:

            # print("moving right")

            zero_to_zero = np.array([[self.x + 1], [self.y]])
            #Iterate Through Food_points

            for i in range(np.size(Wall_Points,1)):
                A = self.distance_formula(zero_to_zero[0][0],zero_to_zero[1][0],Wall_Points[0][i],Wall_Points[1][i])

                additional_reward += self.check_distance_value(A)

            self.reward_matrix[0][0] = self.reward_matrix[0][0] +  additional_reward


            for j in range(np.size(Food_Points,1)):
                B = self.distance_formula(zero_to_zero[0][0],zero_to_zero[1][0],Food_Points[0][j],Food_Points[1][j])

                additional_reward = self.check_food_distance_value(B)
            #     print('Food Points: ')
            #     print(str(Food_Points[0][j]) + ' ' + str(Food_Points[1][j]))
            #     print('Distance: ')
            #     print(B)
            #
            # print(additional_reward)
            self.reward_matrix[0][0] = self.reward_matrix[0,0] +  additional_reward


            zero_to_one = np.array([[self.x], [self.y - 1]])
            for i in range(np.size(Wall_Points,1)):
                A = self.distance_formula(zero_to_one[0][0],zero_to_one[1][0],Wall_Points[0][i],Wall_Points[1][i])
                additional_reward += self.check_distance_value(A)
            self.reward_matrix[0][1] = self.reward_matrix[0][1] +  additional_reward

            for j in range(np.size(Food_Points,1)):
                B = self.distance_formula(zero_to_one[0][0],zero_to_one[1][0],Food_Points[0][j],Food_Points[1][j])
                additional_reward = self.check_food_distance_value(B)
            self.reward_matrix[0][1] = self.reward_matrix[0][1] +  additional_reward




            zero_to_two = np.array([[self.x], [self.y + 1]])
            for i in range(np.size(Wall_Points,1)):
                A = self.distance_formula(zero_to_two[0][0],zero_to_two[1][0],Wall_Points[0][i],Wall_Points[1][i])
                additional_reward += self.check_distance_value(A)
            self.reward_matrix[0][2] = self.reward_matrix[0][2] +  additional_reward


            for j in range(np.size(Food_Points,1)):
                B = self.distance_formula(zero_to_two[0][0],zero_to_two[1][0],Food_Points[0][j],Food_Points[1][j])
                additional_reward = self.check_food_distance_value(B)

            self.reward_matrix[0][2] = self.reward_matrix[0][2] +  additional_reward
            # print(self.reward_matrix)



        if self.state_1:
            # print('moving up')
            one_to_zero = np.array([[self.x + 1], [self.y]])
            #Iterate Through Food_points

            for i in range(np.size(Wall_Points,1)):
                A = self.distance_formula(one_to_zero[0][0],one_to_zero[1][0],Wall_Points[0][i],Wall_Points[1][i])
                additional_reward += self.check_distance_value(A)
            self.reward_matrix[1][0] = self.reward_matrix[1][0] +  additional_reward

            for j in range(np.size(Food_Points,1)):
                B = self.distance_formula(one_to_zero[0][0],one_to_zero[1][0],Food_Points[0][j],Food_Points[1][j])
                additional_reward = self.check_food_distance_value(B)
            self.reward_matrix[1][0] = self.reward_matrix[1][0] +  additional_reward


            one_to_one = np.array([[self.x], [self.y - 1]])
            for i in range(np.size(Wall_Points,1)):
                A = self.distance_formula(one_to_one[0][0],one_to_one[1][0],Wall_Points[0][i],Wall_Points[1][i])
                additional_reward += self.check_distance_value(A)
            self.reward_matrix[1][1] = self.reward_matrix[1][1] +  additional_reward

            for j in range(np.size(Food_Points,1)):
                B = self.distance_formula(one_to_one[0][0],one_to_one[1][0],Food_Points[0][j],Food_Points[1][j])
                additional_reward = self.check_food_distance_value(B)
            self.reward_matrix[1][1] = self.reward_matrix[1][1] +  additional_reward



            one_to_three = np.array([[self.x - 1], [self.y]])
            for i in range(np.size(Wall_Points,1)):
                A = self.distance_formula(one_to_three[0][0],one_to_three[1][0],Wall_Points[0][i],Wall_Points[1][i])
                additional_reward += self.check_distance_value(A)
            self.reward_matrix[1][3] = self.reward_matrix[1][3] +  additional_reward

            for j in range(np.size(Food_Points,1)):
                B = self.distance_formula(one_to_three[0][0],one_to_three[1][0],Food_Points[0][j],Food_Points[1][j])
                additional_reward = self.check_food_distance_value(B)
            self.reward_matrix[1][3] = self.reward_matrix[1][3] +  additional_reward

            # print(self.reward_matrix)

        #
        if self.state_2:
            # print('moving down')
            two_to_zero = np.array([[self.x + 1], [self.y]])
            #Iterate Through Food_points

            for i in range(np.size(Wall_Points,1)):
                A = self.distance_formula(two_to_zero[0][0],two_to_zero[1][0],Wall_Points[0][i],Wall_Points[1][i])
                additional_reward += self.check_distance_value(A)
            self.reward_matrix[2][0] = self.reward_matrix[2][0] +  additional_reward

            for j in range(np.size(Food_Points,1)):
                B = self.distance_formula(two_to_zero[0][0],two_to_zero[1][0],Food_Points[0][j],Food_Points[1][j])
                additional_reward = self.check_food_distance_value(B)
            self.reward_matrix[2][0] = self.reward_matrix[2][0] +  additional_reward




            two_to_two = np.array([[self.x], [self.y + 1]])
            for i in range(np.size(Wall_Points,1)):
                A = self.distance_formula(two_to_two[0][0],two_to_two[1][0],Wall_Points[0][i],Wall_Points[1][i])
                additional_reward += self.check_distance_value(A)
            self.reward_matrix[2][2] = self.reward_matrix[2][2] +  additional_reward

            for j in range(np.size(Food_Points,1)):
                B = self.distance_formula(two_to_two[0][0],two_to_two[1][0],Food_Points[0][j],Food_Points[1][j])
                additional_reward = self.check_food_distance_value(B)
            self.reward_matrix[2][2] = self.reward_matrix[2][2] +  additional_reward



            two_to_three = np.array([[self.x - 1], [self.y]])
            for i in range(np.size(Wall_Points,1)):
                A = self.distance_formula(two_to_three[0][0],two_to_three[1][0],Wall_Points[0][i],Wall_Points[1][i])
                additional_reward += self.check_distance_value(A)
            self.reward_matrix[2][3] = self.reward_matrix[2][3] +  additional_reward

            for j in range(np.size(Food_Points,1)):
                B = self.distance_formula(two_to_three[0][0],two_to_three[1][0],Food_Points[0][j],Food_Points[1][j])
                additional_reward = self.check_food_distance_value(B)
            self.reward_matrix[2][3] = self.reward_matrix[2][3] +  additional_reward
            # print(self.reward_matrix)
        #
        if self.state_3:
            # print('moving left')
            three_to_one = np.array([[self.x], [self.y - 1]])
            #Iterate Through Food_points

            for i in range(np.size(Wall_Points,1)):
                A = self.distance_formula(three_to_one[0][0],three_to_one[1][0],Wall_Points[0][i],Wall_Points[1][i])
                additional_reward += self.check_distance_value(A)
            self.reward_matrix[3][1] = self.reward_matrix[3][1] +  additional_reward

            for j in range(np.size(Food_Points,1)):
                B = self.distance_formula(three_to_one[0][0],three_to_one[1][0],Food_Points[0][j],Food_Points[1][j])
                additional_reward = self.check_food_distance_value(B)
            self.reward_matrix[3][1] = self.reward_matrix[3][1] +  additional_reward


            three_to_two = np.array([[self.x], [self.y + 1]])
            for i in range(np.size(Wall_Points,1)):
                A = self.distance_formula(three_to_two[0][0],three_to_two[1][0],Wall_Points[0][i],Wall_Points[1][i])
                additional_reward += self.check_distance_value(A)
            self.reward_matrix[3][2] = self.reward_matrix[3][2] +  additional_reward

            for j in range(np.size(Food_Points,1)):
                B = self.distance_formula(three_to_two[0][0],three_to_two[1][0],Food_Points[0][j],Food_Points[1][j])
                additional_reward = self.check_food_distance_value(B)
            self.reward_matrix[3][2] = self.reward_matrix[3][2] +  additional_reward



            three_to_three = np.array([[self.x - 1], [self.y]])
            for i in range(np.size(Wall_Points,1)):
                A = self.distance_formula(three_to_three[0][0],three_to_three[1][0],Wall_Points[0][i],Wall_Points[1][i])
                additional_reward += self.check_distance_value(A)
            self.reward_matrix[3][3] = self.reward_matrix[3][3] +  additional_reward

            for j in range(np.size(Food_Points,1)):
                B = self.distance_formula(three_to_three[0][0],three_to_three[1][0],Food_Points[0][j],Food_Points[1][j])
                additional_reward = self.check_food_distance_value(B)
            self.reward_matrix[3][3] = self.reward_matrix[3][3] +  additional_reward

            # print(self.reward_matrix)




        return

    #Log All possible actions




    def available_actions(self):
        #MAKING CHANGES
        print(self.reward_matrix)

        if self.state_0:
            current_state_row = self.reward_matrix[0]
            av_act = np.where(current_state_row > -1000)[0]

        if self.state_1:
            current_state_row = self.reward_matrix[1]
            av_act = np.where(current_state_row > -1000)[0]


        if self.state_2:
            current_state_row = self.reward_matrix[2]
            av_act = np.where(current_state_row > -1000)[0]

        if self.state_3:
            current_state_row = self.reward_matrix[3]
            av_act = np.where(current_state_row > -1000)[0]

        return av_act

    #Randomly select next Action
    def sample_next_action(self,available_act):

        try:
            if not available_act:
                if self.state_0:
                    available_act = [0, 1, 2]
                    next_action = int(np.random.choice(available_act, 1))
                if self.state_1:
                    available_act = [0, 1, 3]
                    next_action = int(np.random.choice(available_act, 1))
                if self.state_2:
                    available_act = [0, 2, 3]
                    next_action = int(np.random.choice(available_act, 1))
                if self.state_3:
                    available_act = [1, 2, 3]
                    next_action = int(np.random.choice(available_act, 1))
            else:
                next_action = int(np.random.choice(available_act, 1))
            return next_action
        except:
            next_action = int(np.random.choice(available_act, 1))
            return next_action




    def choose_best_action(self):

        # av_act = self.available_actions()

        if self.state_0:
            max_index = np.where(self.game.Q_MATRIX[self.state_0_index] == np.max(self.game.Q_MATRIX[self.state_0_index]))[0]

            if max_index.shape[0] > 1:
                max_index = int(np.random.choice(max_index, size = 1))
            else:
                max_index = int(max_index)



        if self.state_1:
            max_index = np.where(self.game.Q_MATRIX[self.state_1_index] == np.max(self.game.Q_MATRIX[self.state_1_index]))[0]

            if max_index.shape[0] > 1:
                max_index = int(np.random.choice(max_index, size = 1))
            else:
                max_index = int(max_index)



        if self.state_2:
            max_index = np.where(self.game.Q_MATRIX[self.state_2_index] == np.max(self.game.Q_MATRIX[self.state_2_index]))[0]

            if max_index.shape[0] > 1:
                max_index = int(np.random.choice(max_index, size = 1))
            else:
                max_index = int(max_index)


        if self.state_3:
            max_index = np.where(self.game.Q_MATRIX[self.state_3_index] == np.max(self.game.Q_MATRIX[self.state_3_index]))[0]

            if max_index.shape[0] > 1:
                max_index = int(np.random.choice(max_index, size = 1))
            else:
                max_index = int(max_index)
        return max_index




    def press_key_based_on_action(self,action):
        if self.state_0:
            if action == 0:
                key_event = pg.event.Event(pg.KEYDOWN, key = pg.K_RIGHT)
                pg.event.post(key_event)

            if action == 1:
                key_event = pg.event.Event(pg.KEYDOWN, key = pg.K_UP)
                pg.event.post(key_event)

            if action == 2:
                key_event = pg.event.Event(pg.KEYDOWN, key = pg.K_DOWN)
                pg.event.post(key_event)


        if self.state_1:
            if action == 0:
                key_event = pg.event.Event(pg.KEYDOWN, key = pg.K_RIGHT)
                pg.event.post(key_event)

            if action == 1:
                key_event = pg.event.Event(pg.KEYDOWN, key = pg.K_UP)
                pg.event.post(key_event)

            if action == 3:
                key_event = pg.event.Event(pg.KEYDOWN, key = pg.K_LEFT)
                pg.event.post(key_event)

        if self.state_2:
            if action == 0:
                key_event = pg.event.Event(pg.KEYDOWN, key = pg.K_RIGHT)
                pg.event.post(key_event)

            if action == 2:
                key_event = pg.event.Event(pg.KEYDOWN, key = pg.K_DOWN)
                pg.event.post(key_event)

            if action == 3:
                key_event = pg.event.Event(pg.KEYDOWN, key = pg.K_LEFT)
                pg.event.post(key_event)

        if self.state_3:
            if action == 1:
                key_event = pg.event.Event(pg.KEYDOWN, key = pg.K_UP)
                pg.event.post(key_event)

            if action == 2:
                key_event = pg.event.Event(pg.KEYDOWN, key = pg.K_DOWN)
                pg.event.post(key_event)

            if action == 3:
                key_event = pg.event.Event(pg.KEYDOWN, key = pg.K_LEFT)
                pg.event.post(key_event)




    #This is the learning Algorithm
    def update_Q(self, action):


        if self.state_0:



            max_index = np.where(self.game.Q_MATRIX[action] == np.max(self.game.Q_MATRIX[action]))[0]
            # print('state0')
            # print(max_index)
            # print(max_index.shape[0])
            if max_index.shape[0] > 1:
                max_index = int(np.random.choice(max_index, size = 1))
                # print(max_index)
            else:
                max_index = int(max_index)
            max_value = self.game.Q_MATRIX[action, max_index]


            # print("CHECKIN REWARD AT STATE AND Q: ")
            # print(max_value)
            # print(action)
            # print(str(self.game.Q_MATRIX[self.state_0_index, action]))
            # print((self.reward_matrix[self.state_0_index, action]))


            #Q learning formula
            self.game.Q_MATRIX[self.state_0_index,action] += self.reward_matrix[self.state_0_index, action] + self.game.GAMMA * max_value

        if self.state_1:

            # print(action)
            #
            # print(self.game.Q_MATRIX[action])


            max_index = np.where(self.game.Q_MATRIX[action] == np.max(self.game.Q_MATRIX[action]))[0]
            # print('state1')
            # print(max_index)
            # print(max_index.shape[0])

            if max_index.shape[0] > 1:
                max_index = int(np.random.choice(max_index, size = 1))
            else:
                max_index = int(max_index)
            max_value = self.game.Q_MATRIX[action, max_index]


            #Q learining distance_formula
            self.game.Q_MATRIX[self.state_1_index,action] += self.reward_matrix[self.state_1_index, action] + self.game.GAMMA  * max_value



        if self.state_2:


            max_index = np.where(self.game.Q_MATRIX[action] == np.max(self.game.Q_MATRIX[action]))[0]
            # print('state2')
            # print(max_index)
            # print(max_index.shape[0])

            if max_index.shape[0] > 1:
                max_index = int(np.random.choice(max_index, size = 1))
            else:
                max_index = int(max_index)
            max_value = self.game.Q_MATRIX[action, max_index]


            #Q learining distance_formula
            self.game.Q_MATRIX[self.state_2_index,action] += self.reward_matrix[self.state_2_index, action] + self.game.GAMMA * max_value


        if self.state_3:


            max_index = np.where(self.game.Q_MATRIX[action] == np.max(self.game.Q_MATRIX[action]))[0]
            # print('state3')
            # print(max_index)
            # print(max_index.shape[0])

            if max_index.shape[0] > 1:
                max_index = int(np.random.choice(max_index, size = 1))
            else:
                max_index = int(max_index)
            max_value = self.game.Q_MATRIX[action, max_index]


            #Q learining distance_formula
            self.game.Q_MATRIX[self.state_3_index,action] += self.reward_matrix[self.state_3_index, action] + self.game.GAMMA * max_value


        #Normalize Q
        self.game.Q_MATRIX = self.game.Q_MATRIX / np.max(self.game.Q_MATRIX) * 100



    def move(self, dx=0, dy=0):
        if not self.collide_with_walls(dx, dy):

            self.dx = dx
            self.dy = dy

    def collide_with_walls(self, dx, dy):

        for wall in self.game.walls:

            if wall.x == self.x + dx and wall.y == self.y + dy:
                return True


        return False

    def get_food(self, dx, dy):
        for food in self.game.foods:

            if food.x == self.x + dx and food.y == self.y + dy:

                self.food_x = food.x
                self.food_y = food.y

                self.ate_food = True
                self.game.SCORE += 1
                food.moveFood()



    def grow(self):
        Body(self.game, self.food_x, self.food_y)
        #print('Body at ' + 'pos ' + str(self.food_x) + ', ' + str(self.food_y))

        self.has_body = True


    def move_body(self):
        x = self.last_x
        y = self.last_y

        # print(str(x))
        # print(str(y))
        for body in self.game.body:
            body.move(x,y)

            x = body.x
            y = body.y

    def update_state(self, x, y):
        if x == 1 and y == 0:
            self.state_0 = True
            self.state_1 = False
            self.state_2 = False
            self.state_3 = False
        elif x == 0 and y == -1:
            self.state_0 = False
            self.state_1 = True
            self.state_2 = False
            self.state_3 = False
        elif x == 0 and y == 1:
            self.state_0 = False
            self.state_1 = False
            self.state_2 = True
            self.state_3 = False
        elif x == -1 and y == 0:
            self.state_0 = False
            self.state_1 = False
            self.state_2 = False
            self.state_3 = True

    def update(self):
        if self.initial:
            self.rect.x = self.x * TILESIZE
            self.rect.y = self.y * TILESIZE
            self.initial = False

            self.update_state(self.dx, self.dy)
        else:

            self.get_food(self.dx, self.dy)

            if not self.collide_with_walls(self.dx,self.dy):
                self.last_x = self.x
                self.last_y = self.y

                self.update_state(self.dx, self.dy)

                self.x += self.dx
                self.y += self.dy

                for i in range(0,48):
                    self.game.vision_field[0][i] += self.dx
                    self.game.vision_field[1][i] += self.dy

                self.rect.x += self.dx * TILESIZE
                self.rect.y += self.dy * TILESIZE

                self.moved = True


                if self.ate_food:
                    self.grow()
                    self.ate_food = False

                if self.moved and self.has_body:


                    First = True
                    pos = [0,0]
                    i = 0
                    for body in self.game.body:

                        #print(str(pos))

                        if First:
                            #print('Prev ' + str(i) + 'pos ' + str(self.last_x) + ', ' + str(self.last_y))
                            #print('Current ' + str(i) + 'pos ' + str(self.x) + ', ' + str(self.y))
                            pos = body.move(self)
                            #print('Body ' + str(i) + 'moved to pos ' + str(pos[0]) + ', ' + str(pos[1]))
                            First = False
                            i+=1
                        else:

                            pos = body.move2(pos, self)
                            #print('Body ' + str(i) + 'moved to pos ' + str(pos[0]) + ', ' + str(pos[1]))
                            i+=1
            else:
                self.hit_wall = True

            #THIS IS THE PART WHERE THE A.I. MAKES IT's DECISIONS

            if self.game.TRAINING:

                self.update_reward_matrix()

                # print(self.reward_matrix)
                # print(self.game.Q_MATRIX)

                av_act = self.available_actions()
                action = self.sample_next_action(av_act)
                self.update_Q(action)
                self.press_key_based_on_action(action)


                # print("New_Q")
                # print(self.game.Q_MATRIX)
                # print(self.game.Q_MATRIX)
            else:
                # self.update_reward_matrix()

                # print(self.reward_matrix)
                # print(self.game.Q_MATRIX)


                action = self.choose_best_action()
                # self.update_Q(action)
                # print("New_Q")
                # print(self.game.Q_MATRIX)

                self.press_key_based_on_action(action)



            #Make a move



        #Follow the leader logic needed here




class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Food(pg.sprite.Sprite):
    def __init__(self, game):
        self.groups = game.all_sprites, game.foods
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.x = random.randrange(1,31)
        self.y = random.randrange(1,23)
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE



    def moveFood(self):
            self.x = random.randrange(1,31)
            self.y = random.randrange(1,23)
            self.rect.x = self.x * TILESIZE
            self.rect.y = self.y * TILESIZE

class Body(pg.sprite.Sprite):
    def __init__(self, game, x ,y):
        self.groups = game.all_sprites, game.walls, game.body
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(BODY)
        self.rect = self.image.get_rect()
        self.prev_x = x
        self.prev_y = y
        self.x = x
        self.y = y

        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE

    def move(self,Player):
        # print(str(self.x))
        # print(str(self.y))
        # print(str(Player.x))
        # print(str(Player.y))
        if self.x == Player.x and self.y == Player.y:
            #print('no move')
            pos =[0,0]
            return pos
        else:

            pos = [self.x, self.y]
            self.x = Player.last_x
            self.y = Player.last_y
            self.rect.x = self.x * TILESIZE
            self.rect.y = self.y * TILESIZE


            return pos

    def move2(self,pos,Player):

        if self.x == Player.x and self.y == Player.y:
            #print('Body in head')
            pos =[0,0]
            return pos

        elif self.x == pos[0]  and self.y == pos[1]:
            #print('IN BODY SPOT')
            pos =[0,0]
            return pos


        else:
            self.x = pos[0]
            self.y = pos[1]
            self.rect.x = self.x * TILESIZE
            self.rect.y = self.y * TILESIZE
            pos = [self.prev_x, self.prev_y]
            self.prev_x = self.x
            self.prev_y = self.y
            return pos



        return pos
class Sight(pg.sprite.Sprite):
    def __init__(self, game, Player, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.player = Player
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()

        self.x = x
        self.y = y
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE

    def update(self):
        self.x += self.player.dx
        self.y += self.player.dy



        self.rect.x += self.player.dx * TILESIZE
        self.rect.y += self.player.dy * TILESIZE
