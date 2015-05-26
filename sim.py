#!/usr/bin/env python
# Author: Will Skywalker

# Air Traffic Control Simulator 
# License: Apache 2.0

import random

import sim_gui, kaitak


__version__ = '0.0.1'


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

    def new_arrival_plane(self):
        codenum = random.randrange(12)
        num = random.randrange(30, 4000)
        self._arrival_line[kaitak.code[codenum]+str(num)] = Plane(kaitak.companies[codenum], random.choice(kaitak.mode), kaitak.code[codenum]+str(num), 'Arrival')




class Plane(object):

    def __init__(self, company, model, number, state, height=0, speed=0, direction=0):
        self._company = company
        self._model = model
        self._number = number
        self._state = state
        self._height = height
        self._speed = speed
        self._direction = direction

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

    def change_altitude(self, change):
        self._height += change

    def change_speed(self, change):
        self._speed += change

    def change_direction(self, target, turn=None):
        if self._direction != target:
            if turn:
                self._direction += 1 if turn == 'left' else self._direction-1
            else:
                self._direction += 1 if abs(self._direction-target)<180 else self._direction-1


if __name__ == '__main__':
    sim_gui.SimulatorGUI(Airport([(275, 245), (325, 355)]))

        


