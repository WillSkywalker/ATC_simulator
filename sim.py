#!/usr/bin/env python
# Author: Will Skywalker

# Air Traffic Control Simulator 
# License: Apache 2.0

from __future__ import division
import random, math, time, json

import sim_gui, sound


__version__ = '0.0.1'


APPROACHING_POINTS = (((220, 50), 100, 190),
                      ((560, 50), 120, 255),
                      ((760, 50), 180, 260),
                      ((790, 240), 220, 320),
                      ((790, 540), 230, 350),
                      ((640, 680), 280, 360),
                      ((370, 680), 0, 90),
                      ((220, 630), 35, 85))
COMPANY_NUMBER = 12


def choose_airport(name):
    return json.load(open('maps/'+name+'.json'))


class Airport(object):

    def __init__(self, the_map):
        self._info = the_map
        self._runway = the_map['runway']
        self._runway_point = the_map['runway_point']
        self._runway_available = True
        self.full_name = the_map['full_name']
        # self._wind_direction = wind_direction
        # self._wind_speed = wind_speed
        self._ready_line = {}
        self._waiting_line = {}
        self._arrival_line = {}

    def get_companies(self):
        return self._info['companies']

    def get_codes(self):
        return self._info['code']

    def get_modes(self):
        return self._info['mode']

    def get_runway(self):
        return (self._runway[0][0]+215, self._runway[0][1]+40, 
                self._runway[1][0]+215, self._runway[1][1]+40)

    def get_arrival_line(self):
        return self._arrival_line

    def get_ready_line(self):
        return self._ready_line

    def get_waiting_line(self):
        return self._waiting_line

    def update(self):
        for each in self._arrival_line.values():
            each.update()
            if each.get_height() == 0:
                del self._arrival_line[each.get_number()]
                print self._arrival_line
                raise EOFError, each.get_number()+': '+ \
                    sound.male_report("We have landed at Runway "+each.get_landing_way()+'. Thank you.')
                

    def control_plane(self, code, order, num=0, *otras):
        if code.upper() in self._ready_line:
            self._ready_line[code.upper()].receive_order(order, num)
        elif code.upper() in self._waiting_line:
            self._waiting_line[code.upper()].receive_order(order, num)
        elif code.upper() in self._arrival_line:
            self._arrival_line[code.upper()].receive_order(order, num)
            

    def new_arrival_plane(self):
        codenum = random.randrange(COMPANY_NUMBER)
        num = random.randrange(30, 4000)
        point = random.choice(APPROACHING_POINTS)
        self._arrival_line[self._info['code'][codenum]+str(num)] = Plane(
            self._info['companies'][codenum], random.choice(self._info['mode']), 
            self._info['code'][codenum]+str(num), 'Arrival', 
            random.choice([5000, 6000, 7000, 8000]),
            random.randrange(240, 300), random.randrange(point[1], point[2]),
            point[0])
        return self._info['code'][codenum], self._info['companies'][codenum]+' ', num



class Plane(Airport):

    def __init__(self, company, model, number, state='Ready', height=0, 
                 speed=0, direction=0, place=[799, 799]):
        self._company = company
        self._model = model
        self._number = number
        self._state = state
        self._target_height = self._height = height
        self._target_speed = self._speed = speed
        self._target_direction = self._direction = direction
        self._place = list(place)


    def get_info(self):
        return self._model

    def get_number(self):
        return self._number

    def get_company(self):
        return self._company

    def get_state(self):
        return self._state

    def get_speed(self):
        return self._speed

    def get_height(self):
        return self._height

    # def get_direction(self):
    #     return self._direction

    def get_place(self):
        return self._place

    def get_landing_way(self):
        return self._landing_way

    def receive_order(self, order, num):
        time.sleep(1.5)
        if order.lower() == 'c':
            if len(num) == 3:
                if 0 <= int(num) <= 360:
                    self._target_direction = int(num)
                    sound.male_report('Roger, heading '+' '.join(list(num)))

            elif len(num) == 1 and num > 1:
                self._target_height = int(num)*1000
                sound.male_report('Roger, maintain '+num+'000 inches.')
        elif order.lower() == 's':
            self._target_speed = int(num)
            sound.male_report('Roger, speed changing to '+num+' knots.')
        elif order.lower() == 'l':
            if self._height > 3000:
                raise ValueError, self._number+': '+ \
                    sound.male_report("Negative, we are too high to land now.")
            elif abs(self._direction - the_map['runway_point'][num][1]) > 45 or \
                math.sqrt((self._place[0]-the_map['runway_point'][num][0][0])**2 \
                +(self._place[1]-the_map['runway_point'][num][0][1])**2) > 150:

                # print self._place, the_map['runway_point'][num]
                # print math.sqrt((self._place[0]-the_map['runway_point'][num][0][0])**2 + (self._place[1]-the_map['runway_point'][str(num)][0][1])**2)
                raise ValueError, self._number+': '+ \
                    sound.male_report("Negative, we are too far away from the runway.")
            else:
                self._state = 'Landing'
                self._target_speed = random.randrange(120, 160)
                self._target_height = random.randrange(600, 900)
                sound.male_report("Roger, we are approaching the runway.")
                self._target_direction = math.degrees(math.atan2((the_map['runway_point'][num][0][0]-self._place[0]), 
                                                    (the_map['runway_point'][num][0][1]-self._place[1])))%360
                self._landing_way = num
        else:
            raise ValueError, self._number+': '+ \
                sound.male_report("Negative, your order is invalid.")




    def update(self):
        # print self._number, self._direction
        self._place[0] += self._speed * math.sin((self._direction)/180*math.pi) / 200
        self._place[1] += self._speed * math.cos((self._direction)/180*math.pi) / -200
        if self._height != self._target_height:
            self._height = self._height+50 if self._height<self._target_height else self._height-50
        if abs(self._speed - self._target_speed) > 5:
            self._speed = self._speed+5 if self._speed<self._target_speed else self._speed-5
        if self._direction != self._target_direction:
            self._direction = (self._direction+1)%360 \
                if 0<(self._target_direction-self._direction)<180 \
                or (self._target_direction-self._direction)<-180 \
                else (self._direction-1)%360
        if self._state == 'Landing':
            self._target_direction = math.degrees(math.atan2((the_map['runway_point'][self._landing_way][0][0]-self._place[0]), 
                                                 (self._place[1]-the_map['runway_point'][self._landing_way][0][1])))%360
            compare = math.degrees(math.atan2((540-self._place[0]), (self._place[1]-395)))%360
            if abs(self._place[0]-the_map['runway_point'][self._landing_way][0][0])<5 and abs(self._place[1]-the_map['runway_point'][self._landing_way][0][1])<5:
                self._target_height = 0
                self._target_direction = the_map['runway_point'][self._landing_way][1]
                self._target_speed = 1
                self._state = 'Landed'
                

        


if __name__ == '__main__':
    the_map = choose_airport('kaitak')
    sim_gui.SimulatorGUI(Airport(choose_airport('kaitak')))

        


