#!/usr/bin/env python

import time, random
import kaitak, sound
import Tkinter as Tk
# from sim import __version__

PHOTOS = {}
ORDERS = {'c': 'Clear to ',
          's': 'Change your speed to '}

class SimulatorGUI():

    def __init__(self, airport):
        self._airport = airport
        self._root = Tk.Tk()
        self._root.title("Air Traffic Control Simulator ")
        self._frame = Tk.Canvas(self._root, bg='#003366',
                             width=800,
                             height=720)
        self._frame.grid()
        self._order = ''

        self.input_move = Tk.Entry(self._root, width=110)
        self.input_move.bind("<Return>", self.enter_order)
        self.input_move.grid(row=1)
        # self._root.after(500, self.tick)

        PHOTOS['Aeroflot'] = Tk.PhotoImage(file='logos/aeroflot.gif')
        PHOTOS['Air India'] = Tk.PhotoImage(file='logos/air india.gif')
        PHOTOS['All Nippon'] = Tk.PhotoImage(file='logos/all nippon.gif')
        PHOTOS['Cathay'] = Tk.PhotoImage(file='logos/cathay.gif')
        PHOTOS['China Eastern'] = Tk.PhotoImage(file='logos/china eastern.gif')
        PHOTOS['China Southern'] = Tk.PhotoImage(file='logos/china southern.gif')
        PHOTOS['Dynasty'] = Tk.PhotoImage(file='logos/dynasty.gif')
        PHOTOS['Emirates'] = Tk.PhotoImage(file='logos/emirates.gif')
        PHOTOS['FedEx Express'] = Tk.PhotoImage(file='logos/fedex express.gif')
        PHOTOS['Lufthansa'] = Tk.PhotoImage(file='logos/lufthansa.gif')
        PHOTOS['Qantas'] = Tk.PhotoImage(file='logos/qantas.gif')
        PHOTOS['United'] = Tk.PhotoImage(file='logos/united.gif')
        PHOTOS['UPS'] = Tk.PhotoImage(file='logos/ups.gif')
        bg = Tk.PhotoImage(file='logos/background.gif')

        self._frame.create_image(402, 20, image=bg)
        self._frame.create_line(*self._airport.get_runway(), width=4, fill='white')
        self._frame.create_text(self._airport.get_runway()[0]-8, self._airport.get_runway()[1]-8, text='13', fill='white')
        self._frame.create_text(self._airport.get_runway()[2]+8, self._airport.get_runway()[3]+8, text='31', fill='white')
        self._frame.create_line(0, 40, 803, 40, width=5)
        self._frame.create_line(210, 40, 210, 693, width=5)
        self._frame.create_text(130, 20, text=kaitak.__doc__, fill='white')
        self._frame.create_rectangle(0, 690, 800, 720, fill='black')
        self._count = 0

        self.tick()
        self._root.mainloop()

    def tick(self):
        if self._order == "":
            if self._count == 20:
                sound_text = self._airport.new_arrival_plane()
                self._frame.delete('radio')
                greet = random.choice(kaitak.greetings)
                sound.male_report(greet+sound_text[1]+' '.join(list(str(sound_text[2]))))
                self.radio_draw(sound_text[0]+str(sound_text[2])+': '+greet+sound_text[1]+str(sound_text[2]))
                # self._count = 0

        self._airport.update()
        self.ord_draw(self._frame)
        self._root.after(500, self.tick)
        self._count += 1

    def solve(self):
        new_puzzle = self._puzzle.clone()
        self.order = new_puzzle.solve_puzzle()

    def print_moves(self):
        print self._current_moves
        self._current_moves = ""

    def enter_order(self, event):
        raw_order = self.input_move.get()
        order = raw_order.split()
        sound.male_report_clean(' '.join(list(order[0]))+', '+ORDERS[order[1].lower()]+(' '.join(list(order[2]))))
        self.radio_draw('Ground: '+order[0]+', '+ORDERS[order[1].lower()]+order[2]+'.')
        self._airport.control_plane(*order)
        self.input_move.delete(0, 100)

    def radio_draw(self, attention):
        self._frame.delete('radio')
        self._frame.create_text(400, 705, text=attention, fill='white', tags='radio')

    def ord_draw(self, canvas):
        canvas.delete('temp')
        canvas.create_text(780, 20, text=time.strftime('%H:%M', time.localtime()), fill='white', tags='temp')

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
            canvas.create_text(place[0]-30, place[1]-15, text=plane.get_number()+'\n'+str(plane.get_height()/100)+' '+str(plane.get_speed()), fill='white', tags='temp')
