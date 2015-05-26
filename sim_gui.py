#!/usr/bin/env python

import time
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
        PHOTOS['air_india'] = Tk.PhotoImage(file='logos/air india.gif')
        PHOTOS['all_nippon'] = Tk.PhotoImage(file='logos/all nippon.gif')
        PHOTOS['cathay'] = Tk.PhotoImage(file='logos/cathay.gif')
        PHOTOS['china_eastern'] = Tk.PhotoImage(file='logos/china eastern.gif')
        PHOTOS['china_southern'] = Tk.PhotoImage(file='logos/china southern.gif')
        PHOTOS['dynasty'] = Tk.PhotoImage(file='logos/dynasty.gif')
        PHOTOS['emirates'] = Tk.PhotoImage(file='logos/emirates.gif')
        PHOTOS['fedex_express'] = Tk.PhotoImage(file='logos/fedex express.gif')
        PHOTOS['lufthansa'] = Tk.PhotoImage(file='logos/lufthansa.gif')
        PHOTOS['qantas'] = Tk.PhotoImage(file='logos/qantas.gif')
        PHOTOS['united'] = Tk.PhotoImage(file='logos/united.gif')
        PHOTOS['ups'] = Tk.PhotoImage(file='logos/ups.gif')
        bg = Tk.PhotoImage(file='logos/background.gif')

        self._frame.create_image(402, 20, image=bg)
        self._frame.create_line(*self._airport.get_runway(), width=4, fill='white')
        self._frame.create_text(self._airport.get_runway()[0]-8, self._airport.get_runway()[1]-8, text='13', fill='white')
        self._frame.create_text(self._airport.get_runway()[2]+8, self._airport.get_runway()[3]+8, text='31', fill='white')
        self._frame.create_line(0, 40, 800, 40, width=5)
        self._frame.create_line(210, 40, 210, 690, width=5)
        self._frame.create_text(130, 20, text=kaitak.__doc__, fill='white')
        self._frame.create_text(780, 20, text=time.strftime('%H:%M', time.localtime()), fill='white')


        self.draw(self._frame)
        self._root.mainloop()

    def tick(self):
        if self._order == "":
            self._airport.new_arrival_plane()
            self.draw(self._frame)
            self._root.after(3000, self.tick)
            return

        self.draw(self._frame)
        self._root.after(3000, self.tick)

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
            # canvas.create_line(0, 43, text=time.strftime('%H:%M', time.localtime()), fill='white')

        for i, plane in enumerate(arrivals):
            canvas.create_image(60, 70+i*100, image=PHOTOS[plane.get_company()], tags='temp')
            canvas.create_text(160, 70+i*100, text=plane.get_number(), tags='temp')
            canvas.create_text(60, 110+i*100, text=plane.get_info(), fill='#666699', tags='temp')
            canvas.create_text(160, 110+i*100, text=plane.get_state(), fill='#006600', tags='temp')
