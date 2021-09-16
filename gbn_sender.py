## sender_gbn

import time
import random
import threading
import socket
from socket import *
from time import sleep





def _time_out():
    print("TIME OUT! RESEND!")
    
def send_error(senderSocket):
    global receiverName
    global receiverPort
    senderSocket.sendto(str(packet).encode('utf8'),(receiverName, receiverPort))

def send_sender():
    global receiverName
    global receiverPort

    global ack
    global seq_num
    global base 
    global sender_window 
    global window_size 
    global next_seq_num

   

    global send 
    global resend 
    global resend_num 
    global count
    global data
    global packet
    
    senderSocket = socket(AF_INET, SOCK_DGRAM) # 소켓 생성
    while True: # 무한루프
        if seq_num ==99:
            while True:
                sender_rcv(senderSocket) # 아직 오지 않은 ack를 받기 위함
            
        
        for i in range(seq_num, next_seq_num+1):
            sendError = random.randint(1, 1000) # 1부터 1000까지 임의의 랜덤 숫자 저장
            if sendError == 10: # 1000분의 1의 확률
                print("S: send pkt", i)
                print("SENDER LOSS")
                _time_out()
                resend.append(i)
                send_error(senderSocket, packet, resend)
                send_sender()
                    
            else: # 손실되지 않았다면 
                data = data + chr(97+i) # data에 계속해서 다른 문자열 추가
                packet = str(i) + data # pkt와 data를 합쳐 packet 생성
                print("S: R에게 보내는 데이터 -> ", data)
                
                senderSocket.sendto(str(packet).encode('utf8'),(receiverName, receiverPort)) # 패킷 전송
                
                print("S: send pkt", i)
                print("")
                send.append(i)
                count += 1
                
            seq_num = count
            
        print("--------------------------------------")
        
           

        
        sender_rcv(senderSocket)


def sender_rcv(senderSocket):
    global receiverName
    global receiverPort
    global next_seq_num
    global base
    global window_size
    global seq_num

    int_check = 0

    
    ack_r, receiverAddress  = senderSocket.recvfrom(1028) # 패킷 수신 대기
    ack_r = ack_r.decode() 
    ack = int(ack_r) # 형변환


    if ack == -1: # 비정상적인 ack, 즉 손실
        print("RECEIVER LOSS")
        print(" 다시 재전송 !")
            
    elif ack == base: # sender_window의 처음과 같을 경우 
        print("S: rcv ack ",base)
        base+=1 
        window_size += 1
        next_seq_num+=1

    if ack==98:
        print("종료")
        exit()



ack = 0
seq_num = 0
base = 0 # sender_window의 첫번째

count = 0
sender_window = 4 # 확인 응답이 되지 않은 패킷의 최대 허용수
window_size = 50
next_seq_num = sender_window + base - 1 # sender_window의 끝
seq_num = 0

data = "" # 데이터를 추가하기 위한 문자열
packet = "" # 데이터와 ack를 저장할 문자열
    
receiverName  = "127.0.0.1"
receiverPort = 12000
    
send = []
resend = []
resend_num = 0

print("--------------------------------------")

send_sender() # 함수 호출
senderSocket.close()
