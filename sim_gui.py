#!/usr/bin/env python

import time, os, random
import kaitak
import Tkinter as Tk
# from sim import __version__

PHOTOS = {}

class SimulatorGUI():

    def __init__(self, airport):
        self._airport = airport
        self._root = Tk.Tk()
        self._root.title("Air Traffic Control Simulator ")
        self._frame = Tk.Canvas(self._root, bg='#003366',
                             width=800,
                             height=690)
        self._frame.grid()
        self._order = ''

        self.input_move = Tk.Entry(self._root, width=100)
        self.input_move.bind("<Return>", self.enter_order)
        self.input_move.grid(row=1)
        self._root.after(3000, self.tick)

        PHOTOS['aeroflot'] = Tk.PhotoImage(file='logos/aeroflot.gif')
        PHOTOS['air india'] = Tk.PhotoImage(file='logos/air india.gif')
        PHOTOS['all nippon'] = Tk.PhotoImage(file='logos/all nippon.gif')
        PHOTOS['cathay'] = Tk.PhotoImage(file='logos/cathay.gif')
        PHOTOS['china eastern'] = Tk.PhotoImage(file='logos/china eastern.gif')
        PHOTOS['china southern'] = Tk.PhotoImage(file='logos/china southern.gif')
        PHOTOS['dynasty'] = Tk.PhotoImage(file='logos/dynasty.gif')
        PHOTOS['emirates'] = Tk.PhotoImage(file='logos/emirates.gif')
        PHOTOS['fedex express'] = Tk.PhotoImage(file='logos/fedex express.gif')
        PHOTOS['lufthansa'] = Tk.PhotoImage(file='logos/lufthansa.gif')
        PHOTOS['qantas'] = Tk.PhotoImage(file='logos/qantas.gif')
        PHOTOS['united'] = Tk.PhotoImage(file='logos/united.gif')
        PHOTOS['ups'] = Tk.PhotoImage(file='logos/ups.gif')
        bg = Tk.PhotoImage(file='logos/background.gif')

        self._frame.create_image(402, 20, image=bg)
        self._frame.create_line(*self._airport.get_runway(), width=4, fill='white')
        self._frame.create_text(self._airport.get_runway()[0]-8, self._airport.get_runway()[1]-8, text='13', fill='white')
        self._frame.create_text(self._airport.get_runway()[2]+8, self._airport.get_runway()[3]+8, text='31', fill='white')
        self._frame.create_line(0, 40, 803, 40, width=5)
        self._frame.create_line(210, 40, 210, 693, width=5)
        self._frame.create_text(130, 20, text=kaitak.__doc__, fill='white')
        self._frame.create_text(780, 20, text=time.strftime('%H:%M', time.localtime()), fill='white')
        self._count = 0

        self.draw(self._frame)
        self._root.mainloop()

    def tick(self):
        self._count += 1
        if self._order == "":
            if self._count >= 15:
                sound = self._airport.new_arrival_plane()
                self.draw(self._frame)
                os.system('say '+random.choice(kaitak.greetings)+sound+' -r 200')
                self._count = 0
            self._airport.update()
            self.draw(self._frame)
            self._root.after(500, self.tick)
            return

        self.draw(self._frame)
        self._root.after(500, self.tick)

    def solve(self):
        new_puzzle = self._puzzle.clone()
        self.order = new_puzzle.solve_puzzle()

    def print_moves(self):
        print self._current_moves
        self._current_moves = ""

    def enter_order(self, event):
        order = self.input_move.get()
        self.input_move.delete(0, 100)


    def draw(self, canvas):
        """
        Draw the puzzle
        """
        canvas.delete('temp')
        arrivals = self._airport.get_arrival_line().values()
        for i in xrange(len(arrivals)):
            canvas.create_rectangle(0, 43+i*100, 208, 143+i*100, fill='white', width=2, tags='temp')

        for i, plane in enumerate(arrivals):
            canvas.create_image(65, 75+i*100, image=PHOTOS[plane.get_company()], tags='temp')
            canvas.create_text(165, 75+i*100, text=plane.get_number(), tags='temp')
            canvas.create_text(65, 115+i*100, text=plane.get_info(), fill='#666699', tags='temp')
            canvas.create_text(165, 115+i*100, text=plane.get_state(), fill='#006600', tags='temp')
            place = plane.get_place()
            canvas.create_oval(place[0]-5, place[1]-5, place[0]+5, place[1]+5, fill='white', tags='temp')
            canvas.create_text(place[0]-30, place[1]-15, text=plane.get_number()+'\n'+str(plane.get_height())[:2]+' '+str(plane.get_speed()), fill='white', tags='temp')
