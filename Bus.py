import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

import sys

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True

import secGUI_support
  
def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root
    root = tk.Tk()
    secGUI_support.set_Tk_var()
    top = Toplevel1 (root)
    secGUI_support.init(root, top)
    root.mainloop()

w = None
def create_Toplevel1(root, *args, **kwargs):
    '''Starting point when module is imported by another program.'''
    global w, w_win, rt
    rt = root
    w = tk.Toplevel (root)
    secGUI_support.set_Tk_var()
    top = Toplevel1 (w)
    secGUI_support.init(w, top, *args, **kwargs)
    return (w, top)

def destroy_Toplevel1():
    global w
    w.destroy()
    w = None

class Toplevel1:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#d9d9d9' # X11 color: 'gray85'
        font10 = "-family Constantia -size 22 -weight bold -slant "  \
            "roman -underline 0 -overstrike 0"
        font11 = "-family Arial -size 14 -weight normal -slant roman "  \
            "-underline 0 -overstrike 0"
        font14 = "-family {Comic Sans MS} -size 17 -weight bold -slant"  \
            " italic -underline 0 -overstrike 0"
        font15 = "-family Arial -size 11 -weight normal -slant roman "  \
            "-underline 0 -overstrike 0"
        font16 = "-family {Franklin Gothic Medium} -size 13 -weight "  \
            "bold -slant roman -underline 0 -overstrike 0"
        font23 = "-family Impact -size 24 -weight bold -slant roman "  \
            "-underline 0 -overstrike 0"
        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')
        self.style.configure('.',background=_bgcolor)
        self.style.configure('.',foreground=_fgcolor)
        self.style.configure('.',font="TkDefaultFont")
        self.style.map('.',background=
            [('selected', _compcolor), ('active',_ana2color)])

        top.geometry("949x794+528+98")
        top.title("MASTERCHEF's Food for Weather")
        top.configure(background="#dbfeff")

        self.Frame1 = tk.Frame(top)
        self.Frame1.place(relx=0.021, rely=0.239, relheight=0.435, relwidth=0.69)

        self.Frame1.configure(relief='groove')
        self.Frame1.configure(borderwidth="2")
        self.Frame1.configure(relief='groove')
        self.Frame1.configure(background="#070707")
        self.Frame1.configure(width=655)

        self.Label1 = tk.Label(self.Frame1)
        self.Label1.place(relx=0.015, rely=0.029, height=36, width=362)
        self.Label1.configure(background="#0f0103")
        self.Label1.configure(disabledforeground="#a3a3a3")
        self.Label1.configure(font=font10)
        self.Label1.configure(foreground="#f7eca5")
        self.Label1.configure(text='''Bus Display''')
        self.Label1.configure(width=362)

        self.Listbox1 = tk.Listbox(self.Frame1)
        self.Listbox1.place(relx=0.031, rely=0.203, relheight=0.719
                , relwidth=0.51)
        self.Listbox1.configure(background="#ffffd6")
        self.Listbox1.configure(disabledforeground="#a3a3a3")
        self.Listbox1.configure(font=font11)
        self.Listbox1.configure(foreground="#000000")
        self.Listbox1.configure(width=334)
        z=bus()
        self.Listbox1.insert(1,''.join(z))

def bus():
  # Use a service account
  cred = credentials.Certificate('pragmatic-star-266013-ce5923bb9343.json')
  firebase_admin.initialize_app(cred)

  db = firestore.client()
  dbV = firestore.client()

  #################################### GET AMBULANCE LOCATION ############################
  users_ref = db.collection(u'amb')
  docs = users_ref.stream()
  for doc in docs:
    pass
  lat=doc.to_dict()['location'].latitude
  longi=doc.to_dict()['location'].longitude



  long_amb = round(longi,4)
  lat_amb = round(lat,4)

  #################################### GET HOSPITAL LOCATION ############################

  users_ref = db.collection(u'amb')
  docs = users_ref.stream()
  for doc in docs:
    pass
  lat=doc.to_dict()['dest'].latitude
  longi=doc.to_dict()['dest'].longitude


  hospital_long = round(longi,4)
  hospital_lat = round(lat,4)

  #################################### GET CORDINATES OF WAY ############################

  import googlemaps
  from datetime import datetime
  import polyline
  def lat(a,b):
      gmaps = googlemaps.Client(key='AIzaSyAZQl0TRenJIoCbKNjDKmT2LN9Y94um9qs')
      now = datetime.now()
      directions_result = gmaps.directions(a, b,
                                           mode="driving",
                                           departure_time=now)
      final=list()
      for i in directions_result:
          #print(i.keys())
         # print(i['legs'])
          for j in i['legs']:
              #print(j.keys())
              for k in j['steps']:
                  final.append(k['polyline'])
      
      finall=[]
      for p in final:
          #print(p)
          #print(p['points'])
          finall.extend(polyline.decode(p['points']))
      finall=[(round(item[0],4),round(item[1],4))for item in finall]
      return finall

  a = list(lat((lat_amb,long_amb),(hospital_lat,hospital_long)))

  #################################### GET BUS LOCATION ############################

  bus_locationusers_ref = dbV.collection(u'vehicle')
  docs = bus_locationusers_ref.stream()
  for doc in docs:
    if doc.id == 'nOLmedqY6oSVJadY7eIKlYYQR9T2':
      lat_bus=(doc.to_dict()['point'].latitude)
      long_bus=(doc.to_dict()['point'].longitude)

  #################################### CALCULATE DISTANCE BETWEEN BUS AND AMBULANCE ############################

  from math import radians, sin, cos, acos

  slat = radians(float(lat_amb))
  slon = radians(float(long_amb))
  elat = radians(float(lat_bus))
  elon = radians(float(long_bus))

  dist = 6371.01 * acos(sin(slat)*sin(elat) + cos(slat)*cos(elat)*cos(slon - elon))
  dist

  #################################### PRINTS ############################
  final="--- Bus Route ---"
  if (lat_bus, long_bus) in a and dist <= 3:#(lat_bus, long_bus),a[0]
    final="Emergency Vehicle Approaching"
  return final


if __name__ == '__main__':
    vp_start_gui()
