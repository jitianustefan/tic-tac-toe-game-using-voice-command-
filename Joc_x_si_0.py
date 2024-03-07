# -*- coding: utf-8 -*-
"""
Created on Sat Dec 23 16:44:09 2023

@author: jitia
"""
# import module necesare aplicatiei
from tkinter import Tk, Button, Text, Scrollbar,StringVar,END,Label,WORD
from tkinter import messagebox, ttk
import speech_recognition as sr
import numpy as np
import time
from gtts import gTTS
import pygame

#instanta fereastra principala
window = Tk()
#adaugare titlu interfata 
window.title("X și 0")
#variabile pentru numele jucatorilor
jucator_1 = StringVar()
jucator_2 = StringVar()
#matricea initializata cu 4 pe baza careia verific castigatorul 
m = np.array([ [4,4,4], [4,4,4], [4,4,4] ])

#functia de recunoastere a numelui in prima fereastra
def recunoastere_nume(variabila_jucator,eticheta, scena_joc):
    recunoastere = sr.Recognizer()
    with sr.Microphone() as source:
        recunoastere.adjust_for_ambient_noise(source)
        audio = recunoastere.listen(source,timeout = 5, phrase_time_limit=3)
    try:
        nume_jucator = recunoastere.recognize_google(audio, language="ro-RO")
        
        print(f"Ati spus: {nume_jucator}")
        variabila_jucator.set(nume_jucator)
        eticheta.delete('1.0', 'end')

        # Adaugă noul text
        eticheta.config(state="normal")
        eticheta.delete("1.0", "end-1c")
        eticheta.insert('1.0', str(nume_jucator))
        eticheta.config(state="disabled")
        # Actualizare interfață grafică

    except sr.UnknownValueError:
        print(f"Recunoașterea vocii a eșuat. Vă rugăm să încercați din nou.")
       
        scena_joc.config(state = "normal")
       
        scena_joc.insert(END, f"Recunoașterea numelui a eșuat. Apăsați butonul pentru a încerca din nou.\n")
        scena_joc.see(END) 
        scena_joc.config(state = "disabled")
    except sr.RequestError as e:
        print(f"Eroare la cerere pentru recunoaștere vocală; {e}")
        

def afiseaza_tabel():
    print(f"Nume jucator x: {jucator_1.get()}, nume jucator 0: {jucator_2.get()}")
    global semn
    
    #verific daca am valori in variabilele pentru nume
    if not jucator_1.get() or not jucator_2.get():
        messagebox.showwarning("Avertisment", "Introduceți numele ambilor jucători!")
        return
    # verific daca valorile din variabilele de nume sunt diferite intre ele
    if jucator_1.get()== jucator_2.get() and jucator_1.get() !="" :
        messagebox.showwarning("Avertisment", "Introduceți nume de jucători diferite!")
        return
    
    # Șterge tot conținutul din fereastra actuală
    for widget in window.winfo_children():
        widget.destroy()
        
    #afiseaza widget-uri pentru fereastra alege ordinea    
    eticheta_ordine = Label(window, text=f'Cine este primul jucător ? \n {jucator_1.get()} sau {jucator_2.get()}', font=("Helvetica", 18, "bold"),bg="#99ccff")
    eticheta_ordine.grid(row=0, column=0, padx=10, pady=10)
    #chenarul pentru mesaje
    scena_joc = Text(window, height=10, width=40, wrap=WORD, font=("Helvetica", 10), bg="#e6f7ff")
    scena_joc.grid(row=7, column=0, columnspan=3, padx=10, pady=10) 
    
    #apelez functia in care se alege ordinea
    window.after(100,lambda: alege_ordinea(scena_joc))
      
def alege_ordinea(scena_joc):
    #setez culoarea fundalului 
    window.config(bg="#e6f7ff")
    global semn

    recunoastere = sr.Recognizer()
    #context pentru utilizarea microfonului. Toate operatiile de recunoastrere vocala vor avea loc in interiorul acestui context.
    with sr.Microphone() as source:
        recunoastere.adjust_for_ambient_noise(source)
        audio = recunoastere.listen(source)
    try:
        #salvez valoarea de la microfon in variabila ordine_jucator
        ordine_jucator = recunoastere.recognize_google(audio, language="ro-RO")
        print(f"Ati spus primul jucator este: {ordine_jucator}")
        if ordine_jucator == jucator_1.get():
            print(f"primul jucator este {jucator_1.get()}")
            semn = "X"
        elif ordine_jucator == jucator_2.get():
            print(f"primul jucator este {jucator_2.get()}")
            semn = "O"
    #afisez in interfata mesajul in cazul in care recunoasterea vocala nu a avut succes
    except sr.UnknownValueError:
        scena_joc.insert(END, f"Recunoașterea vocii a eșuat. Vă rugăm să încercați din nou.\n")
        scena_joc.see(END) 
        print(f"Recunoașterea vocii a eșuat. Vă rugăm să încercați din nou.")
    except sr.RequestError as e:
        print(f"Eroare la cerere pentru recunoaștere vocală; {e}")
        
        
    print(f"Valoarea din semn este: {semn}")
    #verific starea de ordine a jucatorilor
    if semn == "neinitializat":
        window.after(100,lambda: alege_ordinea(scena_joc))
        print("Mai apelez o data ordinea")
    else:
         #afisez fereastra cu interfata pentru X si 0
         print("apelez etichetele pt ....")
         window.geometry("700x600")
         global eticheta_joc
         #sterg toate widget-urile
         for widget in window.winfo_children():
             widget.destroy()
         
         #in functie de randul jucatorului afisez un text cu randul carui jucator este
         if semn == 'O':
             eticheta_tura = Label(window, text=f'{jucator_2.get()} alege poziția',font=("Helvetica", 12, "bold"), bg="#99ccff")
             eticheta_tura.grid(row=0, column=0,columnspan=3, padx=10, pady=10)
             etichete_tura.append(eticheta_tura)
         else:
             eticheta_tura = Label(window, text=f'{jucator_1.get()} alege poziția',font=("Helvetica", 12, "bold"),bg="#99ccff")
             eticheta_tura.grid(row=0, column=0,columnspan=3, padx=10, pady=10)
             etichete_tura.append(eticheta_tura)
         #afisez indexii pentru coloane folosindu-ma de un for
         for i, litera in enumerate(['A', 'B', 'C']):
             eticheta_coloana = Label(window, text=litera, font=("Helvetica", 14, "bold"), bg="#e6f7ff")
             eticheta_coloana.grid(row=1, column=i + 1, padx=10, pady=10)
         #afisez indexii pentru randuri cu un for
         for i in range(1, 4):
             eticheta_rand = Label(window, text=str(i), font=("Helvetica", 14, "bold"),bg="#e6f7ff")
             eticheta_rand.grid(row=i + 1, column=0, padx=10)
         #afisez casutele in care se marcheaza X sau 0
         for i in range(1, 4):
             for j in range(1, 4):
                 eticheta_joc = Label(window, text='', width=10, height=2, relief='solid', borderwidth=1,font=("Helvetica", 18, "bold"),bg="#cce5ff")
                 eticheta_joc.grid(row=i + 1, column=j)
                 etichete_joc.append(eticheta_joc)
         #afisez chenarul pentru mesaje
         scena_joc = Text(window, height=10, width=40, wrap=WORD, font=("Helvetica", 10), bg="#e6f7ff")
         scena_joc.grid(row=7, column=1, columnspan=3, pady=10)
                    
         #apelez functia care preia coordonata de la microfon        
         window.after(100, lambda: comanda_vocala(scena_joc))  
        
# functia prin care citesc info si adaug info in fiecare patratica
def comanda_vocala(scena_joc):
    global semn, m
    recunoastere = sr.Recognizer()
    #context pentru utilizarea microfonului. 
    with sr.Microphone() as source:
        recunoastere.adjust_for_ambient_noise(source)
        audio = recunoastere.listen(source, phrase_time_limit=3)
    try:
        comanda = recunoastere.recognize_google(audio, language="ro-RO")
        #daca comanda a fost preluata de la microfon cu succes o trimit ca parametru functiei proceseaza_comanda
        print(f"Ati spus: {comanda}")
        proceseaza_comanda(comanda,scena_joc)

    except sr.UnknownValueError:
        #mesaj de eroare
        scena_joc.insert(END, f"Recunoașterea comenzii vocale a eșuat. Încearcă din nou.\n")
        scena_joc.see(END) 
        print(f"Recunoașterea comenzii vocale a eșuat. Vă rugăm să încercați din nou.")
    except sr.RequestError as e:
        print(f"Eroare la cerere pentru recunoaștere vocală; {e}")
     
    
    style = ttk.Style()
    style.configure("TButton", padding=6, relief="flat", background="#ccc")
    print(m)
    
    #verific starea jocului; Daca a castigat cineva sau este egalitate
    if not win_condition():
        window.after(100, lambda: comanda_vocala(scena_joc))
    elif win_condition() == "egalitate":
        etichete_tura[0].config(text='A câștigat prietenia !',bg="#e6f7ff")
        print("A castigat prietenia")
        mesaj_castig = f"A câștigat prietenia !"
        #apelez functia de anuntare la boxe a mesajului corespunzator
        window.after(1000, lambda: rostește_mesaj(mesaj_castig))
        #reinitializez variabilele
        jucator_1.set("")
        jucator_2.set("")
        for row in range(3):
            for element in range(3):
                m[row][element] = 4
        #intreb daca se mai doreste jucarea unei runde
        eticheta_restart = Label(window, text=f'Doriti sa mai jucati o data ?', font=("Helvetica", 12, "bold"),bg="#e6f7ff", foreground='red')
        eticheta_restart.grid(row=5, column=0,columnspan=3, pady=10)
        #afisez butoanele pentru restart si inchide joc
        buton_restart = ttk.Button(window, text='Restart ', command=inceput)
        buton_restart.grid(row = 6, column=0, padx= 50, pady=20)
        buton_inchidere = ttk.Button(window, text='Închide Joc', command=inchide_joc)
        buton_inchidere.grid(row = 6, column=1, pady=20)
    else:
        if semn == "X":
            print(f"A castigat jucatorul O")
            nume_jucator_castigator = jucator_1.get() if semn == "O" else jucator_2.get()
            etichete_tura[0].config(text=f"A câștigat {nume_jucator_castigator}",bg="#e6f7ff")
            print(f"A câștigat {nume_jucator_castigator}")
            #apelez functia de anuntare la boxe a mesajului corespunzator
            mesaj_castig = f"A câștigat {nume_jucator_castigator}"
            window.after(1000, lambda: rostește_mesaj(mesaj_castig))
            #reinitializez variabilele
            jucator_1.set("")
            jucator_2.set("")
            for row in range(3):
                for element in range(3):
                    m[row][element] = 4
            #intreb daca se mai doreste jucarea unei runde
            eticheta_restart = Label(window, text=f'Doriti sa mai jucati o data ?', font=("Helvetica", 12, "bold"),bg="#e6f7ff", foreground='red')
            eticheta_restart.grid(row=5, column=0,columnspan=3, pady=10)
            #afisez butoanele pentru restart si inchide joc
            buton_restart = ttk.Button(window, text='Restart', command=inceput)
            buton_restart.grid(row = 6, column=0, padx= 50, pady=20)
            buton_inchidere = ttk.Button(window, text='Închide Joc', command=inchide_joc)
            buton_inchidere.grid(row = 6, column=1, pady=20)
        else:
            nume_jucator_castigator = jucator_1.get() if semn == "O" else jucator_2.get()
            etichete_tura[0].config(text=f"A câștigat {nume_jucator_castigator}",bg="#e6f7ff")
            print(f"A câștigat {nume_jucator_castigator}")
            #apelez functia de anuntare la boxe a mesajului corespunzator
            mesaj_castig = f"A câștigat {nume_jucator_castigator}"
            window.after(1000, lambda: rostește_mesaj(mesaj_castig))
            print("A castigat jucatorul X")
            #reinitializez variabilele
            jucator_1.set("")
            jucator_2.set("")
            for row in range(3):
                for element in range(3):
                    m[row][element] = 4
            #intreb daca se mai doreste jucarea unei runde
            eticheta_restart = Label(window, text=f'Doriti sa mai jucati o data ?', font=("Helvetica", 12, "bold"),bg="#e6f7ff", foreground='red')
            eticheta_restart.grid(row=5, column=0,columnspan=3, pady=10)
            #afisez butoanele pentru restart si inchide joc
            buton_restart = ttk.Button(window, text='Restart', command=inceput)
            buton_restart.grid(row = 6, column=0, padx= 50, pady=20)
            buton_inchidere = ttk.Button(window, text='Închide Joc', command=inchide_joc)
            buton_inchidere.grid(row = 6, column=1, pady=20)
    
    
def proceseaza_comanda(comanda,scena_joc):
    global semn
    if comanda in ["unu A", "1A", "1a", "1 a", "a1", "A1","a 1"]:
        if m[0][0] == 4:
            print("Ești în 1A")
            functia_de_completare(semn, 0)
            if semn == 'O':
                    m[0][0]= 0
                    semn = "X"
                    etichete_tura[0].config(text=f'Este randul jucatorului {jucator_1.get()}')
            else:
                    
                    m[0][0]= 1
                    semn = "O"
                    etichete_tura[0].config(text=f'Este randul jucatorului {jucator_2.get()}')
        else:
            scena_joc.insert(END, f"Poziție deja ocupată\n")
            scena_joc.see(END) 
            print("Ati spus deja o pozitie ocupata incercati alta pozitie")
    elif comanda in ["unu B", "1B", "1b", "1 b", "B1"," b1", "b 1"]:
        if m[0][1] == 4:
            print("Ești în 1B")
            functia_de_completare(semn, 1)
            if semn == 'O':
                    m[0][1]= 0
                    semn = "X"
                    etichete_tura[0].config(text=f'Este rândul jucatorului {jucator_1.get()}')
            else:
                    m[0][1]= 1
                    semn = "O"
                    etichete_tura[0].config(text=f'Este randul jucatorului {jucator_2.get()}')
        else:
            scena_joc.insert(END, f"Poziție deja ocupată\n")
            scena_joc.see(END) 
            print("Ati spus deja o pozitie ocupata incercati alta pozitie")
    elif comanda in ["unu C", "1C", "1c", "unu c", "1 c","C1", "c 1", "c1"]:
        if m[0][2] == 4:
            print("Ești în 1C")
            functia_de_completare(semn, 2)
            if semn == 'O':
                    m[0][2]= 0
                    semn = "X"
                    etichete_tura[0].config(text=f'Este randul jucatorului {jucator_1.get()}')
            else:
                    m[0][2]= 1
                    semn = "O"
                    etichete_tura[0].config(text=f'Este randul jucatorului {jucator_2.get()}')
        else:
            scena_joc.insert(END, f"Poziție deja ocupată\n")
            scena_joc.see(END) 
            print("Ati spus deja o pozitie ocupata incercati alta pozitie")
    elif comanda in ["doi A", "2A", "2a", "2 a", "A2", "a2", "a 2"]:
        if m[1][0] == 4:
            print("Ești în 2A")
            functia_de_completare(semn, 3)
            if semn == 'O':
                    m[1][0]= 0
                    semn = "X"
                    etichete_tura[0].config(text=f'Este randul jucatorului {jucator_1.get()}')
            else:
                    m[1][0]= 1
                    semn = "O"
                    etichete_tura[0].config(text=f'Este randul jucatorului {jucator_2.get()}')
        else:
            scena_joc.insert(END, f"Poziție deja ocupată\n")
            scena_joc.see(END) 
            print("Ati spus deja o pozitie ocupata incercati alta pozitie")
    elif comanda in ["doi B", "2B", "2b", "2 b", "B2", "b2", "b 2"]:
        if m[1][1] == 4:
            print("Ești în 2B")
            functia_de_completare(semn, 4)
            if semn == 'O':
                    m[1][1]= 0
                    semn = "X"
                    etichete_tura[0].config(text=f'Este randul jucatorului {jucator_1.get()}')
            else:
                    m[1][1]= 1
                    semn = "O"
                    etichete_tura[0].config(text=f'Este randul jucatorului {jucator_2.get()}')
        else:
            scena_joc.insert(END, f"Poziție deja ocupată\n")
            scena_joc.see(END) 
            print("Ati spus deja o pozitie ocupata incercati alta pozitie")

    elif comanda in ["doi C", "2C", "2c", "2 c", "C2", "c2", "c 2"]:
        if m[1][2] == 4:
            print("Ești în 2C")
            functia_de_completare(semn, 5)
            if semn == 'O':
                    m[1][2]= 0
                    semn = "X"
                    etichete_tura[0].config(text=f'Este randul jucatorului {jucator_1.get()}')
            else:
                    m[1][2]= 1
                    semn = "O"
                    etichete_tura[0].config(text=f'Este randul jucatorului {jucator_2.get()}')
        else:
            scena_joc.insert(END, f"Poziție deja ocupată\n")
            scena_joc.see(END) 
            print("Ati spus deja o pozitie ocupata incercati alta pozitie")

    elif comanda in ["trei A", "3A", "3a", "3 a", "A3", "a3", "a 3"]:
        if m[2][0] == 4:
            print("Ești în 3A")
            functia_de_completare(semn, 6)
            if semn == 'O':
                    m[2][0]= 0
                    semn = "X"
                    etichete_tura[0].config(text=f'Este randul jucatorului {jucator_1.get()}')
            else:
                    m[2][0]= 1
                    semn = "O"
                    etichete_tura[0].config(text=f'Este randul jucatorului {jucator_2.get()}')
        else:
            scena_joc.insert(END, f"Poziție deja ocupată\n")
            scena_joc.see(END) 
            print("Ati spus deja o pozitie ocupata incercati alta pozitie")
            
    elif comanda in ["trei B", "3B", "3b", "3 b", "B3", "b3", "b 3"]:
        if m[2][1] == 4:
            print("Ești în 3B")
            functia_de_completare(semn, 7)
            if semn == 'O':
                    m[2][1]= 0
                    semn = "X"
                    etichete_tura[0].config(text=f'Este randul jucatorului {jucator_1.get()}')
            else:
                    m[2][1]= 1
                    semn = "O"
                    etichete_tura[0].config(text=f'Este randul jucatorului {jucator_2.get()}')
        else:
            scena_joc.insert(END, f"Poziție deja ocupată\n")
            scena_joc.see(END) 
            print("Ati spus deja o pozitie ocupata incercati alta pozitie")

    elif comanda in ["trei C", "3C", "3c", "trei c","3 c", "C3", "c3", "c 3"]:
        if m[2][2] == 4:
            print("Ești în 3C")
            functia_de_completare(semn, 8)
            if semn == 'O':
                    m[2][2]= 0
                    semn = "X"
                    etichete_tura[0].config(text=f'Este randul jucatorului {jucator_1.get()}')
            else:
                    m[2][2]= 1
                    semn = "O"
                    etichete_tura[0].config(text=f'Este randul jucatorului {jucator_2.get()}')
        else:
            scena_joc.insert(END, f"Poziție deja ocupată\n")
            scena_joc.see(END) 
            print("Ati spus deja o pozitie ocupata incercati alta pozitie")
    else:
        scena_joc.insert(END, f"Opțiune invalidă \n")
        scena_joc.see(END) 
        print("Comandă necunoscută")
    
        
def functia_de_completare(valoare, index):
    #verificare suplimentara ca indexul sa fie in vectorul cu indexi casutelor
    if 0 <= index < len(etichete_joc):
        # Setează valoarea cheii text a etichetei
        etichete_joc[index].config(text=valoare)
    else:
        print("Index invalid")
        
#functia care verifica daca a castigat cineva     
def win_condition():
     s1 = 0
     s2=0
     egalitate = "egalitate"
     #fac suma pe coloane 
     column_sums = [sum([row[i] for row in m]) for i in range(0,len(m[0]))]
     #fac suma pe randuri
     row_sums = [sum(row) for row in m]
     #intorc adevarat daca suma pe randuri sau coloane este 0 sau 3
     if(3 in column_sums) or(0 in column_sums) :return True
     if(3 in row_sums)  or (0 in row_sums) :return True
     
     #fac suma pe diagonale
     for i in range(3) :
     
         s1 += m[i][i];
         s2 += m[i][2 - i ];
    # daca suma pe diagonale este 0 sau 3 intorc adevarat        
     if(s1 == 3) or (s1 == 0) : return True
     if(s2 == 3 ) or (s2 == 0) : return True
     #verific daca mai am spatii libere in matrice daca nu este remiza
     if verifica_egalitate(m):
         print("A castigat prietenia")
         return egalitate
        
     return False
#verifica egalitatea
def verifica_egalitate(m):
    for row in m:
        for element in row:
            if element == 4:
                return False
    return True     
#foloseste boxele pentru a anunta castigatorul
def rostește_mesaj(mesaj):
    #convertesc text in audio
    tts = gTTS(text=mesaj, lang='ro')
    #salvez in fisier audio
    tts.save("castigator.mp3")
    pygame.mixer.init()#initializez modului pygame.mixer responabil pentru manipularea sunetului
    pygame.mixer.music.load("castigator.mp3")  # Încarcă fișierul audio
    pygame.mixer.music.play()  # Redă fișierul audio
    pygame.time.wait(3000)  # Așteaptă 3 secunde (sau până la sfârșitul melodiei) înainte de a continua
    pygame.mixer.quit()     
#inchi fereastra de joc         
def inchide_joc():
    window.destroy()
#functia care reinitializeaza variabilele de stare a jocului si afiseaza fereastra de inceput 
def inceput():
    for widget in window.winfo_children():
        widget.destroy()
    global etichete_joc 
    global etichete_tura
    global semn
    etichete_joc = [] 
    etichete_tura = []
    semn = "neinitializat"
    window.geometry("400x470")
    window.config(bg="#e6f7ff") 
    #eticheta pt joc
    titlu = Label(window, text='Joc X și 0',bg="#99ccff",font=("Helvetica", 12, "bold"), relief='ridge', padx=10, pady=10)
    titlu.grid(row=0, column=1, padx=50, pady=20)
    
    #etichete pentru nume jucator 1
    label_eticheta_1 = Label(window, text='Jucător 1: ',font=("Helvetica", 8, "bold"), bg="#99ccff",relief='ridge', padx=5, pady=5)
    label_eticheta_1.grid(row=1,column=1,padx=10,pady=10,)
    eticheta_nume_1 = Text(window, height=2, width=13,relief='ridge',state = "disabled")
    eticheta_nume_1.grid(row = 2,column=1)
    #etichete pentru nume jucator 2
    label_eticheta_2 = Label(window, text='Jucător 2: ',font=("Helvetica", 8, "bold"), bg="#99ccff",relief='ridge', padx=5, pady=5)
    label_eticheta_2.grid(row=1,column=2,padx=10,pady=10)
    eticheta_nume_2 = Text(window, height=2, width=13, relief='ridge', state = "disabled")
    eticheta_nume_2.grid(row = 2,column=2)
    
    
    #butoane pt inserare nume stilizate care oferă un set de widget-uri tematice
    style = ttk.Style()
    style.configure("TButton", padding=6, relief="flat", background="#ccc")

    buton_nume1 = ttk.Button(window, text='Introdu numele jucătorului x', command=lambda: recunoastere_nume(jucator_1, eticheta_nume_1,scena_joc))
    buton_nume1.grid(row=3, column=1, padx=10, pady=15)

    buton_nume2 = ttk.Button(window, text='Introdu numele jucatorului 0', command=lambda: recunoastere_nume(jucator_2, eticheta_nume_2,scena_joc))
    buton_nume2.grid(row=3, column=2, padx=10, pady=15)

    buton_start = ttk.Button(window, text='Start', command=afiseaza_tabel)
    buton_start.grid(row=4, column=1, padx=50, pady=20)
    #widget text pentru a afisa in interfata mesaje utilizatorului 
    scena_joc = Text(window, height=5, width=40, wrap=WORD, font=("Helvetica", 10), bg="#e6f7ff", state = "disabled")
    scena_joc.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

inceput()