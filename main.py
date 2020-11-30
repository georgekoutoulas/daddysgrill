import kivy
import sqlite3 as sql
import math
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.checkbox import CheckBox
from kivy.properties import ObjectProperty, StringProperty, ListProperty
from kivy.uix.popup import Popup
from kivy.uix.dropdown import DropDown

kivy.require('1.11.1') # replace with your current kivy version !
kv = Builder.load_file("daddysgrill.kv")
    


class MainScreen(Screen):
    add_new_order = ObjectProperty(False)

    def insert_data(self):
        
        con = sql.connect("C:\\Users\\Flok1\\Desktop\\KIvy_projects\\DaddysGrill.db")
        con.execute("PRAGMA foreign_keys = ON")
        con.commit()
        cur = con.cursor()
        cur.execute(""" INSERT INTO pelates (epwnumo) VALUES (?)""",
                    (self.add_new_order.epwnumo,) )
        con.commit()
        con.close()    


class MenuScreen(Screen):
    category = ObjectProperty(False)
    name = ObjectProperty(False)
    btn = ObjectProperty(False)

    def delete_pelati_if_back(self):
        con = sql.connect("C:\\Users\\Flok1\\Desktop\\KIvy_projects\\DaddysGrill.db")
        cur = con.cursor()
        cur.execute("""DELETE FROM pelates WHERE idpelati = (SELECT MAX(idpelati) FROM pelates)""")
        con.commit()
        con.close()

    def print_on_screen_paraggelia(self):
        
        con = sql.connect("C:\\Users\\Flok1\\Desktop\\KIvy_projects\\DaddysGrill.db")
        cur = con.cursor()
        cur.execute("""SELECT category, name, ulika, amount, price FROM paraggelia 
                       WHERE idpelati = (SELECT MAX(idpelati) FROM paraggelia)""")
        last_data = cur.fetchall()
        con.commit()
        con.close()
        # for category, name, ulika, amount, price in last_data:
        #     print("",category, ":\n",name, "\n", ulika,"\t x ", amount, "",price,"€\n\n")
        for i in last_data:
            for j in i:
                self.add_widget(Button(text=i[0]))
                self.add_widget(Button(text=i[1]))
 

class OrektikaScreen(Screen):

    patates = ObjectProperty(False)
    patates_me_turi = ObjectProperty(False)
    tzatziki = ObjectProperty(False)
    feta = ObjectProperty(False)
    sws_giaourti_mikri = ObjectProperty(False)
    sws_giaourti_megali = ObjectProperty(False)
    sws_moustarda_mikri = ObjectProperty(False)
    sws_moustarda_megali = ObjectProperty(False)
    pita = ObjectProperty(False)
    
    

    def insert_data(self):

        self.orektika_data = (self.patates,self.patates_me_turi,self.tzatziki,
                              self.feta,self.sws_moustarda_mikri,self.sws_giaourti_megali,
                              self.sws_moustarda_mikri,self.sws_moustarda_megali, self.pita)

        for tx in self.orektika_data:
            if int(tx.text) > 0:
                con = sql.connect("C:\\Users\\Flok1\\Desktop\\KIvy_projects\\DaddysGrill.db")
                cur = con.cursor()
                cur.execute(""" INSERT INTO paraggelia (name, price, amount, category) VALUES (?,?,?,?)""",
                            (tx.name, tx.price, tx.amount, tx.category) )
                cur.execute("""UPDATE paraggelia SET idpelati = (SELECT idpelati FROM pelates WHERE idpelati = (SELECT MAX(idpelati) FROM pelates)) 
                               WHERE idparaggelias = (SELECT MAX(idparaggelias) FROM paraggelia)""")
                con.commit()
                con.close() 

        con = sql.connect("C:\\Users\\Flok1\\Desktop\\KIvy_projects\\DaddysGrill.db")
        cur = con.cursor()
        cur.execute("""SELECT category, name, ulika, amount, price FROM paraggelia 
                       WHERE idpelati = (SELECT MAX(idpelati) FROM paraggelia)""") 
        last_data = cur.fetchall()
        print(last_data)
        for i in last_data:
            for j in i:
                print(j)
       

class SalatesScreen(Screen):
    xwriatiki = ObjectProperty(False)
    caesars = ObjectProperty(False)
    xwr_ulika_button = ObjectProperty(False)

    def insert_data(self):
        
        self.salates_data = (self.xwriatiki, self.caesars)

        for tx in self.salates_data:
            if int(tx.text) > 0 and self.xwr_ulika_button.value == 0:

                con = sql.connect("C:\\Users\\Flok1\\Desktop\\KIvy_projects\\DaddysGrill.db")
                cur = con.cursor()
                cur.execute(""" INSERT INTO paraggelia (name, price, amount, ulika, category) VALUES (?,?,?,?,?)""",
                            (tx.name, tx.price, tx.amount, tx.ulika, tx.category) )
                cur.execute("""UPDATE paraggelia SET idpelati = (SELECT idpelati FROM pelates WHERE idpelati = (SELECT MAX(idpelati) FROM pelates)) 
                               WHERE idparaggelias = (SELECT MAX(idparaggelias) FROM paraggelia)""")
                con.commit()
                con.close()

        con = sql.connect("C:\\Users\\Flok1\\Desktop\\KIvy_projects\\DaddysGrill.db")
        cur = con.cursor()
        cur.execute("""SELECT category, name, ulika, amount, price FROM paraggelia 
                       WHERE idpelati = (SELECT MAX(idpelati) FROM paraggelia)""") 
        last_data = cur.fetchall()
        print(last_data)

    
    def show_popup(self):
        show = PosothtaPopupScreen()
        popupWindow = Popup(title="Επιλογή ποσότητας", content=show, size_hint=(0.4, 0.4))
        popupWindow.open()
            

class XwriatikiYlikaScreen(Screen):

    xwr_ulika_ntomata = ObjectProperty(False)
    xwr_ulika_aggouri = ObjectProperty(False)
    xwr_ulika_kremmudi = ObjectProperty(False)
    xwr_ulika_piperia = ObjectProperty(False)
    xwr_ulika_elies = ObjectProperty(False)
    

    def insert_data(self):
        
        self.xwr_ulika_state = (self.xwr_ulika_ntomata, self.xwr_ulika_aggouri, self.xwr_ulika_kremmudi, self.xwr_ulika_piperia, self.xwr_ulika_elies)
        self.xwr_ulika = []
        for st in self.xwr_ulika_state: 
            if st.state == 'down':
                self.xwr_ulika.append(st.text)
        
        con = sql.connect("C:\\Users\\Flok1\\Desktop\\KIvy_projects\\DaddysGrill.db")
        con.execute("PRAGMA foreign_keys = ON")
        cur = con.cursor()
        cur.execute("""UPDATE paraggelia SET ulika = ? WHERE idparaggelias = (SELECT MAX(idparaggelias) FROM paraggelia);""", [','.join(self.xwr_ulika)])
        con.commit()
        con.close()
        

class CaesarsYlikaScreen(Screen):
    pass

class KalamakiaScreen(Screen):

    kalamaki_xoirino = ObjectProperty(False)
    kalamaki_kotopoulo = ObjectProperty(False)
    kalamaki_kempap = ObjectProperty(False)
    kalamaki_loukaniko = ObjectProperty(False)
    kalamaki_kotompeikon = ObjectProperty(False)
    kalamaki_mpifteki_gemisto = ObjectProperty(False)

    def insert_data(self):

        self.kalamakia_data = (self.kalamaki_xoirino, self.kalamaki_kotopoulo,
                               self.kalamaki_kempap, self.kalamaki_loukaniko,
                               self.kalamaki_kotompeikon, self.kalamaki_mpifteki_gemisto)

        for tx in self.kalamakia_data:
            if int(tx.text) > 0:

                con = sql.connect("C:\\Users\\Flok1\\Desktop\\KIvy_projects\\DaddysGrill.db")
                cur = con.cursor()
                cur.execute(""" INSERT INTO paraggelia (name, price, amount, category) VALUES (?,?,?,?)""",
                            (tx.name, tx.price, tx.amount, tx.category) )
                cur.execute("""UPDATE paraggelia SET idpelati = (SELECT idpelati FROM pelates WHERE idpelati = (SELECT MAX(idpelati) FROM pelates)) 
                               WHERE idparaggelias = (SELECT MAX(idparaggelias) FROM paraggelia)""")
                con.commit()
                con.close()


class TulixtaScreen(Screen):

    guros_xoirino = ObjectProperty(False)
    guros_kotopoulo = ObjectProperty(False)
    guros_kalamaki_xoirino = ObjectProperty(False)
    guros_kalamaki_kotopoulo = ObjectProperty(False)
    guros_kotompeikon = ObjectProperty(False)
    guros_loukaniko = ObjectProperty(False)
    guros_kempap = ObjectProperty(False)
    guros_mpifteki_gemisto = ObjectProperty(False)

    tul_ulika_btn_guros_xoirino = ObjectProperty(False)
    tul_ulika_btn_guros_kotopoulo = ObjectProperty(False)
    tul_ulika_btn_guros_kal_xoir = ObjectProperty(False)
    tul_ulika_btn_guros_kal_kot = ObjectProperty(False)
    tul_ulika_btn_guros_kotomp = ObjectProperty(False)
    tul_ulika_btn_guros_louk = ObjectProperty(False)
    tul_ulika_btn_guros_kempap = ObjectProperty(False)
    tul_ulika_btn_guros_mpift_gem = ObjectProperty(False)

    def insert_data(self):

        self.guros_data = (self.guros_xoirino, self.guros_kotopoulo, self.guros_kalamaki_xoirino,
                           self.guros_kalamaki_kotopoulo, self.guros_kotompeikon, self.guros_loukaniko,
                           self.guros_kempap, self.guros_mpifteki_gemisto)

        self.tul_ulika_btn = (self.tul_ulika_btn_guros_xoirino, self.tul_ulika_btn_guros_kotopoulo,
                              self.tul_ulika_btn_guros_kal_xoir, self.tul_ulika_btn_guros_kal_kot,
                              self.tul_ulika_btn_guros_kotomp, self.tul_ulika_btn_guros_louk,
                              self.tul_ulika_btn_guros_kempap, self.tul_ulika_btn_guros_mpift_gem)


        for tx, vl in zip(self.guros_data, self.tul_ulika_btn):
            if int(tx.text) > 0  and vl.value == 0: 
            
                con = sql.connect("C:\\Users\\Flok1\\Desktop\\KIvy_projects\\DaddysGrill.db")
                cur = con.cursor()
                cur.execute(""" INSERT INTO paraggelia (name, price, amount, category, ulika) VALUES (?,?,?,?,?)""",
                            (tx.name, tx.price, tx.amount, tx.category, tx.ulika) )
                cur.execute("""UPDATE paraggelia SET idpelati = (SELECT idpelati FROM pelates WHERE idpelati = (SELECT MAX(idpelati) FROM pelates)) 
                               WHERE idparaggelias = (SELECT MAX(idparaggelias) FROM paraggelia)""")
                con.commit()
                con.close()


        self.tul_ulika_btn_guros_xoirino.value = 0
        self.tul_ulika_btn_guros_kotopoulo.value = 0
        self.tul_ulika_btn_guros_kal_xoir.value = 0
        self.tul_ulika_btn_guros_kal_kot.value = 0
        self.tul_ulika_btn_guros_kotomp.value = 0
        self.tul_ulika_btn_guros_louk.value = 0
        self.tul_ulika_btn_guros_kempap.value = 0
        self.tul_ulika_btn_guros_mpift_gem.value = 0     


    def show_popup(self):
        show = PosothtaPopupScreen()
        popupWindow = Popup(title="Επιλογή ποσότητας", content=show, size_hint=(0.4, 0.4))
        popupWindow.open()


    def insert_data_guros_xoirino(self):
        
        if int(self.guros_xoirino.text) > 0:
            con = sql.connect("C:\\Users\\Flok1\\Desktop\\KIvy_projects\\DaddysGrill.db")
            cur = con.cursor()
            cur.execute(""" INSERT INTO paraggelia (name, price, amount, category, ulika, insertulika) VALUES (?,?,?,?,?,?)""",
                        (self.guros_xoirino.name, self.guros_xoirino.price, self.guros_xoirino.amount, self.guros_xoirino.category,self.guros_xoirino.ulika, self.tul_ulika_btn_guros_xoirino.insert_ulika) )
            cur.execute("""UPDATE paraggelia SET idpelati = (SELECT idpelati FROM pelates WHERE idpelati = (SELECT MAX(idpelati) FROM pelates)) 
                           WHERE idparaggelias = (SELECT MAX(idparaggelias) FROM paraggelia)""")
            con.commit()
            con.close()

    def insert_data_guros_kotopoulo(self):

        if int(self.guros_kotopoulo.text) > 0:
            con = sql.connect("C:\\Users\\Flok1\\Desktop\\KIvy_projects\\DaddysGrill.db")
            cur = con.cursor()
            cur.execute(""" INSERT INTO paraggelia (name, price, amount, category, ulika, insertulika) VALUES (?,?,?,?,?,?)""",
                        (self.guros_kotopoulo.name, self.guros_kotopoulo.price, self.guros_kotopoulo.amount, self.guros_kotopoulo.category,self.guros_kotopoulo.ulika, self.tul_ulika_btn_guros_kotopoulo.insert_ulika) )
            cur.execute("""UPDATE paraggelia SET idpelati = (SELECT idpelati FROM pelates WHERE idpelati = (SELECT MAX(idpelati) FROM pelates)) 
                           WHERE idparaggelias = (SELECT MAX(idparaggelias) FROM paraggelia)""")
            con.commit()
            con.close()

    def insert_data_kalamaki_xoirino(self):

        if int(self.guros_kalamaki_xoirino.text) > 0:
            con = sql.connect("C:\\Users\\Flok1\\Desktop\\KIvy_projects\\DaddysGrill.db")
            cur = con.cursor()
            cur.execute(""" INSERT INTO paraggelia (name, price, amount, category, ulika, insertulika) VALUES (?,?,?,?,?,?)""",
                        (self.guros_kalamaki_xoirino.name, self.guros_kalamaki_xoirino.price, self.guros_kalamaki_xoirino.amount, self.guros_kalamaki_xoirino.category,self.guros_kalamaki_xoirino.ulika, self.tul_ulika_btn_guros_kal_xoir.insert_ulika) )
            cur.execute("""UPDATE paraggelia SET idpelati = (SELECT idpelati FROM pelates WHERE idpelati = (SELECT MAX(idpelati) FROM pelates)) 
                           WHERE idparaggelias = (SELECT MAX(idparaggelias) FROM paraggelia)""")
            con.commit()
            con.close()

    def insert_data_kalamaki_kotopoulo(self):

        if int(self.guros_kalamaki_kotopoulo.text) > 0:
            con = sql.connect("C:\\Users\\Flok1\\Desktop\\KIvy_projects\\DaddysGrill.db")
            cur = con.cursor()
            cur.execute(""" INSERT INTO paraggelia (name, price, amount, category, ulika, insertulika) VALUES (?,?,?,?,?,?)""",
                        (self.guros_kalamaki_kotopoulo.name, self.guros_kalamaki_kotopoulo.price, self.guros_kalamaki_kotopoulo.amount, self.guros_kalamaki_kotopoulo.category,self.guros_kalamaki_kotopoulo.ulika, self.tul_ulika_btn_guros_kal_kot.insert_ulika) )
            cur.execute("""UPDATE paraggelia SET idpelati = (SELECT idpelati FROM pelates WHERE idpelati = (SELECT MAX(idpelati) FROM pelates)) 
                           WHERE idparaggelias = (SELECT MAX(idparaggelias) FROM paraggelia)""")
            con.commit()
            con.close()

    def insert_data_kotompeikon(self):

        if int(self.guros_kotompeikon.text) > 0:
            con = sql.connect("C:\\Users\\Flok1\\Desktop\\KIvy_projects\\DaddysGrill.db")
            cur = con.cursor()
            cur.execute(""" INSERT INTO paraggelia (name, price, amount, category, ulika, insertulika) VALUES (?,?,?,?,?,?)""",
                        (self.guros_kotompeikon.name, self.guros_kotompeikon.price, self.guros_kotompeikon.amount, self.guros_kotompeikon.category,self.guros_kotompeikon.ulika, self.tul_ulika_btn_guros_kotomp.insert_ulika) )
            cur.execute("""UPDATE paraggelia SET idpelati = (SELECT idpelati FROM pelates WHERE idpelati = (SELECT MAX(idpelati) FROM pelates)) 
                           WHERE idparaggelias = (SELECT MAX(idparaggelias) FROM paraggelia)""")
            con.commit()
            con.close()

    def insert_data_loukaniko(self):

        if int(self.guros_loukaniko.text) > 0:
            con = sql.connect("C:\\Users\\Flok1\\Desktop\\KIvy_projects\\DaddysGrill.db")
            cur = con.cursor()
            cur.execute(""" INSERT INTO paraggelia (name, price, amount, category, ulika, insertulika) VALUES (?,?,?,?,?,?)""",
                        (self.guros_loukaniko.name, self.guros_loukaniko.price, self.guros_loukaniko.amount, self.guros_loukaniko.category,self.guros_loukaniko.ulika, self.tul_ulika_btn_guros_louk.insert_ulika) )
            cur.execute("""UPDATE paraggelia SET idpelati = (SELECT idpelati FROM pelates WHERE idpelati = (SELECT MAX(idpelati) FROM pelates)) 
                           WHERE idparaggelias = (SELECT MAX(idparaggelias) FROM paraggelia)""")
            con.commit()
            con.close()

    def insert_data_kempap(self):

        if int(self.guros_kempap.text) > 0:
            con = sql.connect("C:\\Users\\Flok1\\Desktop\\KIvy_projects\\DaddysGrill.db")
            cur = con.cursor()
            cur.execute(""" INSERT INTO paraggelia (name, price, amount, category, ulika, insertulika) VALUES (?,?,?,?,?,?)""",
                        (self.guros_kempap.name, self.guros_kempap.price, self.guros_kempap.amount, self.guros_kempap.category,self.guros_kempap.ulika, self.tul_ulika_btn_guros_kempap.insert_ulika) )
            cur.execute("""UPDATE paraggelia SET idpelati = (SELECT idpelati FROM pelates WHERE idpelati = (SELECT MAX(idpelati) FROM pelates)) 
                           WHERE idparaggelias = (SELECT MAX(idparaggelias) FROM paraggelia)""")
            con.commit()
            con.close()

    def insert_data_mpifteki_gemisto(self):

        if int(self.guros_mpifteki_gemisto.text) > 0:
            con = sql.connect("C:\\Users\\Flok1\\Desktop\\KIvy_projects\\DaddysGrill.db")
            cur = con.cursor()
            cur.execute(""" INSERT INTO paraggelia (name, price, amount, category, ulika, insertulika) VALUES (?,?,?,?,?,?)""",
                        (self.guros_mpifteki_gemisto.name, self.guros_mpifteki_gemisto.price, self.guros_mpifteki_gemisto.amount, self.guros_mpifteki_gemisto.category,self.guros_mpifteki_gemisto.ulika, self.tul_ulika_btn_guros_mpift_gem.insert_ulika) )
            cur.execute("""UPDATE paraggelia SET idpelati = (SELECT idpelati FROM pelates WHERE idpelati = (SELECT MAX(idpelati) FROM pelates)) 
                           WHERE idparaggelias = (SELECT MAX(idparaggelias) FROM paraggelia)""")
            con.commit()
            con.close()


class TulixtaYlikaScreen(Screen):

    tul_ulika_patates = ObjectProperty(False)
    tul_ulika_ntomata = ObjectProperty(False)
    tul_ulika_kremmudi = ObjectProperty(False)
    tul_ulika_marouli = ObjectProperty(False)
    tul_ulika_tzatziki = ObjectProperty(False)
    tul_ulika_moustarda = ObjectProperty(False)
    tul_ulika_ketsap = ObjectProperty(False)
    tul_ulika_sws_moustarda = ObjectProperty(False)
    tul_ulika_sws_giaourti = ObjectProperty(False)
    tul_ulika_paprika = ObjectProperty(False)
    tul_ulika_paprika_kauteri = ObjectProperty(False)
    tul_ulika_pita_kanoniki = ObjectProperty(False)
    tul_ulika_pita_olikis = ObjectProperty(False)
    tul_ulika_pita_kalampokiou = ObjectProperty(False)
    tul_ulika_2pita_kanoniki = ObjectProperty(False)
    tul_ulika_2pita_olikis = ObjectProperty(False)
    tul_ulika_2pita_kalampokiou = ObjectProperty(False)

    def insert_data(self):
        
        self.tul_ulika_state = (self.tul_ulika_patates, self.tul_ulika_ntomata, self.tul_ulika_kremmudi, 
                                self.tul_ulika_marouli, self.tul_ulika_tzatziki, self.tul_ulika_moustarda,
                                self.tul_ulika_ketsap, self.tul_ulika_sws_moustarda, self.tul_ulika_sws_giaourti,
                                self.tul_ulika_paprika, self.tul_ulika_paprika_kauteri, self.tul_ulika_pita_kanoniki,
                                self.tul_ulika_pita_olikis, self.tul_ulika_pita_kalampokiou, self.tul_ulika_2pita_kanoniki,
                                self.tul_ulika_2pita_olikis, self.tul_ulika_2pita_kalampokiou)
        
        self.tul_ulika = []
    
        for st in self.tul_ulika_state: 
            if st.state == 'down':
                self.tul_ulika.append(st.text)
        
        con = sql.connect("C:\\Users\\Flok1\\Desktop\\KIvy_projects\\DaddysGrill.db")
        cur = con.cursor()
        #cur.execute("""SELECT insertulika FROM paraggelia WHERE insertulika = 1""")
        #cur.execute("""UPDATE paraggelia SET ulika = ? """, [','.join(self.tul_ulika)])
        cur.execute("""UPDATE paraggelia SET ulika= ?, insertulika = 0 WHERE idparaggelias = (SELECT MAX(idparaggelias) FROM paraggelia);""", [','.join(self.tul_ulika)])
        #cur.execute("""UPDATE paraggelia SET ulika = ? WHERE idparaggelias = (SELECT MAX(idparaggelias) FROM paraggelia);""", [','.join(self.tul_ulika)])
        con.commit()
        con.close()

    def delete_data(self):

        con = sql.connect("C:\\Users\\Flok1\\Desktop\\KIvy_projects\\DaddysGrill.db")
        cur = con.cursor()
        cur.execute("""DELETE FROM paraggelia WHERE idparaggelias = (SELECT MAX(idparaggelias) FROM paraggelia)""")
        con.commit()
        con.close()


class MeridesScreen(Screen):

    merida_guros_xoirino = ObjectProperty(False)
    merida_guros_kotopoulo = ObjectProperty(False)
    merida_kalamaki_xoirino = ObjectProperty(False)
    merida_kalamaki_kotopoulo = ObjectProperty(False)
    merida_kotompeikon = ObjectProperty(False)
    merida_loukaniko = ObjectProperty(False)
    merida_kempap = ObjectProperty(False)
    merida_mpifteki_gemisto = ObjectProperty(False)

    def insert_data(self):

        self.merides_data = (self.merida_guros_xoirino, self.merida_guros_kotopoulo,
                             self.merida_kalamaki_xoirino, self.merida_kalamaki_kotopoulo,
                             self.merida_kotompeikon, self.merida_loukaniko,
                             self.merida_kempap, self.merida_mpifteki_gemisto)

        for tx in self.merides_data:
            if int(tx.text) > 0:

                con = sql.connect("C:\\Users\\Flok1\\Desktop\\KIvy_projects\\DaddysGrill.db")
                cur = con.cursor()
                cur.execute(""" INSERT INTO paraggelia (name, price, amount, category) VALUES (?,?,?,?)""",
                            (tx.name, tx.price, tx.amount, tx.category ))
                cur.execute("""UPDATE paraggelia SET idpelati = (SELECT idpelati FROM pelates WHERE idpelati = (SELECT MAX(idpelati) FROM pelates)) 
                               WHERE idparaggelias = (SELECT MAX(idparaggelias) FROM paraggelia)""")
                con.commit()
                con.close()


class MeToKiloScreen(Screen):

    kilo_guros_xoirino = ObjectProperty(False)
    kilo_guros_kotopoulo = ObjectProperty(False)

    def insert_data(self):

        self.kilo_guros_data = (self.kilo_guros_xoirino, self.kilo_guros_kotopoulo)

        for tx in self.kilo_guros_data:
            if int(tx.text) > 0:
                con = sql.connect("C:\\Users\\Flok1\\Desktop\\KIvy_projects\\DaddysGrill.db")
                cur = con.cursor()
                cur.execute(""" INSERT INTO paraggelia (name, price, amount, category) VALUES (?,?,?,?)""",
                            (tx.name, tx.price, tx.amount, tx.category) )
                cur.execute("""UPDATE paraggelia SET idpelati = (SELECT idpelati FROM pelates WHERE idpelati = (SELECT MAX(idpelati) FROM pelates)) 
                               WHERE idparaggelias = (SELECT MAX(idparaggelias) FROM paraggelia)""")
                con.commit()
                con.close()


class GurosClubScreen(Screen):

    guros_club = ObjectProperty(False)

    def insert_data(self):
        
        if int(self.guros_club.text) > 0:
            con = sql.connect("C:\\Users\\Flok1\\Desktop\\KIvy_projects\\DaddysGrill.db")
            cur = con.cursor()
            cur.execute(""" INSERT INTO paraggelia (name, price, amount, category) VALUES (?,?,?,?)""",
                        (self.guros_club.name, self.guros_club.price, self.guros_club.amount, self.guros_club.category) )
            cur.execute("""UPDATE paraggelia SET idpelati = (SELECT idpelati FROM pelates WHERE idpelati = (SELECT MAX(idpelati) FROM pelates)) 
                           WHERE idparaggelias = (SELECT MAX(idparaggelias) FROM paraggelia)""")
            con.commit()
            con.close()


class PoikiliesScreen(Screen):

    poikilia_mikri = ObjectProperty(False)
    poikilia_megali = ObjectProperty(False)


    def insert_data(self):
        self.poikilia_data = (self.poikilia_mikri, self.poikilia_megali)

        for tx in self.poikilia_data:
            if int(tx.text) > 0:
                con = sql.connect("C:\\Users\\Flok1\\Desktop\\KIvy_projects\\DaddysGrill.db")
                cur = con.cursor()
                cur.execute(""" INSERT INTO paraggelia (name, price, amount, category) VALUES (?,?,?,?)""",
                            (tx.name, tx.price, tx.amount, tx.category) )
                cur.execute("""UPDATE paraggelia SET idpelati = (SELECT idpelati FROM pelates WHERE idpelati = (SELECT MAX(idpelati) FROM pelates)) 
                               WHERE idparaggelias = (SELECT MAX(idparaggelias) FROM paraggelia)""")
                con.commit()
                con.close()


class AnapsuktikaScreen(Screen):

    coca_cola_330 = ObjectProperty(False)
    coca_cola_500 = ObjectProperty(False)
    coca_cola_1500 = ObjectProperty(False)
    coca_cola_zero_330 = ObjectProperty(False)
    coca_cola_zero_500 = ObjectProperty(False)
    coca_cola_zero_1500 = ObjectProperty(False)
    coca_cola_light_330 = ObjectProperty(False)
    coca_cola_light_500 = ObjectProperty(False)
    coca_cola_light_1500 = ObjectProperty(False)
    sprite_330 = ObjectProperty(False)
    fanta_330 = ObjectProperty(False)
    soda_330 = ObjectProperty(False)
    amstel_330 = ObjectProperty(False)
    alpha_330 = ObjectProperty(False)
    heineken_330 = ObjectProperty(False)
    fix_330 = ObjectProperty(False)
    nero_500 = ObjectProperty(False)
    nero_1500 = ObjectProperty(False)
    krasi_1500 = ObjectProperty(False)

    def insert_data(self):

        self.pota_anapsuktika_data = (self.coca_cola_330, self.coca_cola_500, self.coca_cola_1500,
                                      self.coca_cola_zero_330, self.coca_cola_zero_500, self.coca_cola_zero_1500,
                                      self.coca_cola_light_330, self.coca_cola_light_500, self.coca_cola_light_1500,
                                      self.sprite_330, self.fanta_330, self.soda_330, self.amstel_330, self.alpha_330,
                                      self.heineken_330, self.fix_330, self.nero_500, self.nero_1500, self.krasi_1500)

        for tx in self.pota_anapsuktika_data:
            if int(tx.text) > 0:
                con = sql.connect("C:\\Users\\Flok1\\Desktop\\KIvy_projects\\DaddysGrill.db")
                cur = con.cursor()
                cur.execute(""" INSERT INTO paraggelia (name, price, amount, category) VALUES (?,?,?,?)""",
                            (tx.name, tx.price, tx.amount, tx.category) )
                cur.execute("""UPDATE paraggelia SET idpelati = (SELECT idpelati FROM pelates WHERE idpelati = (SELECT MAX(idpelati) FROM pelates)) 
                               WHERE idparaggelias = (SELECT MAX(idparaggelias) FROM paraggelia)""")
                con.commit()
                con.close()


class PosothtaPopupScreen(Screen):
    pass

menuscreen = MenuScreen()

# Create the screen manager
sm = ScreenManager()
sm.add_widget(MainScreen(name='main'))
sm.add_widget(MenuScreen(name='menu'))
sm.add_widget(OrektikaScreen(name='orektika'))
sm.add_widget(SalatesScreen(name='salates'))
sm.add_widget(XwriatikiYlikaScreen(name='xwriatiki_ulika'))
sm.add_widget(CaesarsYlikaScreen(name='caesars_ulika'))
sm.add_widget(KalamakiaScreen(name='kalamakia'))
sm.add_widget(TulixtaScreen(name='tulixta'))
sm.add_widget(TulixtaYlikaScreen(name='tulixta_ulika'))
sm.add_widget(MeridesScreen(name='merides'))
sm.add_widget(MeToKiloScreen(name='metokilo'))
sm.add_widget(GurosClubScreen(name='gurosclub'))
sm.add_widget(PoikiliesScreen(name='poikilies'))
sm.add_widget(AnapsuktikaScreen(name='pota_anapsuktika'))

class MyApp(App):
    def build(self):
        return sm

    title = "Daddy's Grill"

    # def print_on_screen_paraggelia(self):
        
    #     con = sql.connect("C:\\Users\\Flok1\\Desktop\\KIvy_projects\\DaddysGrill.db")
    #     cur = con.cursor()
    #     cur.execute("""SELECT category, name, ulika, amount, price FROM paraggelia 
    #                    WHERE idpelati = (SELECT MAX(idpelati) FROM paraggelia)""")
    #     last_data = cur.fetchall()
    #     con.commit()
    #     con.close()
        
    #     for i in last_data:
    #         category = str(last_data[0])
    #         name = str(last_data[1])
    #         return category 

if __name__ == '__main__':
    MyApp().run()