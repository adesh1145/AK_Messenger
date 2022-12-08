# import name_page
# NAME Page
from threading import Thread
from tkinter import *
import socket

#------------define window----------
root=Tk()
root.title("AK. Messenger")
root.geometry("1080x700")

#------------------SIGNUP PAGE--------------------

def signupPage():
    remove_window()
    global f2
    head1=Label(root,text='--Welcome AK. Messenger--\n\nSignup Page',font=("",30,"bold")).place(relx=0.5, rely=0.1, anchor=CENTER)
    f2=Frame(root,bg="grey",padx=50,pady=10)
    f2.pack(pady=200)


    name_label1=Label(f2,text="Name:",font=("",20),padx=7,pady=7,bg="grey")
    name_label1.grid(row=1,column=0)
    number_label1=Label(f2,text="Number:",font=("",20),padx=7,pady=7,bg="grey")
    number_label1.grid(row=2,column=0)
    pass_label1=Label(f2,text="Password:",font=("",20),padx=7,pady=7,bg="grey")
    pass_label1.grid(row=3,column=0)
    pass1_label1=Label(f2,text="Confirm Password:",font=("",20),padx=7,pady=7,bg="grey")
    pass1_label1.grid(row=4,column=0)
   
    num_value=StringVar()
    name_value=StringVar()
    pass_value=StringVar()
    pass1_value=StringVar()
    
    name_entry1=Entry(f2,textvariable=name_value,font=("",20))
    name_entry1.grid(row=1,column=1)
    num_entry1=Entry(f2,textvariable=num_value,font=("",20))
    num_entry1.grid(row=2,column=1)
    pass_entry1=Entry(f2,textvariable=pass_value,show="*",font=("",20))
    pass_entry1.grid(row=3,column=1)
    pass1_entry1=Entry(f2,textvariable=pass1_value,show="*",font=("",20))
    pass1_entry1.grid(row=4,column=1)

    signup_button=Button(f2,text="Next👉",font=("",20),command=lambda:signupLogic(num_value,name_value,pass_value,pass1_value))
    signup_button.grid(row=5,column=1)
    
    login_button=Button(f2,text="Log In",font=("",10),command=lambda:loginPage())
    login_button.grid(row=6,column=1)


#-------------SIGNUP PAGE LOGIC--=---------
def signupLogic(num_value,name_value,pass_value,pass1_value):

    number=num_value.get()
    name=name_value.get()
    passwd = pass_value.get()
    passwd1=pass1_value.get()
    # print(len(number))
    if passwd !=passwd1:
    
        warning_label=Label(f2,text="Password Doesn't Match",font=("",12),padx=10,pady=10,bg="grey",fg="red")
        warning_label.grid(row=0,column=0)
    
    elif len(number)==10 and len(passwd)>3:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(("127.0.0.1",5501))
        # client.connect(("147.185.221.194",43574))
        data=number+passwd+","+name
        client.send(data.encode())
        
        #print(data)
        warning_msg1=client.recv(1024).decode()
        # print(warning_msg1)
        if len(warning_msg1)>22:
            remove_window()
            signupPage()
            warning_label=Label(f2,text=f"{warning_msg1}",font=("",12),padx=10,pady=10,bg="grey",fg="red")
            warning_label.grid(row=0,column=0)
        else:
            remove_window()
            signupOtpPage(warning_msg1,client)
    else:
        warning_label=Label(f2,text="Please Fill 10 Digit No. and Password",font=("",12),padx=10,pady=10,bg="grey",fg="red")
        warning_label.grid(row=0,column=0)        
#------------------OTP PAGE--------------------
def signupOtpPage(warning_msg1,client):
    global f9
    head1=Label(root,text='--Welcome AK. Messenger--\n\nOTP Page',font=("",30,"bold")).place(relx=0.5, rely=0.1, anchor=CENTER)
    f9=Frame(root,bg="grey",padx=50,pady=10)
    f9.pack(pady=200)
    otp_value=StringVar()
    warning_label=Label(f9,text=f"Please enter the OTP sent to {warning_msg1}",font=("",12),padx=10,pady=10,bg="grey",fg="green")
    warning_label.grid(row=0,column=0)
    otp_entry=Entry(f9,textvariable=otp_value,show="*",font=("",20),width=10)
    otp_entry.grid(row=2,column=0)
    otp_button=Button(f9,text="SUBMIT",font=("",20),command=lambda:signupOtpLogic(otp_value,client))
    otp_button.grid(row=3,column=0)

    signup_button=Button(f9,text="Sign Up",font=("",10),command=lambda:signupPage())
    signup_button.grid(row=4,column=0)

#------------------OTP PAGE LOGIC --------------------

def signupOtpLogic(otp_value,client):
    otp_value=otp_value.get()
    client.send(otp_value.encode())
    warning_msg1=client.recv(1024).decode()
    if warning_msg1=="Successful SignUp":
        remove_window()
        loginPage()
    else:
        warning_label=Label(f9,text=f"{warning_msg1}",font=("",12),padx=10,pady=10,bg="grey",fg="red")
        warning_label.grid(row=1,column=0)

#------------------FORGET NUMBER PAGE--------------------

def forgetnumberPage():
    remove_window()
    num_value8=StringVar()
    global f8
    head=Label(root,text='--Welcome AK. Messenger--\n\nForget Page',font=("",30,"bold")).place(relx=0.5, rely=0.1, anchor=CENTER)
    f8=Frame(root,bg="grey",padx=50,pady=50)
    f8.pack(pady=200)
    # warning_label=Label(f8,text=f"{warning_msg}",font=("",12),padx=10,pady=10,bg="grey",fg="red")
    # warning_label.grid(row=0,column=0)
    number_label=Label(f8,text="Number:",font=("",20),padx=10,pady=10,bg="grey")
    number_label.grid(row=1,column=0)
    name_entry=Entry(f8,textvariable=num_value8,font=("",20))
    name_entry.grid(row=1,column=1)
    submit_button=Button(f8,text="Submit",font=("",20),command=lambda:forgetnumberLogic(num_value8))
    submit_button.grid(row=2,column=1)
    login_button=Button(f8,text="Login Page",font=("",10),command=lambda:loginPage())
    login_button.grid(row=2,column=0)

#------------------FORGET NUMBER PAGE LOGIC--------------------

def forgetnumberLogic(num_value8):
    num_value8=num_value8.get()
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1",5501))
    # client.connect(("147.185.221.194",43574))
    # print("99")

    if len(num_value8)!=10:
        warning_label=Label(f8,text=f"Please Fill 10 Digit No.",font=("",12),padx=10,pady=10,bg="grey",fg="red")
        warning_label.grid(row=0,column=0)
    else:
        # print("98")
        # SEND NUMBER
        # num_value8=num_value8+"|"
        client.send(num_value8.encode())
        # print("97")
        warning_msg1=client.recv(1024).decode()
        # print("96")
        if warning_msg1=="No User Exist This Number!":
            # print("95")
            remove_window()
            forgetnumberPage()
            warning_label=Label(f8,text=f"{warning_msg1}",font=("",12),padx=10,pady=10,bg="grey",fg="red")
            warning_label.grid(row=0,column=0)
            # print("94")
        else:
            remove_window()
            forgetOtpPage(warning_msg1,client)


def forgetOtpPage(warning_msg1,client):
    global f7
    head1=Label(root,text='--Welcome AK. Messenger--\n\nOTP Page',font=("",30,"bold")).place(relx=0.5, rely=0.1, anchor=CENTER)
    f7=Frame(root,bg="grey",padx=50,pady=10)
    f7.pack(pady=200)
    otp_value=StringVar()
    warning_label=Label(f7,text=f"Please enter the OTP sent to {warning_msg1}",font=("",12),padx=10,pady=10,bg="grey",fg="green")
    warning_label.grid(row=0,column=0)
    otp_entry=Entry(f7,textvariable=otp_value,font=("",20),width=10)
    otp_entry.grid(row=2,column=0)
    otp_button=Button(f7,text="SUBMIT",font=("",20),command=lambda:forgetOtpLogic(otp_value,client))
    otp_button.grid(row=3,column=0)

    login_button=Button(f7,text="Log In",font=("",10),command=lambda:loginPage())
    login_button.grid(row=4,column=0)

def forgetOtpLogic(otp_value,client):
    otp_value=otp_value.get()
    client.send(otp_value.encode())
    warning_msg1=client.recv(1024).decode()
    if warning_msg1=="OTP Verified !":
        remove_window()
        createNewPasswordPage(warning_msg,client)
    else:
        warning_label=Label(f7,text=f"{warning_msg1}",font=("",12),padx=10,pady=10,bg="grey",fg="red")
        warning_label.grid(row=1,column=0)   


def createNewPasswordPage(warning_msg,client):
    global f6
    pass1=StringVar()
    pass2=StringVar()

    head1=Label(root,text='--Welcome AK. Messenger--\n\nOTP Page',font=("",30,"bold")).place(relx=0.5, rely=0.1, anchor=CENTER)
    f6=Frame(root,bg="grey",padx=50,pady=10)
    f6.pack(pady=200)

    warning_label=Label(f6,text=f"{warning_msg}",font=("",12),padx=10,pady=10,bg="grey",)
    warning_label.grid(row=0,column=0)

    pass1_label=Label(f6,text=f"New Password:",font=("",12),padx=10,pady=10,bg="grey",)
    pass1_label.grid(row=1,column=0)
    pass2_label=Label(f6,text=f"Re-enter Password:",font=("",12),padx=10,pady=10,bg="grey",fg="green")
    pass2_label.grid(row=2,column=0)

    pass1_entry=Entry(f6,textvariable=pass1,show="*",font=("",20))
    pass1_entry.grid(row=1,column=1)
    pass2_entry=Entry(f6,textvariable=pass2,show="*",font=("",20))
    pass2_entry.grid(row=2,column=1)
    submit_button=Button(f6,text="SUBMIT",font=("",20),command=lambda:createNewPasswordLogic(pass1,pass2,client))
    submit_button.grid(row=3,column=1)

def createNewPasswordLogic(pass1,pass2,client):
    pass1=pass1.get()
    pass2=pass2.get()
    if pass1 !=pass2:
        warning_label=Label(f6,text=f"Password Doesn't Match!",font=("",12),padx=10,pady=10,bg="grey",fg="red")
        warning_label.grid(row=0,column=0)
    
    else:
        client.send(pass1.encode())
        remove_window()
        loginPage()
        




#--------------LOGIN PAGE-----------------
def loginPage():
    # print("1")
    remove_window()
    global f1
    global warning_msg
    global warning_label
    warning_msg=""
    # print("2")
    head=Label(root,text='--Welcome AK. Messenger--\n\nLogIn Page',font=("",30,"bold")).place(relx=0.5, rely=0.1, anchor=CENTER)
    f1=Frame(root,bg="grey",padx=50,pady=50)
    f1.pack(pady=200)
    # print("11")

    warning_label=Label(f1,text=f"{warning_msg}",font=("",12),padx=10,pady=10,bg="grey",fg="red")
    warning_label.grid(row=0,column=0)
    # print("12")

    number_label=Label(f1,text="Number:",font=("",20),padx=10,pady=10,bg="grey")
    number_label.grid(row=1,column=0)
    pass_label=Label(f1,text="Password:",font=("",20),padx=10,pady=10,bg="grey")
    pass_label.grid(row=2,column=0)
    num_value=StringVar()
    pass_value=StringVar()
    # print("13")
    name_entry=Entry(f1,textvariable=num_value,font=("",20))
    name_entry.grid(row=1,column=1)
    pass_entry=Entry(f1,textvariable=pass_value,show="*",font=("",20))
    pass_entry.grid(row=2,column=1)
    # print("14")
    login_button=Button(f1,text="Sign In",font=("",20),command=lambda:loginLogic(num_value,pass_value))
    login_button.grid(row=3,column=1)
    signup_button=Button(f1,text="Sign Up",font=("",10),command=lambda:signupPage())
    signup_button.grid(row=4,column=1)
    forget_button=Button(f1,text="Forget Password",font=("",10),command=lambda:forgetnumberPage())
    forget_button.grid(row=4,column=0)
    # print("15")


#------------LOGIN PAGE LOGIC---------------------
def loginLogic(num_value,pass_value):
    # print("3")
    loginPage()
    # print("4")
    global number
    global passwd
    number=num_value.get()
    passwd = pass_value.get()
    # print("5")
    if len(number)==10 and len(passwd)>0:
    #print(number+passwd)
        global client
        # client=""
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # client.connect(("147.185.221.194",43574))
        client.connect(("127.0.0.1",5501))
        
        
        data=number+passwd
        try:
            client.send(data.encode())
            warning_msg=client.recv(1024).decode()
            #print(warning_msg)
            if len(warning_msg)>20:
                
                warning_label=Label(f1,text=f"{warning_msg}",font=("",12),padx=10,pady=10,bg="grey",fg="red")
                warning_label.grid(row=0,column=0)
            else:
                warning_label=Label(f1,text=f"{warning_msg}",font=("",12),padx=10,pady=10,bg="grey",fg="green")
                warning_label.grid(row=0,column=0)
                # remove_window() 
                numberPage()
                # root.mainloop() 
        except:
            client.close()
            root.destroy()
    else:
        warning_label=Label(f1,text="Please Fill 10 Digit No. and Password",font=("",12),padx=10,pady=10,bg="grey",fg="red")
        warning_label.grid(row=0,column=0) 

#------------------NUMBER PAGE--------------------

def numberPage():
        remove_window()
        # print("12")
        global f3
        global warning_msg2
        warning_msg2=""
        head1=Label(root,text='--Welcome AK Messenger--\n\n Enter Friend Number',font=("",30,"bold")).place(relx=0.5, rely=0.1, anchor=CENTER)
        f3=Frame(root,bg="grey",padx=50,pady=10)
        f3.pack(pady=200)


        warning_label=Label(f3,text=f"{warning_msg2}",font=("",12),padx=10,pady=10,bg="grey",fg="red")
        warning_label.grid(row=0,column=0)
        number_label2=Label(f3,text="Number:",font=("",20),padx=7,pady=7,bg="grey")
        number_label2.grid(row=1,column=0)
        num_value=StringVar()
        
        num_entry2=Entry(f3,textvariable=num_value,font=("",20))
        num_entry2.grid(row=1,column=1)
        enter_button=Button(f3,text="Enter",font=("",20),command=lambda:numLogic(num_value.get()))
        enter_button.grid(row=2,column=1)
        # logout_button=Button(f3,text="Logout",font=("",10),command=lambda:logout())
        # logout_button.grid(row=4,column=1)
       
#------------------NUMBER PAGE LOGIC--------------------
        
def numLogic(num_value):
    numberPage()
    # print("11")
    try:
        # print("13")
        client.send(num_value.encode())
        warning_msg2=client.recv(1024).decode()
        #print(warning_msg2)
        if len(warning_msg2)>30:
            # print("14")
            warning_label=Label(f3,text=f"{warning_msg2}",font=("",12),padx=10,pady=10,bg="grey",fg="red")
            warning_label.grid(row=0,column=0)
                        
                    
        else:
            
            # print("15") 
            warning_label=Label(f3,text=f"{warning_msg2}",font=("",12),padx=10,pady=10,bg="grey",fg="green")
            warning_label.grid(row=0,column=0)
            remove_window()
            

            f4=Frame(root,bg="grey",padx=50,pady=10)
            f4.pack()


            # send_button=Button(root,text="🔙\nBack",font=("",20),command=lambda:numberPage())
            # send_button.place(x=0,y=0,height=100,width=100)
            # up_button=Button(root,text="📤\nLogOut",font=("",20),command=lambda:logout())
            # up_button.place(x=980,y=0,height=100,width=100)


            name_label=Label(f4,text=f"{warning_msg2[:10]+' '+warning_msg2[10:]}",font=("",20),padx=10,pady=10,bg="grey",fg="black")
            name_label.grid(row=0,column=0)

            scroll=Scrollbar(root)
            scroll.place(y=1060,height=600)
            global msg_entry
            global mylist
            mylist=Listbox(root,yscrollcommand=scroll.set,font=("",20))
            mylist.place(x=0,y=100,height=500,width=1060)
            scroll.config(command=mylist.yview)

            msg_entry=Text(root,font=("",20))
            msg_entry.place(x=0,y=600,height=100,width=1080)
            send_button=Button(root,text="⏩\nSend",font=("",20),command=lambda:send_chat(client,warning_msg))
            send_button.place(x=980,y=600,height=100,width=100)
            # print("16")
            thread=Thread(target=update_chat_page,args=(client,))
            thread.start()
    except:
        # print("close")
        client.close()
        root.destroy()


            
#------------------SEND CHAT SERVER--------------------

def send_chat(client,warning_msg):
    
    msg=msg_entry.get(1.0, "end-1c")
    try:
        if msg !="":
            msg='You: '+msg
            # print(msg)
            # print(warning_msg)
            # print("send Press")
            client.send(f"{msg}".encode())
            # print("sms sent")
            
            msg_entry.delete(1.0, "end")
    except:
            client.close()
            root.destroy()
            # pass
#------------------UPDATE CHAT PAGE--------------------

def update_chat_page(client):
    chat_status=True
    global logout_status
    logout_status=False
    while True:
       
        try:
            if chat_status:
                # print("17")
                msg=client.recv(1024).decode()
                
                msg=[i for i in msg.split("\n")]
                # print(msg)
                for i in range(0,len(msg)):
                    if msg[i][:5]=='You: ':
                        msg[i]="                                                                "+msg[i]
                        mylist.insert(i,f"{msg[i]}")
                        mylist.yview(END)
                    else:
                        mylist.insert(i,f"{msg[i]}")
                        mylist.yview(END)
                chat_status= False
            
        except:
            # print("18")
            client.close()
            root.destroy()
            break

        try:
            #print("19")
            msg=client.recv(1024).decode()
            if msg[:5]=='You: ':
                            msg="                                                                "+msg
                            mylist.insert(END,f"{msg}")
                            mylist.yview(END)
            else:
                mylist.insert(END,f"{msg}")
                mylist.yview(END)
            
        except:
            client.close()
            root.destroy()
            break
            # pass
        if logout_status:
            # print("Logout")
            break  

#------------------REMOVE WINDOW--------------------

def remove_window():
    for widgets in root.winfo_children():
      widgets.destroy()

#-------------LOGOUT-------------
# def logout():
#     logout_status=False
#     client.close()
#     # print("logout1")
#     loginPage()


#------------------DRIVER--------------------    

loginPage()
root.mainloop()




