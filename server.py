import socket
import multiprocessing
import mysql.connector as sc
from threading import Thread
import random
import requests




#---------------OTP GENERATOR---------
def otpGenerate(sender_number):
    OTP=""
    for i in range(0,4):
        random_value=random.randint(0,9)
        OTP+=str(random_value)
    # accoun_sid="AC3897441ef8c3909eeceb619413f43f15"
    # auth_token="2c83d598b9c9c9f6d5f0ff1cf0fd29c7"

    # client=Client(accoun_sid,auth_token)

    # message=client.messages.create(
    # body=f"Welcome TO AK Messenger! Your OTP is {OTP}",
    # from_="+17179876727",
    # to=f"+91{sender_number}"
    # )

    # print(message.sid)
    return '1234'

#---------------CONNECTION PROCESS---------
def connection_process(server,k):
   
   
    global client
    global count
    global sender_number
    global sender_password
    global all_client
    all_client={}
    print("Waiting for Connection......")
    client,addr=server.accept()
    print("Connection are Established.....")
    print(client,addr)
   
    data=client.recv(1024).decode()
    sender_number=data[:10]
    sender_password=data[10:]
    sender_name=""
    key=''
    # count=0
    for i in range(0,len(data)):
        if data[i]==",":
            count=i
            key='signup'
    # print("hii")
    # print(len(data))
    if key=='signup':
        # print("1")
        sender_password=data[10:count]
        signupLogic(data)
    #-------------FORGET LOGIC------------
    
    elif len(data)==10:

        forgetLogic()

    # -----------LOGIN LOGIC--------------
    elif len(data)>10:
        loginLogic(k)
    print(sender_number,sender_password)


#---------------SIGN UP PAGE LOGIC---------

def signupLogic(data):
    # print("2")
    name=data[count+1:]
    mydb=sc.connect(host='localhost',user='root',passwd='admin',database='data')
    cur=mydb.cursor()
    s="SELECT * FROM UserDetail"
    cur.execute(s)
    # print("3")
    result=cur.fetchall()
    flag1=True
    for i in result:
        if i[0]==sender_number:
            flag1=False
            # print("4")
            
            warning_msg="This Number Is Already Exist !"
            warning_msg=client.send(warning_msg.encode())
            # break
    # print("5")
    if flag1:
        otp_generated=otpGenerate(sender_number)
        warning_msg=f"{sender_number}"
        warning_msg=client.send(warning_msg.encode())
        while True:
            otp_value=client.recv(1024).decode()

            if otp_value==otp_generated:
                warning_msg="Successful SignUp"
                warning_msg=client.send(warning_msg.encode())
                mydb=sc.connect(host='localhost',user='root',passwd='admin',database='data')
                cur=mydb.cursor()
                data=(sender_number,name,sender_password)
                s="INSERT INTO UserDetail (Number,Name,Password) VALUES (%s,%s,%s)"
                cur.execute(s,data)
                mydb.commit()
                break
            else:
                warning_msg="Incorrect OTP"
                warning_msg=client.send(warning_msg.encode())

#---------------FORGET PAGE LOGIC---------

def forgetLogic():
    mydb=sc.connect(host='localhost',user='root',passwd='admin',database='data')
    cur=mydb.cursor()
    s="SELECT * FROM UserDetail"
    cur.execute(s)
    print("3")
    result=cur.fetchall()
    flag1=False
    for i in result:
        if i[0]==sender_number:
            flag1=True
            print("4")
            break
    if flag1:
        print("5")
        otp_generated=otpGenerate(sender_number)
        warning_msg=f"{sender_number}"
        warning_msg=client.send(warning_msg.encode())
        while True:
            otp_value=client.recv(1024).decode()

            if otp_value==otp_generated:
                warning_msg="OTP Verified !"
                warning_msg=client.send(warning_msg.encode())
                password=client.recv(1024).decode()
                mydb=sc.connect(host='localhost',user='root',passwd='admin',database='data')
                cur=mydb.cursor()
                data=f"UPDATE UserDetail SET Password = {password} WHERE Number = {sender_number}"
                
                cur.execute(data)
                mydb.commit()
                break
            else:
                warning_msg="Incorrect OTP"
                warning_msg=client.send(warning_msg.encode())
    else:
        print("6")
        warning_msg="No User Exist This Number!"
        warning_msg=client.send(warning_msg.encode())


#---------------LOGIN LOGIC---------


def loginLogic(k):
    try:
        print("100")
        mydb=sc.connect(host='localhost',user='root',passwd='admin',database='data')
        cur=mydb.cursor()
        s="SELECT * FROM UserDetail"
        cur.execute(s)
        result=cur.fetchall()
        flag=False
        print("99")
        
        for i in result:
            
            if i[0]==sender_number and i[2]==sender_password:
                print(i[0],i[2])
                print("98")
                flag=True
                name1=i[1]
                sender_name=""
                for j in name1:
                    if j !=" ":
                        sender_name=sender_name+j
        print("97")
        if flag:
            all_client[client]=sender_name
            
            print(all_client)
            client.send(sender_name.encode())
            print("96")

            
        
            mydb=sc.connect(host='localhost',user='root',passwd='admin',database='data')
            cur=mydb.cursor()
            s="SELECT * FROM UserDetail"
            cur.execute(s)
            result=cur.fetchall()
            # print("1")

            while True:
                flag2=False
                
                friend_num=client.recv(1024).decode()
                for i in result:
                    print(i[0],friend_num)
                    if i[0]==friend_num:
                        print("11")
                        friend_num_name=i[0]+i[1]
                        friend_name=""
                        for j in i[1]:
                            if j !=" ":
                                friend_name=friend_name+j
                        print("2")
                        flag2=True
                       
                if flag2==False:
                    warning_msg="     No User Exist This Number!     "
                    client.send(warning_msg.encode())
                # except:
                #     del all_client[client]
                #     client.close()
                #     break

                
                if flag2:
                    print("12")
                    client.send(friend_num_name.encode())
                    global sender_table_name
                    global receiver_table_name
                    sender_table_name=sender_name+sender_number+friend_num
                    receiver_table_name=friend_name+friend_num+sender_number
                    print(receiver_table_name)
                break
        else:
            warning_msg="Invailid Number or Password"
            # print("1")
            client.send(warning_msg.encode())

 #-----------CREATE TABLE SENDER------------ 
        print("13")    
        try:
            print("yes")          
            mydb=sc.connect(host='localhost',user='root',passwd='admin',database='data')
            cur=mydb.cursor()
            
            cur.execute(f"CREATE TABLE {sender_table_name} (Chat varchar(200),Number integer(10))")
            print(sender_table_name)
        
    #------------CREATE TABLE RECEIVER------

        
            print("14")
            mydb=sc.connect(host='localhost',user='root',passwd='admin',database='data')
            cur=mydb.cursor()
            
            cur.execute(f"CREATE TABLE {receiver_table_name} (Chat varchar(200),Number integer(10))")
            print(receiver_table_name)
        except:
            pass
        
        print("yes1")
        
        
        receive_thread=Thread(target=receive_msg,args=(friend_name,sender_name,))
        receive_thread.start()
        update_thread=Thread(target=update_chat_page)
        update_thread.start()
        # print(chat_page_break)
        # update_chat_page()
    except:       
        client.close()
        pass
        # del all_client[client]
        
#---------------RECEIVE MESSAGE THROUGH USER---------
        
def receive_msg(friend_name,sender_name):
    global chat_sender
    global chat_receiver
    global chat_page_break
    chat_page_break=False
    print("15")
    while True:
#------------RECEIVE MESSAGE THROUGH SENDER---------------
        
        try:
            print("16")
            chat_sender=client.recv(1024).decode()
            print(chat_sender)
            if chat_sender !="":
                chat_receiver=sender_name+": "+chat_sender[5:] 

                print("17")
            #------INSERT CHAT IN SENDER TABLE--------
            
                mydb=sc.connect(host='localhost',user='root',passwd='admin',database='data')
                cur=mydb.cursor()
                s=f"SELECT * FROM {sender_table_name}"
                cur.execute(s)
                result=cur.fetchall()
                
                
                result=len(result)+1


                mydb=sc.connect(host='localhost',user='root',passwd='admin',database='data')
                cur=mydb.cursor()
                chat_sender=[chat_sender,result]
                cur.execute(f"INSERT INTO {sender_table_name} (Chat,Number) VALUES (%s,%s)",chat_sender)
                mydb.commit()
                print("18")
            #------INSERT CHAT IN RECEIVER TABLE--------
                mydb=sc.connect(host='localhost',user='root',passwd='admin',database='data')
                cur=mydb.cursor()
                s=f"SELECT * FROM {receiver_table_name}"
                cur.execute(s)
                result=cur.fetchall()

                result=len(result)+1


                mydb=sc.connect(host='localhost',user='root',passwd='admin',database='data')
                cur=mydb.cursor()

                chat_receiver=[chat_receiver,result]
                cur.execute(f"INSERT INTO {receiver_table_name} (Chat,Number) VALUES (%s,%s)",chat_receiver)
                mydb.commit()
            else:
                
                client.close()
                print("break")
                del all_client[client]
                client.close()    
                break
      
 
        except:
           
            client.close()
            # print("break")
            del all_client[client]
            client.close()
            break
            # pass
    chat_page_break = True
    print("Complete receive_msg")        
            
            
#--------------CHAT PAGE UPDATE LOGIC-------------------- 
def update_chat_page():
    chat_status=True
    
    while True:
        try:              
            if chat_status:

                mydb=sc.connect(host='localhost',user='root',passwd='admin',database='data')
                cur=mydb.cursor()
                s=f"SELECT * FROM {sender_table_name}"
                cur.execute(s)
                result=cur.fetchall()

                for i in range(0,len(result)):
                    client.send((result[i][0]+"\n").encode())
                    print(result[i][0])
                
                chat_status=False
                no_of_chat=len(result)  

            
            mydb=sc.connect(host='localhost',user='root',passwd='admin',database='data')
            cur=mydb.cursor()
            s=f"SELECT * FROM {sender_table_name}"
            cur.execute(s)
            result=cur.fetchall()
                    
            
            if no_of_chat<len(result):
                # print(len(result))
                no_of_chat=no_of_chat+1
                client.send((result[no_of_chat-1][0]+"\n").encode())
        
            if chat_page_break:
                break
        except:
            pass
            
    print("Update_chat_page")        

#---------------DRIVER---------

if __name__ == "__main__":
    
    global multiprocess
    multiprocess=["" for i in range(0,12)]
    multiprocess_status=[ False for i in range(0,12)]
    print(multiprocess)


    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("127.0.0.1",5501))
    server.listen(100)
    
#----------MULTIPROCESS LOGIC-------------------           
      
    for k in range(0,len(multiprocess)):
    
        multiprocess[k]=multiprocessing.Process(target=connection_process,args=(server,k))         
        multiprocess[k].start()
                
    while True:
        for i in range(0,len(multiprocess)):

            if multiprocess[i].is_alive():
                pass
            else:
                print(f"Done {i}")
                
                multiprocess[i]=multiprocessing.Process(target=connection_process,args=(server,k))
                multiprocess[i].start()
                print(f"start {i}")

        
