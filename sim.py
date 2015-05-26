#!/usr/bin/env python
# Author: Will Skywalker

# Air Traffic Control Simulator 
# License: Apache 2.0

import random, math

import sim_gui, kaitak


__version__ = '0.0.1'


APPROACHING_POINTS = (((220, 50), 100, 190),
                      ((560, 50), 120, 255),
                      ((760, 50), 180, 260),
                      ((790, 240), 220, 320),
                      ((790, 540), 230, 350),
                      ((640, 680), 280, 360),
                      ((370, 680), 0, 90),
                      ((220, 630), 35, 85))


class Airport(object):

    def __init__(self, runway=[(270, 275), (330, 275)], runway_available=[True], wind_direction=0, wind_speed=0):
        self._runway = runway
        self._runway_available = runway_available
        self._wind_direction = wind_direction
        self._wind_speed = wind_speed
        self._ready_line = {}
        self._waiting_line = {}
        self._arrival_line = {}

    def get_runway(self):
        return self._runway[0][0]+215, self._runway[0][1]+40, self._runway[1][0]+215, self._runway[1][1]+40

    def get_arrival_line(self):
        return self._arrival_line

    def get_ready_line(self):
        return self._ready_line

    def get_waiting_line(self):
        return self._waiting_line

    def update(self):
        for each in self._arrival_line.values():
            each.update()

    def new_arrival_plane(self):
        codenum = random.randrange(12)
        num = random.randrange(30, 4000)
        point = random.choice(APPROACHING_POINTS)
        self._arrival_line[kaitak.code[codenum]+str(num)] = Plane(kaitak.companies[codenum], random.choice(kaitak.mode), 
                                                                  kaitak.code[codenum]+str(num), 'Arrival', 
                                                                  random.choice([5000, 6000, 7000, 8000]),
                                                                  random.randrange(240, 300), random.randrange(point[1], point[2]),
                                                                  point[0])
        return kaitak.companies[codenum] + ', ' + ' '.join(list(str(num)))



class Plane(object):

    def __init__(self, company, model, number, state='Ready', height=0, speed=0, direction=0, place=[799, 799]):
        self._company = company
        self._model = model
        self._number = number
        self._state = state
        self._height = height
        self._speed = speed
        self._direction = direction
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

    def get_direction(self):
        return self._direction

    def get_place(self):
        return self._place

    def change_altitude(self, target):
        if self._height != target:
            self._direction += 50 if self._height<target else self._direction-50

    def change_speed(self, speed):
        if self._height != target:
            self._direction += 10 if self._height<target else self._direction-10

    def change_direction(self, target, turn=None):
        if self._direction != target:
            if turn:
                self._direction += 1 if turn == 'left' else self._direction-1
            else:
                self._direction += 1 if abs(self._direction-target)<180 else self._direction-1

    def update(self):
        print self._speed, self._direction
        print self._speed * math.cos(self._direction/180*math.pi) / 100, self._speed * math.sin(self._direction/180*math.pi) / 100
        self._place[0] += self._speed * math.cos((self._direction-90)/180.0*math.pi) / 300
        self._place[1] += self._speed * math.sin((self._direction-90)/180.0*math.pi) / 300
        


if __name__ == '__main__':
    sim_gui.SimulatorGUI(Airport([(275, 245), (325, 355)]))

        


