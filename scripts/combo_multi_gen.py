import os,pip
import random
from random import choice
import traceback
import subprocess,webbrowser
import sys
import time
import names
from tqdm import tqdm

yeninesil=(
"00:1A:79:",
"33:44:CF:",
"10:27:BE:",
"A0:BB:3E:",
"00:1B:79:",
"00:2A:79:",
)
os.system('cls')
c =     ["1","2","3","4","5","6","7","8","9","0","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"," "]

time.sleep(0.5)
mouse=("""
\33[0m\33[32m

█▀▀ █▀█ █▀▄▀█ █▄▄ █▀█   █▀▀ █▀▀ █▄░█
█▄▄ █▄█ █░▀░█ █▄█ █▄█   █▄█ ██▄ █░▀█
            
      \33[0m\33[0m\33[0m\33
\33[0;1;5;m
 """)
print(mouse)

time.sleep(0.5)
print ("""

Choose Which Type of Combo You Would Like to Make.

0)Mac Combo Generating
-------Matching-------
1)Mail:Pass.
2)User:Pass Names.
3)User:Pass Names Matching.
4)FirstLast:FirstLast
5)Mail.
6)Pass.
7)User.User Matching
8)User.
9)foreign:User numbered
10)foriegn:User matching.
11)User:Birth year.
12)User:Pass:Birth year.
13)User:Pass:(2 Nums).
14)User:Pass:(4 Nums).
15)User:Pass:(123 User).
16)User:Pass:(4x4 Nums Same).
17)User:Pass:(5x5 Nums Same).
18)User:Pass:(6x6 Nums Same).
19)User:Pass:(7x7 Nums Same).
20)User:Pass:(8x8 Nums Same).
21)User:Pass:(9x9 Nums Same).
22)User:Pass:(10x10 Nums Same).
23)User:Pass:(12x12 Nums Same).
24)User:Pass:(15x15 Nums Same).
---------Mixed-----------
25)User:Pass:(10x10 Mixed).
26)User:Pass:(12x10 Mixed).
27)User:Pass:(15x10 Mixed).
28)User:Pass:(Random Nums).
--------Different---------
29)User:Pass:(4x4 Nums Diff).
30)User:Pass:(5x5 Nums Diff).
31)User:Pass:(6x6 Nums Diff).
32)User:Pass:(7x7 Nums Diff).
33)User:Pass:(8x8 Nums Diff).
34)User:Pass:(9x9 Nums Diff).
35)User:Pass:(10x10 Nums Diff).
36)User:Pass:(12x12 Nums Diff).
37)User:Pass:(15x15 Nums Diff).

99)Exit.

""")
menu = input("Enter Option ")

if menu=="0":
    print("""

    Mac Combo Generating
    """)
    nnesil=str(yeninesil)
    nnesil=(nnesil.count(',')+1)
    for xd in range(0,(nnesil)):
            print(str(xd+1)+" - "+yeninesil[xd] )
    #subprocess.run(["clear", ""])


#print(nnesil)
    i=0
    nesil=0
    dosya=input("""
    Enter Your Combo File Name...

    File name=""")
    karisik=input("""
    \33[0m\33[1;40m Creating mixed mac type !

    \33[0m\33[1;40mPress Enter""")
    karisik=karisik.upper()
    print("")
    if not karisik[:1]=="E" :
        for xd in range(0,(nnesil)):
            print(str(xd+1)+" - "+yeninesil[xd] )
        nesil=input("""
        
    Choose Mac type=""")

    adet=input("""

    Number of macs to generate=""")

    DosyaA="/data/data/com.termux/files/home/storage/downloads/iptv/combo/"+dosya+".txt"
    def kaydet(mac):
        dosya=open(DosyaA,'a+') 
        dosya.write(mac)
        dosya.close()


    while True:
        #hex_num = hex(mag)[2:].zfill(6)
        genmac = "%02x:%02x:%02x"% (random.randint(0, 256),random.randint(0, 256),random.randint(0, 256))
        genmac=genmac.replace('100','10')
        #print(karisik[:1])
        if karisik[:1]=="E" :
            for xd in range(0,nnesil):
                    genmac = "%02x:%02x:%02x"% (random.randint(0, 256),random.randint(0, 256),random.randint(0, 256))
                    genmac=genmac.replace('100','10')
                    print(yeninesil[xd]+genmac)
                    kaydet(yeninesil[xd]+genmac+"\n")
        else:
            print(yeninesil[int(nesil)-1]+genmac)
            kaydet(yeninesil[int(nesil)-1]+genmac+"\n")
        i=i+1
        if str(i) ==adet:
            break
    print("\n\nProcess Completed now Goto Scanner and Scan for Fun\n\n")



if menu=="1":
    #os.system('clear')
    gmail = input("Which Mail Type ? (Ex:@gmail.com): ")
    hwm = int(input("Enter number of combos to generate : "))
    print (" ")
    print ("Enter the name of the file you want to save  ")
    print ("No need to enter the .txt ")
    filename = input("example combos     :  ")
    filename = filename + ".txt"
    print (" ")


    f = open(filename, "w")
    f.write("")
    f.close()

    for i in range (0,hwm):
        i = 1+1
        rname = names.get_first_name()
        rlastname = names.get_last_name()
        num = random.randint(0,2023)
        all1 = "%s%s%s"%(rname,num,gmail)
        alln = "%s%s%s%s"%(all1,":",rname,num)
        all2 = "%s%s%s"%(rlastname,num,gmail)
        allf = "%s%s%s%s"%(all2,":",rlastname,num) 
        all=alln 
        print(i," = ",all)
        f = open(filename, "a")
        f.write(all)
        f.write("\n")
        f.close()
        i += 1
    x = input("\nPress Enter To Exit...")


if menu=="2":
    hwm = int(input("Enter number of combos to generate : "))
    print (" ")
    print ("Enter the name of the file you want to save  ")
    print ("No need to enter the .txt ")
    filename = input("example combos     :  ")
    filename = filename + ".txt"
    print (" ")


    f = open(filename, "w")
    f.write("")
    f.close()

    for i in range (0,hwm):
        i = 1+1
        rname = names.get_first_name()
        rlastname = names.get_last_name()
        num = random.randint(1900,2023)
        all1 = "%s%s"%(rname,num)
        alln = "%s%s%s%s"%(all1,":",rlastname,num)
        all2 = "%s%s"%(rlastname,num)
        allf = "%s%s%s%s"%(all2,":",rname,num) 
        all=alln 
        print(i," = ",all)
        f = open(filename, "a")
        f.write(all)
        f.write("\n")
        f.close()
        i += 1
    x = input("\nPress Enter To Exit...")
    

if menu=="3":
    hwm = int(input("Enter number of combos to generate : "))
    print (" ")
    print ("Enter the name of the file you want to save  ")
    print ("No need to enter the .txt ")
    filename = input("example combos     :  ")
    filename = filename + ".txt"
    print (" ")


    f = open(filename, "w")
    f.write("")
    f.close()
    
    for i in range (0,hwm):
        i = 1+1
        rname = names.get_first_name()
        rlastname = names.get_last_name()
        num = random.randint(0,999)
        all1 = "%s"%(rname)
        alln = "%s%s%s"%(all1,":",rname)
        all2 = "%s"%(rlastname)
        allf = "%s%s%s"%(all2,":",rlastname)
        all=alln 
        print(i," = ",all)
        f = open(filename, "a")
        f.write(all)
        f.write("\n")
        f.close()
        i += 1
    x = input("\nPress Enter To Exit...")


if menu=="4":
    hwm = int(input("Enter number of combos to generate : "))
    print (" ")
    print ("Enter the name of the file you want to save  ")
    print ("No need to enter the .txt ")
    filename = input("example combos     :  ")
    filename = filename + ".txt"
    print (" ")


    f = open(filename, "w")
    f.write("")
    f.close()

    for i in range (0,hwm):
        i = 1+1
        rname = names.get_first_name()
        rlastname = names.get_last_name()
        #num = random.randint(1900,2020)
        all1 = "%s%s"%(rname,rlastname)
        alln = "%s%s%s%s"%(all1,":",rname,rlastname)
        all2 = "%s%s"%(rname,rlastname)
        allf = "%s%s%s%s"%(all2,":",rname,rlastname) 
        all=(alln)
        print(i," = ",all)
        f = open(filename, "a")
        f.write(all)
        f.write("\n")
        f.close()
        i += 1
    x = input("\nPress Enter To Exit...")


if menu=="5":
    #os.system('clear')
    gmail = input("Which Mail Type ? (Ex:@gmail.com): ")
    hwm = int(input("Enter number of combos to generate : "))
    print (" ")
    print ("Enter the name of the file you want to save  ")
    print ("No need to enter the .txt ")
    filename = input("example combos     :  ")
    filename = filename + ".txt"
    print (" ")


    f = open(filename, "w")
    f.write("")
    f.close()
    
    for i in range (0,hwm):
        i = 1+1
        rname = names.get_first_name()
        rlastname = names.get_last_name()
        num = random.randint(1500,2023)
        all1 = "%s%s%s"%(rname,num,gmail)
        all2 = "%s%s%s"%(rlastname,num,gmail)
        all=all1 
        print(i," = ",all)
        f = open(filename, "a")
        f.write(all)
        f.write("\n")
        f.close()
        i += 1
    x = input("\nPress Enter To Exit...")
    
    
if menu=="6":
    #os.system('clear')
    hwm = int(input("Enter number of combos to generate : "))
    print (" ")
    print ("Enter the name of the file you want to save  ")
    print ("No need to enter the .txt ")
    filename = input("example combos     :  ")
    filename = filename + ".txt"
    print (" ")


    f = open(filename, "w")
    f.write("")
    f.close()
    
    for i in range (0,hwm):
        i = 1+1
        rname = names.get_first_name()
        rlastname = names.get_last_name()
        num = random.randint(0,2023)
        alln = "%s%s"%(rname,num)
        all=alln 
        print(i," = ",all)
        f = open(filename, "a")
        f.write(all)
        f.write("\n")
        f.close()
        i += 1
    x = input("\nPress Enter To Exit...")
    
if menu=="7":
    hwm = int(input("Enter number of combos to generate : "))
    print (" ")
    print ("Enter the name of the file you want to save  ")
    print ("No need to enter the .txt ")
    filename = input("example combos     :  ")
    filename = filename + ".txt"
    print (" ")


    f = open(filename, "w")
    f.write("")
    f.close()
    
    for i in range (0,hwm):
        i = 1+1
        rname = names.get_first_name()
        rlastname = names.get_last_name()
        num = random.randint(000,999)
        all1 = "%s"%(rname)
        alln = "%s%s%s"%(all1,":",rname)
        all2 = "%s"%(rlastname)
        allf = "%s%s%s"%(all2,":",rlastname)
        all=alln 
        print(i," = ",all)
        f = open(filename, "a")
        f.write(all)
        f.write("\n")
        f.close()
        i += 1
    x = input("\nPress Enter To Exit...")


if menu=="8":
    hwm = int(input("Enter number of combos to generate : "))
    print (" ")
    print ("Enter the name of the file you want to save  ")
    print ("No need to enter the .txt ")
    filename = input("example combos     :  ")
    filename = filename + ".txt"
    print (" ")


    f = open(filename, "w")
    f.write("")
    f.close()
    
    for i in range (0,hwm):
        i = 1+1
        rname = names.get_first_name()
        rlastname = names.get_last_name()
        num = random.randint(1900,2023)
        all1 = "%s%s"%(rname,num)
        all2 = "%s%s"%(rlastname,num)
        all=all1 
        print(i," = ",all)
        f = open(filename, "a")
        f.write(all)
        f.write("\n")
        f.close()
        i += 1
    x = input("\nPress Enter To Exit...")



if menu=="9":
    hwm = int(input("Enter number of combos to generate : "))
    print (" ")
    print ("Enter the name of the file you want to save  ")
    print ("No need to enter the .txt ")
    filename = input("example combos     :  ")
    filename = filename + ".txt"
    print (" ")


    f = open(filename, "w")
    f.write("")
    f.close()
    
    for i in range (0,hwm):
        i = 1+1
        fname = names.get_first_name()
        flastname = names.get_last_name()
        num = random.randint(000,999)
        all1 = "%s%s"%(fname,num)
        alln = "%s%s%s%s"%(all1,":",fname,num)
        all2 = "%s%s"%(flastname,num)
        allf = "%s%s%s%s"%(all2,":",flastname,num)
        all=alln 
        print(i," = ",all)
        f = open(filename, "a")
        f.write(all)
        f.write("\n")
        f.close()
        i += 1
    x = input("\nPress Enter To Exit...")


if menu=="10":
    hwm = int(input("Enter number of combos to generate : "))
    print (" ")
    print ("Enter the name of the file you want to save  ")
    print ("No need to enter the .txt ")
    filename = input("example combos     :  ")
    filename = filename + ".txt"
    print (" ")


    f = open(filename, "w")
    f.write("")
    f.close()
    
    for i in range (0,hwm):
        i = 1+1
        fname = names.get_first_name()
        flastname = names.get_last_name()
        num = random.randint(000,999)
        all1 = "%s"%(fname)
        alln = "%s%s%s"%(all1,":",fname)
        all2 = "%s"%(flastname)
        allf = "%s%s%s"%(all2,":",flastname)
        all=alln 
        print(i," = ",all)
        f = open(filename, "a")
        f.write(all)
        f.write("\n")
        f.close()
        i += 1
    x = input("\nPress Enter To Exit...")



if menu=="11":
    hwm = int(input("Enter number of combos to generate : "))
    print (" ")
    print ("Enter the name of the file you want to save  ")
    print ("No need to enter the .txt ")
    filename = input("example combos     :  ")
    filename = filename + ".txt"
    print (" ")


    f = open(filename, "w")
    f.write("")
    f.close()
    
    for i in range (0,hwm):
        i = 1+1
        fname = names.get_first_name()
        flastname = names.get_last_name()
        num = random.randint(1900,2023)
        alln = "%s%s"%(fname,num)
        all=alln 
        print(i," = ",all)
        f = open(filename, "a")
        f.write(all)
        f.write("\n")
        f.close()
        i += 1
    x = input("\nPress Enter To Exit...")



if menu=="12":
    hwm = int(input("Enter number of combos to generate : "))
    print (" ")
    print ("Enter the name of the file you want to save  ")
    print ("No need to enter the .txt ")
    filename = input("example combos     :  ")
    filename = filename + ".txt"
    print (" ")


    f = open(filename, "w")
    f.write("")
    f.close()
    
    for i in range (0,hwm):
        i = 1+1
        fname = names.get_first_name()
        flastname = names.get_last_name()
        num = random.randint(10,10)
        all1 = "%s%s"%(fname,num)
        alln = "%s%s%s%s"%(all1,":",fname,num)
        all2 = "%s%s"%(flastname,num)
        allf = "%s%s%s%s"%(all2,":",flastname,num)
        all=alln 
        print(i," = ",all)
        f = open(filename, "a")
        f.write(all)
        f.write("\n")
        f.close()
        i += 1
    x = input("\nPress Enter To Exit...")



if menu=="13":
    hwm = int(input("Enter number of combos to generate : "))
    print (" ")
    print ("Enter the name of the file you want to save  ")
    print ("No need to enter the .txt ")
    filename = input("example combos     :  ")
    filename = filename + ".txt"
    print (" ")


    f = open(filename, "w")
    f.write("")
    f.close()
    
    for i in range (0,hwm):
        i = 1+1
        fname = names.get_first_name()
        flastname = names.get_last_name()
        num = random.randint(00,99)
        all1 = "%s%s"%(fname,num)
        alln = "%s%s%s%s"%(all1,":",fname,num)
        all2 = "%s%s"%(flastname,num)
        allf = "%s%s%s%s"%(all2,":",flastname,num)
        all=alln 
        print(i," = ",all)
        f = open(filename, "a")
        f.write(all)
        f.write("\n")
        f.close()
        i += 1
    x = input("\nPress Enter To Exit...")


if menu=="14":
    hwm = int(input("Enter number of combos to generate : "))
    print (" ")
    print ("Enter the name of the file you want to save  ")
    print ("No need to enter the .txt ")
    filename = input("example combos     :  ")
    filename = filename + ".txt"
    print (" ")


    f = open(filename, "w")
    f.write("")
    f.close()
    
    for i in range (0,hwm):
        i = 1+1
        fname = names.get_first_name()
        flastname = names.get_last_name()
        num = random.randint(0000,9999)
        all1 = "%s%s"%(fname,num)
        alln = "%s%s%s%s"%(all1,":",fname,num)
        all2 = "%s%s"%(flastname,num)
        allf = "%s%s%s%s"%(all2,":",flastname,num)
        all=alln 
        print(i," = ",all)
        f = open(filename, "a")
        f.write(all)
        f.write("\n")
        f.close()
        i += 1
    x = input("\nPress Enter To Exit...")    


if menu=="15":
    hwm = int(input("Enter number of combos to generate : "))
    print (" ")
    print ("Enter the name of the file you want to save  ")
    print ("No need to enter the .txt ")
    filename = input("example combos     :  ")
    filename = filename + ".txt"
    print (" ")


    f = open(filename, "w")
    f.write("")
    f.close()
    
    for i in range (0,hwm):
        i = 1+1
        fname = names.get_first_name()
        flastname = names.get_last_name()
        num = random.randint(123,123)
        all1 = "%s%s"%(fname,num)
        alln = "%s%s%s%s"%(all1,":",fname,num)
        all2 = "%s%s"%(flastname,num)
        allf = "%s%s%s%s"%(all2,":",flastname,num)
        all=alln 
        print(i," = ",all)
        f = open(filename, "a")
        f.write(all)
        f.write("\n")
        f.close()
        i += 1
    x = input("\nPress Enter To Exit...")


if menu=="16":
    c =     ["1","2","3","4","5","6","7","8","9","0","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"," "]


    print(" ")
    print(" ")

# To take input from the user,
    n = int(input("Enter number of combos to generate :   "))
    print (" ")
    print ("Enter the name of the file you want to save  ")
    print ("No need to enter the .txt ")
    filename = input("example combos     :  ")
    filename = filename + ".txt"
    print (" ")

# reset filename

    f = open(filename, "w")
    f.write("")
    f.close()

    i = 1

    while i <= n:
      g1=random.randint(0,9)
      g2=random.randint(0,9)
      g3=random.randint(0,9)
      g4=random.randint(0,9)
      c1 = c[g1]
      c2 = c[g2]
      c3 = c[g3]
      c4 = c[g4]
      user = c1+c2+c3+c4
      user=user+":"+user 
      print(i," = ",user)
      f = open(filename, "a")
      f.write(user)
      f.write("\n")
      f.close()
      i += 1
   


    print (" ")
    print (n," COMBOS SAVED TO : ",filename,)
    print (" ")
    print ("SCRIPT WRITTEN BY <= 🅼🆁.🅽🅾🅾🅱 =>")
    print (" ")
    print ("PRESS ENTER TO EXIT")
    input()



#if menu=="99":
    quit()




if menu=="17":
    c =     ["1","2","3","4","5","6","7","8","9","0","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"," "]


    print(" ")
    print(" ")

# To take input from the user,
    n = int(input("Enter number of combos to generate :   "))
    print (" ")
    print ("Enter the name of the file you want to save  ")
    print ("No need to enter the .txt ")
    filename = input("example combos     :  ")
    filename = filename + ".txt"
    print (" ")

# reset filename

    f = open(filename, "w")
    f.write("")
    f.close()

    i = 1

    while i <= n:
      g1=random.randint(0,9)
      g2=random.randint(0,9)
      g3=random.randint(0,9)
      g4=random.randint(0,9)
      g5=random.randint(0,9)
      c1 = c[g1]
      c2 = c[g2]
      c3 = c[g3]
      c4 = c[g4]
      c5 = c[g5]
      user = c1+c2+c3+c4+c5
      user=user+":"+user 
      print(i," = ",user)
      f = open(filename, "a")
      f.write(user)
      f.write("\n")
      f.close()
      i += 1
   
    x = input("\nPress Enter To Exit...")

    print (" ")
    print (n," COMBOS SAVED TO : ",filename,)
    print (" ")
    print ("SCRIPT WRITTEN BY <= 🅼🆁.🅽🅾🅾🅱 =>")
    print (" ")
    print ("PRESS ENTER TO EXIT")
    input()



#if menu=="99":
    quit()



if menu=="18":
    c =     ["1","2","3","4","5","6","7","8","9","0","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"," "]


    print(" ")
    print(" ")

# To take input from the user,
    n = int(input("Enter number of combos to generate :   "))
    print (" ")
    print ("Enter the name of the file you want to save  ")
    print ("No need to enter the .txt ")
    filename = input("example combos     :  ")
    filename = filename + ".txt"
    print (" ")

# reset filename

    f = open(filename, "w")
    f.write("")
    f.close()

    i = 1

    while i <= n:
       g1=random.randint(0,9)
       g2=random.randint(0,9)
       g3=random.randint(0,9)
       g4=random.randint(0,9)
       g5=random.randint(0,9)
       g6=random.randint(0,9)
       c1 = c[g1]
       c2 = c[g2]
       c3 = c[g3]
       c4 = c[g4]
       c5 = c[g5]
       c6 = c[g6]
       user = c1+c2+c3+c4+c5+c6
       user=user+":"+user 
       print(i," = ",user)
       f = open(filename, "a")
       f.write(user)
       f.write("\n")
       f.close()
       i += 1
   

    print (" ")
    print (n," COMBOS SAVED TO : ",filename,)
    print (" ")
    print ("SCRIPT WRITTEN BY <= 🅼🆁.🅽🅾🅾🅱 =>")
    print (" ")
    print ("PRESS ENTER TO EXIT")
    input()

#    quit()




if menu=="19":
    c =     ["1","2","3","4","5","6","7","8","9","0","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"," "]


    print(" ")
    print(" ")

# To take input from the user,
    n = int(input("Enter number of combos to generate :   "))
    print (" ")
    print ("Enter the name of the file you want to save  ")
    print ("No need to enter the .txt ")
    filename = input("example combos     :  ")
    filename = filename + ".txt"
    print (" ")

# reset filename

    f = open(filename, "w")
    f.write("")
    f.close()

    i = 1

    while i <= n:
       g1=random.randint(0,9)
       g2=random.randint(0,9)
       g3=random.randint(0,9)
       g4=random.randint(0,9)
       g5=random.randint(0,9)
       g6=random.randint(0,9)
       g7=random.randint(0,9)
       c1 = c[g1]
       c2 = c[g2]
       c3 = c[g3]
       c4 = c[g4]
       c5 = c[g5]
       c6 = c[g6]
       c7 = c[g7]
       user = c1+c2+c3+c4+c5+c6+c7
       user=user+":"+user 
       print(i," = ",user)
       f = open(filename, "a")
       f.write(user)
       f.write("\n")
       f.close()
       i += 1
   

    print (" ")
    print (n," COMBOS SAVED TO : ",filename,)
    print (" ")
    print ("SCRIPT WRITTEN BY <= 🅼🆁.🅽🅾🅾🅱 =>")
    print (" ")
    print ("PRESS ENTER TO EXIT")
    input()

#    quit()


if menu=="20":
    c =     ["1","2","3","4","5","6","7","8","9","0","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"," "]


    print(" ")
    print(" ")

# To take input from the user,
    n = int(input("Enter number of combos to generate :   "))
    print (" ")
    print ("Enter the name of the file you want to save  ")
    print ("No need to enter the .txt ")
    filename = input("example combos     :  ")
    filename = filename + ".txt"
    print (" ")

# reset filename

    f = open(filename, "w")
    f.write("")
    f.close()

    i = 1

    while i <= n:
       g1=random.randint(0,9)
       g2=random.randint(0,9)
       g3=random.randint(0,9)
       g4=random.randint(0,9)
       g5=random.randint(0,9)
       g6=random.randint(0,9)
       g7=random.randint(0,9)
       g8=random.randint(0,9)
       c1 = c[g1]
       c2 = c[g2]
       c3 = c[g3]
       c4 = c[g4]
       c5 = c[g5]
       c6 = c[g6]
       c7 = c[g7]
       c8 = c[g8]
       user = c1+c2+c3+c4+c5+c6+c7+c8
       user=user+":"+user 
       print(i," = ",user)
       f = open(filename, "a")
       f.write(user)
       f.write("\n")
       f.close()
       i += 1
   

    print (" ")
    print (n," COMBOS SAVED TO : ",filename,)
    print (" ")
    print ("SCRIPT WRITTEN BY <= 🅼🆁.🅽🅾🅾🅱 =>")
    print (" ")
    print ("PRESS ENTER TO EXIT")
    input()



#    quit()



if menu=="21":
    c =     ["1","2","3","4","5","6","7","8","9","0","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"," "]


    print(" ")
    print(" ")

# To take input from the user,
    n = int(input("Enter number of combos to generate :   "))
    print (" ")
    print ("Enter the name of the file you want to save  ")
    print ("No need to enter the .txt ")
    filename = input("example combos     :  ")
    filename = filename + ".txt"
    print (" ")

# reset filename

    f = open(filename, "w")
    f.write("")
    f.close()

    i = 1

    while i <= n:
       g1=random.randint(0,9)
       g2=random.randint(0,9)
       g3=random.randint(0,9)
       g4=random.randint(0,9)
       g5=random.randint(0,9)
       g6=random.randint(0,9)
       g7=random.randint(0,9)
       g8=random.randint(0,9)
       g9=random.randint(0,9)
       c1 = c[g1]
       c2 = c[g2]
       c3 = c[g3]
       c4 = c[g4]
       c5 = c[g5]
       c6 = c[g6]
       c7 = c[g7]
       c8 = c[g8]
       c9 = c[g9]
       user = c1+c2+c3+c4+c5+c6+c7+c8+c9
       user=user+":"+user 
       print(i," = ",user)
       f = open(filename, "a")
       f.write(user)
       f.write("\n")
       f.close()
       i += 1
   

    print (" ")
    print (n," COMBOS SAVED TO : ",filename,)
    print (" ")
    print ("SCRIPT WRITTEN BY <= 🅼🆁.🅽🅾🅾🅱 =>")
    print (" ")
    print ("PRESS ENTER TO EXIT")
    input()



#    quit()








if menu=="22":
    c =     ["1","2","3","4","5","6","7","8","9","0","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"," "]


    print(" ")
    print(" ")

# To take input from the user,
    n = int(input("Enter number of combos to generate :   "))
    print (" ")
    print ("Enter the name of the file you want to save  ")
    print ("No need to enter the .txt ")
    filename = input("example combos     :  ")
    filename = filename + ".txt"
    print (" ")

# reset filename

    f = open(filename, "w")
    f.write("")
    f.close()

    i = 1

    while i <= n:
       g1=random.randint(0,9)
       g2=random.randint(0,9)
       g3=random.randint(0,9)
       g4=random.randint(0,9)
       g5=random.randint(0,9)
       g6=random.randint(0,9)
       g7=random.randint(0,9)
       g8=random.randint(0,9)
       g9=random.randint(0,9)
       g10=random.randint(0,9)
       c1 = c[g1]
       c2 = c[g2]
       c3 = c[g3]
       c4 = c[g4]
       c5 = c[g5]
       c6 = c[g6]
       c7 = c[g7]
       c8 = c[g8]
       c9 = c[g9]
       c9 = c[g10]
       user = c1+c2+c3+c4+c5+c6+c7+c8+c9+c10
       user=user+":"+user 
       print(i," = ",user)
       f = open(filename, "a")
       f.write(user)
       f.write("\n")
       f.close()
       i += 1
   

    print (" ")
    print (n," COMBOS SAVED TO : ",filename,)
    print (" ")
    print ("SCRIPT WRITTEN BY <= 🅼🆁.🅽🅾🅾🅱 =>")
    print (" ")
    print ("PRESS ENTER TO EXIT")
    input()



#    quit()


if menu=="23":
    c =     ["1","2","3","4","5","6","7","8","9","0","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"," "]


    print(" ")
    print(" ")

# To take input from the user,
    n = int(input("Enter number of combos to generate :   "))
    print (" ")
    print ("Enter the name of the file you want to save  ")
    print ("No need to enter the .txt ")
    filename = input("example combos     :  ")
    filename = filename + ".txt"
    print (" ")

    # reset filename

    f = open(filename, "w")
    f.write("")
    f.close()

    i = 1

    while i <= n:
       g1=random.randint(0,9)
       g2=random.randint(0,9)
       g3=random.randint(0,9)
       g4=random.randint(0,9)
       g5=random.randint(0,9)
       g6=random.randint(0,9)
       g7=random.randint(0,9)
       g8=random.randint(0,9)
       g9=random.randint(0,9)
       g10=random.randint(0,9)
       g11=random.randint(0,9)
       g12=random.randint(0,9)
       c1 = c[g1]
       c2 = c[g2]
       c3 = c[g3]
       c4 = c[g4]
       c5 = c[g5]
       c6 = c[g6]
       c7 = c[g7]
       c8 = c[g8]
       c9 = c[g9]
       c10 = c[g10]
       c11 = c[g11]
       c12 = c[g12]
       user = c1+c2+c3+c4+c5+c6+c7+c8+c9+c10+c11+c12
       user=user+":"+user 
       print(i," = ",user)
       f = open(filename, "a")
       f.write(user)
       f.write("\n")
       f.close()
       i += 1
   

    print (" ")
    print (n," COMBOS SAVED TO : ",filename,)
    print (" ")
    print ("SCRIPT WRITTEN BY <= 🅼🆁.🅽🅾🅾🅱 =>")
    print (" ")
    print ("PRESS ENTER TO EXIT")
    input()



#if menu=="99":
    quit()



if menu=="24":
    c =     ["1","2","3","4","5","6","7","8","9","0","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"," "]


    print(" ")
    print(" ")

# To take input from the user,
    n = int(input("Enter number of combos to generate :   "))
    print (" ")
    print ("Enter the name of the file you want to save  ")
    print ("No need to enter the .txt ")
    filename = input("example combos     :  ")
    filename = filename + ".txt"
    print (" ")

# reset filename

    f = open(filename, "w")
    f.write("")
    f.close()

    i = 1

    while i <= n:
       g1=random.randint(0,9)
       g2=random.randint(0,9)
       g3=random.randint(0,9)
       g4=random.randint(0,9)
       g5=random.randint(0,9)
       g6=random.randint(0,9)
       g7=random.randint(0,9)
       g8=random.randint(0,9)
       g9=random.randint(0,9)
       g10=random.randint(0,9)
       g11=random.randint(0,9)
       g12=random.randint(0,9)
       g13=random.randint(0,9)
       g14=random.randint(0,9)
       g15=random.randint(0,9)
       c1 = c[g1]
       c2 = c[g2]
       c3 = c[g3]
       c4 = c[g4]
       c5 = c[g5]
       c6 = c[g6]
       c7 = c[g7]
       c8 = c[g8]
       c9 = c[g9]
       c10 = c[g10]
       c11 = c[g11]
       c12 = c[g12]
       c13 = c[g13]
       c14 = c[g14]
       c15 = c[g15]
       user = c1+c2+c3+c4+c5+c6+c7+c8+c9+c10+c11+c12+c13+c14+c15
       user=user+":"+user 
       print(i," = ",user)
       f = open(filename, "a")
       f.write(user)
       f.write("\n")
       f.close()
       i += 1
   

    print (" ")
    print (n," COMBOS SAVED TO : ",filename,)
    print (" ")
    print ("SCRIPT WRITTEN BY <= 🅼🆁.🅽🅾🅾🅱 =>")
    print (" ")
    print ("PRESS ENTER TO EXIT")
    input()



#if menu=="99":
    quit()


if menu=="25":
    c =     ["1","2","3","4","5","6","7","8","9","0","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"," "]


    print(" ")
    print(" ")

# To take input from the user,
    n = int(input("Enter number of combos to generate :   "))
    print (" ")
    print ("Enter the name of the file you want to save  ")
    print ("No need to enter the .txt ")
    filename = input("example combos     :  ")
    filename = filename + ".txt"
    print (" ")

# reset filename

    f = open(filename, "w")
    f.write("")
    f.close()

    i = 1

    while i <= n:
       g1=random.randint(0,61)
       g2=random.randint(0,61)
       g3=random.randint(0,61)
       g4=random.randint(0,61)
       g5=random.randint(0,61)
       g6=random.randint(0,61)
       g7=random.randint(0,61)
       g8=random.randint(0,61)
       g9=random.randint(0,61)
       g10=random.randint(0,61)
       c1 = c[g1]
       c2 = c[g2]
       c3 = c[g3]
       c4 = c[g4]
       c5 = c[g5]
       c6 = c[g6]
       c7 = c[g7]
       c8 = c[g8]
       c9 = c[g9]
       c10 = c[g10]
       user = c1+c2+c3+c4+c5+c6+c7+c8+c9+c10
       g1=random.randint(1,61)
       g2=random.randint(1,61)
       g3=random.randint(1,61)
       g4=random.randint(1,61)
       g5=random.randint(1,61)
       g6=random.randint(1,61)
       g7=random.randint(1,61)
       g8=random.randint(1,61)
       g9=random.randint(1,61)
       g10=random.randint(1,61)
       c1 = c[g1]
       c2 = c[g2]
       c3 = c[g3]
       c4 = c[g4]
       c5 = c[g5]
       c6 = c[g6]
       c7 = c[g7]
       c8 = c[g8]
       c9 = c[g9]
       c10 = c[g10]
       pw = c1+c2+c3+c4+c5+c6+c7+c8+c9+c10
       user=user+":"+pw 
       print(i," = ",user)
       f = open(filename, "a")
       f.write(user)
       f.write("\n")
       f.close()
       i += 1
   

    print (" ")
    print (n," COMBOS SAVED TO : ",filename,)
    print (" ")
    print ("SCRIPT WRITTEN BY <= 🅼🆁.🅽🅾🅾🅱 =>")
    print (" ")
    print ("PRESS ENTER TO EXIT")
    input()



#if menu=="99":
    quit()



if menu=="26":
    c =     ["1","2","3","4","5","6","7","8","9","0","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"," "]


    print(" ")
    print(" ")

# To take input from the user,
    n = int(input("Enter number of combos to generate :   "))
    print (" ")
    print ("Enter the name of the file you want to save  ")
    print ("No need to enter the .txt ")
    filename = input("example combos     :  ")
    filename = filename + ".txt"
    print (" ")

# reset filename

    f = open(filename, "w")
    f.write("")
    f.close()

    i = 1

    while i <= n:
       g1=random.randint(0,9)
       g2=random.randint(0,9)
       g3=random.randint(0,9)
       g4=random.randint(0,9)
       g5=random.randint(0,9)
       g6=random.randint(0,9)
       g7=random.randint(0,9)
       g8=random.randint(0,9)
       g9=random.randint(0,9)
       g10=random.randint(0,9)
       g11=random.randint(0,9)
       g12=random.randint(0,9)
       c1 = c[g1]
       c2 = c[g2]
       c3 = c[g3]
       c4 = c[g4]
       c5 = c[g5]
       c6 = c[g6]
       c7 = c[g7]
       c8 = c[g8]
       c9 = c[g9]
       c10 = c[g10]
       c11 = c[g11]
       c12 = c[g12]
       user=c1+c2+c3+c4+c5+c6+c7+c8+c9+c10+c11+c12
       g1=random.randint(1,9)
       g2=random.randint(1,9)
       g3=random.randint(1,9)
       g4=random.randint(1,9)
       g5=random.randint(1,9)
       g6=random.randint(1,9)
       g7=random.randint(1,9)
       g8=random.randint(1,9)
       g9=random.randint(1,9)
       g10=random.randint(1,9)
       c1 = c[g1]
       c2 = c[g2]
       c3 = c[g3]
       c4 = c[g4]
       c5 = c[g5]
       c6 = c[g6]
       c7 = c[g7]
       c8 = c[g8]
       c9 = c[g9]
       c10= c[g10]
       user = c1+c2+c3+c4+c5+c6+c7+c8+c9+c10
       user=user+":"+user 
       print(i," = ",user)
       f = open(filename, "a")
       f.write(user)
       f.write("\n")
       f.close()
       i += 1
   

    print (" ")
    print (n," COMBOS SAVED TO : ",filename,)
    print (" ")
    print ("SCRIPT WRITTEN BY <= 🅼🆁.🅽🅾🅾🅱 =>")
    print (" ")
    print ("PRESS ENTER TO EXIT")
    input()



#if menu=="99":
    quit()



if menu=="27":
    c =     ["1","2","3","4","5","6","7","8","9","0","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"," "]


    print(" ")
    print(" ")

# To take input from the user,
    n = int(input("Enter number of combos to generate :   "))
    print (" ")
    print ("Enter the name of the file you want to save  ")
    print ("No need to enter the .txt ")
    filename = input("example combos     :  ")
    filename = filename + ".txt"
    print (" ")

# reset filename

    f = open(filename, "w")
    f.write("")
    f.close()

    i = 1

    while i <= n:
       g1=random.randint(0,61)
       g2=random.randint(0,61)
       g3=random.randint(0,61)
       g4=random.randint(0,61)
       g5=random.randint(0,61)
       g6=random.randint(0,61)
       g7=random.randint(0,61)
       g8=random.randint(0,61)
       g9=random.randint(0,61)
       g10=random.randint(0,61)
       g11=random.randint(0,61)
       g12=random.randint(0,61)
       g13=random.randint(0,61)
       g14=random.randint(0,61)
       g15=random.randint(0,61)
       c1 = c[g1]
       c2 = c[g2]
       c3 = c[g3]
       c4 = c[g4]
       c5 = c[g5]
       c6 = c[g6]
       c7 = c[g7]
       c8 = c[g8]
       c9 = c[g9]
       c10 = c[g10]
       c11 = c[g11]
       c12 = c[g12]
       c13 = c[g13]
       c14 = c[g14]
       c15 = c[g15]
       user = c1+c2+c3+c4+c5+c6+c7+c8+c9+c10+c11+c12+c13+c14+c15
       g1=random.randint(1,61)
       g2=random.randint(1,61)
       g3=random.randint(1,61)
       g4=random.randint(1,61)
       g5=random.randint(1,61)
       g6=random.randint(1,61)
       g7=random.randint(1,61)
       g8=random.randint(1,61)
       g9=random.randint(1,61)
       g10=random.randint(1,61)
       c1 = c[g1]
       c2 = c[g2]
       c3 = c[g3]
       c4 = c[g4]
       c5 = c[g5]
       c6 = c[g6]
       c7 = c[g7]
       c8 = c[g8]
       c9 = c[g9]
       c10 = c[g10]
       pw = c1+c2+c3+c4+c5+c6+c7+c8+c9+c10
       user=user+":"+pw 
       print(i," = ",user)
       f = open(filename, "a")
       f.write(user)
       f.write("\n")
       f.close()
       i += 1



#if menu=="99":
    quit()



if menu=="28":
    hwm = int(input("Enter number of combos to generate : "))
    print (" ")
    print ("Enter the name of the file you want to save  ")
    print ("No need to enter the .txt ")
    filename = input("example combos     :  ")
    filename = filename + ".txt"
    print (" ")


    f = open(filename, "w")
    f.write("")
    f.close()
    
    for i in range (0,hwm):
        i = 1+1
        rname = random.randint(0,999)
        rlastname = random.randint(0,999)
        num = random.randint(0,999)
        all1 = "%s%s"%(rname,num)
        alln = "%s%s%s%s"%(all1,":",rname,num)
        all2 = "%s%s"%(rlastname,num)
        allf = "%s%s%s%s"%(all2,":",rlastname,num)
        all=alln 
        print(i," = ",all)
        f = open(filename, "a")
        f.write(all)
        f.write("\n")
        f.close()
        i += 1
    x = input("\nPress Enter To Exit...")


if menu=="29":
    c =     ["1","2","3","4","5","6","7","8","9","0"," "]


    print(" ")
    print(" ")

# To take input from the user,
    n = int(input("Enter number of combos to generate :   "))
    print (" ")
    print ("Enter the name of the file you want to save  ")
    print ("No need to enter the .txt ")
    filename = input("example combos     :  ")
    filename = filename + ".txt"
    print (" ")

# reset filename

    f = open(filename, "w")
    f.write("")
    f.close()

    i = 1

    while i <= n:
       g1=random.randint(0,9)
       g2=random.randint(0,9)
       g3=random.randint(0,9)
       g4=random.randint(0,9)
       c1 = c[g1]
       c2 = c[g2]
       c3 = c[g3]
       c4 = c[g4]
       user = c1+c2+c3+c4
       g1=random.randint(0,9)
       g2=random.randint(0,9)
       g3=random.randint(0,9)
       g4=random.randint(0,9)
       c1 = c[g1]
       c2 = c[g2]
       c3 = c[g3]
       c4 = c[g4]
       pw = c1+c2+c3+c4
       user=user+":"+pw 
       print(i," = ",user)
       f = open(filename, "a")
       f.write(user)
       f.write("\n")
       f.close()
       i += 1

    x = input("\nPress Enter To Exit...")

    quit()


if menu=="30":
    c =     ["1","2","3","4","5","6","7","8","9","0"," "]


    print(" ")
    print(" ")

# To take input from the user,
    n = int(input("Enter number of combos to generate :   "))
    print (" ")
    print ("Enter the name of the file you want to save  ")
    print ("No need to enter the .txt ")
    filename = input("example combos     :  ")
    filename = filename + ".txt"
    print (" ")

# reset filename

    f = open(filename, "w")
    f.write("")
    f.close()

    i = 1

    while i <= n:
       g1=random.randint(0,9)
       g2=random.randint(0,9)
       g3=random.randint(0,9)
       g4=random.randint(0,9)
       g5=random.randint(0,9)
       c1 = c[g1]
       c2 = c[g2]
       c3 = c[g3]
       c4 = c[g4]
       c5 = c[g5]
       user = c1+c2+c3+c4+c5
       g1=random.randint(0,9)
       g2=random.randint(0,9)
       g3=random.randint(0,9)
       g4=random.randint(0,9)
       g5=random.randint(0,9)
       c1 = c[g1]
       c2 = c[g2]
       c3 = c[g3]
       c4 = c[g4]
       c5 = c[g5]
       pw = c1+c2+c3+c4+c5
       user=user+":"+pw 
       print(i," = ",user)
       f = open(filename, "a")
       f.write(user)
       f.write("\n")
       f.close()
       i += 1

    x = input("\nPress Enter To Exit...")

    quit()



if menu=="31":
    c =     ["1","2","3","4","5","6","7","8","9","0"," "]


    print(" ")
    print(" ")

# To take input from the user,
    n = int(input("Enter number of combos to generate :   "))
    print (" ")
    print ("Enter the name of the file you want to save  ")
    print ("No need to enter the .txt ")
    filename = input("example combos     :  ")
    filename = filename + ".txt"
    print (" ")

# reset filename

    f = open(filename, "w")
    f.write("")
    f.close()

    i = 1

    while i <= n:
       g1=random.randint(0,9)
       g2=random.randint(0,9)
       g3=random.randint(0,9)
       g4=random.randint(0,9)
       g5=random.randint(0,9)
       g6=random.randint(0,9)
       c1 = c[g1]
       c2 = c[g2]
       c3 = c[g3]
       c4 = c[g4]
       c5 = c[g5]
       c6 = c[g6]
       user = c1+c2+c3+c4+c5+c6
       g1=random.randint(0,9)
       g2=random.randint(0,9)
       g3=random.randint(0,9)
       g4=random.randint(0,9)
       g5=random.randint(0,9)
       g6=random.randint(0,9)
       c1 = c[g1]
       c2 = c[g2]
       c3 = c[g3]
       c4 = c[g4]
       c5 = c[g5]
       c6 = c[g6]
       pw = c1+c2+c3+c4+c5+c6
       user=user+":"+pw 
       print(i," = ",user)
       f = open(filename, "a")
       f.write(user)
       f.write("\n")
       f.close()
       i += 1

    x = input("\nPress Enter To Exit...")

    quit()  





if menu=="32":
    c =     ["1","2","3","4","5","6","7","8","9","0"," "]


    print(" ")
    print(" ")

# To take input from the user,
    n = int(input("Enter number of combos to generate :   "))
    print (" ")
    print ("Enter the name of the file you want to save  ")
    print ("No need to enter the .txt ")
    filename = input("example combos     :  ")
    filename = filename + ".txt"
    print (" ")

# reset filename

    f = open(filename, "w")
    f.write("")
    f.close()

    i = 1

    while i <= n:
       g1=random.randint(0,9)
       g2=random.randint(0,9)
       g3=random.randint(0,9)
       g4=random.randint(0,9)
       g5=random.randint(0,9)
       g6=random.randint(0,9)
       g7=random.randint(0,9)
       c1 = c[g1]
       c2 = c[g2]
       c3 = c[g3]
       c4 = c[g4]
       c5 = c[g5]
       c6 = c[g6]
       c7 = c[g7]
       user = c1+c2+c3+c4+c5+c6+c7
       g1=random.randint(0,9)
       g2=random.randint(0,9)
       g3=random.randint(0,9)
       g4=random.randint(0,9)
       g5=random.randint(0,9)
       g6=random.randint(0,9)
       g7=random.randint(0,9)
       c1 = c[g1]
       c2 = c[g2]
       c3 = c[g3]
       c4 = c[g4]
       c5 = c[g5]
       c6 = c[g6]
       c7 = c[g7]
       pw = c1+c2+c3+c4+c5+c6+c7
       user=user+":"+pw 
       print(i," = ",user)
       f = open(filename, "a")
       f.write(user)
       f.write("\n")
       f.close()
       i += 1

    x = input("\nPress Enter To Exit...")

    quit()  


if menu=="33":
    c =     ["1","2","3","4","5","6","7","8","9","0"," "]


    print(" ")
    print(" ")

# To take input from the user,
    n = int(input("Enter number of combos to generate :   "))
    print (" ")
    print ("Enter the name of the file you want to save  ")
    print ("No need to enter the .txt ")
    filename = input("example combos     :  ")
    filename = filename + ".txt"
    print (" ")

# reset filename

    f = open(filename, "w")
    f.write("")
    f.close()

    i = 1

    while i <= n:
       g1=random.randint(0,9)
       g2=random.randint(0,9)
       g3=random.randint(0,9)
       g4=random.randint(0,9)
       g5=random.randint(0,9)
       g6=random.randint(0,9)
       g7=random.randint(0,9)
       g8=random.randint(0,9)
       c1 = c[g1]
       c2 = c[g2]
       c3 = c[g3]
       c4 = c[g4]
       c5 = c[g5]
       c6 = c[g6]
       c7 = c[g7]
       c8 = c[g8]
       user = c1+c2+c3+c4+c5+c6+c7+c8
       g1=random.randint(0,9)
       g2=random.randint(0,9)
       g3=random.randint(0,9)
       g4=random.randint(0,9)
       g5=random.randint(0,9)
       g6=random.randint(0,9)
       g7=random.randint(0,9)
       g8=random.randint(0,9)
       c1 = c[g1]
       c2 = c[g2]
       c3 = c[g3]
       c4 = c[g4]
       c5 = c[g5]
       c6 = c[g6]
       c7 = c[g7]
       c8 = c[g8]
       pw = c1+c2+c3+c4+c5+c6+c7+c8
       user=user+":"+pw 
       print(i," = ",user)
       f = open(filename, "a")
       f.write(user)
       f.write("\n")
       f.close()
       i += 1

    x = input("\nPress Enter To Exit...")

    quit() 


if menu=="34":
    c =     ["1","2","3","4","5","6","7","8","9","0"," "]


    print(" ")
    print(" ")

# To take input from the user,
    n = int(input("Enter number of combos to generate :   "))
    print (" ")
    print ("Enter the name of the file you want to save  ")
    print ("No need to enter the .txt ")
    filename = input("example combos     :  ")
    filename = filename + ".txt"
    print (" ")

# reset filename

    f = open(filename, "w")
    f.write("")
    f.close()

    i = 1

    while i <= n:
       g1=random.randint(0,9)
       g2=random.randint(0,9)
       g3=random.randint(0,9)
       g4=random.randint(0,9)
       g5=random.randint(0,9)
       g6=random.randint(0,9)
       g7=random.randint(0,9)
       g8=random.randint(0,9)
       g9=random.randint(0,9)
       c1 = c[g1]
       c2 = c[g2]
       c3 = c[g3]
       c4 = c[g4]
       c5 = c[g5]
       c6 = c[g6]
       c7 = c[g7]
       c8 = c[g8]
       c9 = c[g9]
       user = c1+c2+c3+c4+c5+c6+c7+c8+c9
       g1=random.randint(0,9)
       g2=random.randint(0,9)
       g3=random.randint(0,9)
       g4=random.randint(0,9)
       g5=random.randint(0,9)
       g6=random.randint(0,9)
       g7=random.randint(0,9)
       g8=random.randint(0,9)
       g9=random.randint(0,9)
       c1 = c[g1]
       c2 = c[g2]
       c3 = c[g3]
       c4 = c[g4]
       c5 = c[g5]
       c6 = c[g6]
       c7 = c[g7]
       c8 = c[g8]
       c9 = c[g9]
       pw = c1+c2+c3+c4+c5+c6+c7+c8+c9
       user=user+":"+pw 
       print(i," = ",user)
       f = open(filename, "a")
       f.write(user)
       f.write("\n")
       f.close()
       i += 1

    x = input("\nPress Enter To Exit...")

    quit() 


if menu=="35":
    c =     ["1","2","3","4","5","6","7","8","9","0"," "]


    print(" ")
    print(" ")

# To take input from the user,
    n = int(input("Enter number of combos to generate :   "))
    print (" ")
    print ("Enter the name of the file you want to save  ")
    print ("No need to enter the .txt ")
    filename = input("example combos     :  ")
    filename = filename + ".txt"
    print (" ")

# reset filename

    f = open(filename, "w")
    f.write("")
    f.close()

    i = 1

    while i <= n:
       g1=random.randint(0,9)
       g2=random.randint(0,9)
       g3=random.randint(0,9)
       g4=random.randint(0,9)
       g5=random.randint(0,9)
       g6=random.randint(0,9)
       g7=random.randint(0,9)
       g8=random.randint(0,9)
       g9=random.randint(0,9)
       g10=random.randint(0,9)
       c1 = c[g1]
       c2 = c[g2]
       c3 = c[g3]
       c4 = c[g4]
       c5 = c[g5]
       c6 = c[g6]
       c7 = c[g7]
       c8 = c[g8]
       c9 = c[g9]
       c10 = c[g10]
       user = c1+c2+c3+c4+c5+c6+c7+c8+c9+c10
       g1=random.randint(0,9)
       g2=random.randint(0,9)
       g3=random.randint(0,9)
       g4=random.randint(0,9)
       g5=random.randint(0,9)
       g6=random.randint(0,9)
       g7=random.randint(0,9)
       g8=random.randint(0,9)
       g9=random.randint(0,9)
       g10=random.randint(0,9)
       c1 = c[g1]
       c2 = c[g2]
       c3 = c[g3]
       c4 = c[g4]
       c5 = c[g5]
       c6 = c[g6]
       c7 = c[g7]
       c8 = c[g8]
       c9 = c[g9]
       c10 = c[g10]
       pw = c1+c2+c3+c4+c5+c6+c7+c8+c9+c10
       user=user+":"+pw 
       print(i," = ",user)
       f = open(filename, "a")
       f.write(user)
       f.write("\n")
       f.close()
       i += 1

    x = input("\nPress Enter To Exit...")

    quit() 



if menu=="36":
    c =     ["1","2","3","4","5","6","7","8","9","0"," "]


    print(" ")
    print(" ")

# To take input from the user,
    n = int(input("Enter number of combos to generate :   "))
    print (" ")
    print ("Enter the name of the file you want to save  ")
    print ("No need to enter the .txt ")
    filename = input("example combos     :  ")
    filename = filename + ".txt"
    print (" ")

# reset filename

    f = open(filename, "w")
    f.write("")
    f.close()

    i = 1

    while i <= n:
       g1=random.randint(0,9)
       g2=random.randint(0,9)
       g3=random.randint(0,9)
       g4=random.randint(0,9)
       g5=random.randint(0,9)
       g6=random.randint(0,9)
       g7=random.randint(0,9)
       g8=random.randint(0,9)
       g9=random.randint(0,9)
       g10=random.randint(0,9)
       g11=random.randint(0,9)
       g12=random.randint(0,9)
       c1 = c[g1]
       c2 = c[g2]
       c3 = c[g3]
       c4 = c[g4]
       c5 = c[g5]
       c6 = c[g6]
       c7 = c[g7]
       c8 = c[g8]
       c9 = c[g9]
       c10 = c[g10]
       c11 = c[g11]
       c12 = c[g12]
       user = c1+c2+c3+c4+c5+c6+c7+c8+c9+c10+c11+c12
       g1=random.randint(0,9)
       g2=random.randint(0,9)
       g3=random.randint(0,9)
       g4=random.randint(0,9)
       g5=random.randint(0,9)
       g6=random.randint(0,9)
       g7=random.randint(0,9)
       g8=random.randint(0,9)
       g9=random.randint(0,9)
       g10=random.randint(0,9)
       g11=random.randint(0,9)
       g12=random.randint(0,9)
       c1 = c[g1]
       c2 = c[g2]
       c3 = c[g3]
       c4 = c[g4]
       c5 = c[g5]
       c6 = c[g6]
       c7 = c[g7]
       c8 = c[g8]
       c9 = c[g9]
       c10 = c[g10]
       c11 = c[g11]
       c12 = c[g12]
       pw = c1+c2+c3+c4+c5+c6+c7+c8+c9+c10+c11+c12
       user=user+":"+pw 
       print(i," = ",user)
       f = open(filename, "a")
       f.write(user)
       f.write("\n")
       f.close()
       i += 1

    x = input("\nPress Enter To Exit...")

    quit() 

if menu=="37":
    c =     ["1","2","3","4","5","6","7","8","9","0"," "]


    print(" ")
    print(" ")

# To take input from the user,
    n = int(input("Enter number of combos to generate :   "))
    print (" ")
    print ("Enter the name of the file you want to save  ")
    print ("No need to enter the .txt ")
    filename = input("example combos     :  ")
    filename = filename + ".txt"
    print (" ")

# reset filename

    f = open(filename, "w")
    f.write("")
    f.close()

    i = 1

    while i <= n:
       g1=random.randint(0,9)
       g2=random.randint(0,9)
       g3=random.randint(0,9)
       g4=random.randint(0,9)
       g5=random.randint(0,9)
       g6=random.randint(0,9)
       g7=random.randint(0,9)
       g8=random.randint(0,9)
       g9=random.randint(0,9)
       g10=random.randint(0,9)
       g11=random.randint(0,9)
       g12=random.randint(0,9)
       g13=random.randint(0,9)
       g14=random.randint(0,9)
       g15=random.randint(0,9)
       c1 = c[g1]
       c2 = c[g2]
       c3 = c[g3]
       c4 = c[g4]
       c5 = c[g5]
       c6 = c[g6]
       c7 = c[g7]
       c8 = c[g8]
       c9 = c[g9]
       c10 = c[g10]
       c11 = c[g11]
       c12 = c[g12]
       c13 = c[g13]
       c14 = c[g14]
       c15 = c[g15]
       user = c1+c2+c3+c4+c5+c6+c7+c8+c9+c10+c11+c12+c13+c14+c15
       g1=random.randint(0,9)
       g2=random.randint(0,9)
       g3=random.randint(0,9)
       g4=random.randint(0,9)
       g5=random.randint(0,9)
       g6=random.randint(0,9)
       g7=random.randint(0,9)
       g8=random.randint(0,9)
       g9=random.randint(0,9)
       g10=random.randint(0,9)
       g11=random.randint(0,9)
       g12=random.randint(0,9)
       g13=random.randint(0,9)
       g14=random.randint(0,9)
       g15=random.randint(0,9)
       c1 = c[g1]
       c2 = c[g2]
       c3 = c[g3]
       c4 = c[g4]
       c5 = c[g5]
       c6 = c[g6]
       c7 = c[g7]
       c8 = c[g8]
       c9 = c[g9]
       c10 = c[g10]
       c11 = c[g11]
       c12 = c[g12]
       c13 = c[g13]
       c14 = c[g14]
       c15 = c[g15]
       pw = c1+c2+c3+c4+c5+c6+c7+c8+c9+c10+c11+c12+c13+c14+c15
       user=user+":"+pw 
       print(i," = ",user)
       f = open(filename, "a")
       f.write(user)
       f.write("\n")
       f.close()
       i += 1

    x = input("\nPress Enter To Exit...")

    quit() 

