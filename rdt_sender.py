
from socket import *
from threading import *
import random
import threading
import time
from threading import Thread
from time import sleep

data = "ABCDEFG" # S가 R에게 보낼 데이터
              
def _time_start(): # 타이머 시작하는 함수
    global check
    global t_0
    
    t = threading.currentThread() 
    t_0 = 0 # 초기화
    check = 0 # 초기화

    for i in range(10):# 총 0.01초 딜레이 시키기 위함 0.001*10
        if getattr(t, "run", True):
            time.sleep(0.001)
            check+=1
        else: # false가 되면
            break
  
    t_0 = 1

def _time_out():# time out이 발생하면
    print("TIME OUT! RESEND!")
    

    
def send_sender():
    global data
    global seq_num
    global ack

    global ack_receiver
    global pkt_sender
    global t_0
    global check
    
    receiverName = "127.0.0.1" # 서버의 ip 주소
    receiverPort = 12000
    
    
    senderSocket = socket(AF_INET, SOCK_DGRAM) # UDP 소켓 생성
    # senderSocket.bind(("", receiverPort))

    while True: # 무한 루프
        resend_check = 0

        if seq_num == 500:# 총 500번 반복되면 프로그램이 종료되게 
            print("--------------------------------------")
            print("종료")
            exit()
        
        PKT_error = random.randint(1,1000) # 1에서 1000까지 임의의 정수 하나
        
        if PKT_error == 10 :# 0.001의 확률
            print("S: send pkt", pkt_sender,"에 대한")
            print("SENDER LOSS 발생")
            _time_out()
            send_sender()

        packet = str(pkt_sender) + data # PKT와 DATA 합침
        senderSocket.sendto(packet.encode('utf8'),(receiverName, receiverPort))
        # receiver에게 packet 전송
       
        print("S: send pkt", pkt_sender) 
        
        seq_num+=1 # 전송되었음으로 seq_num+=1

        t = threading.Thread(target = _time_start) # Thread 생성
        t_0 = 0 # 초기화
        check = 0 # 초기화
        t.start() # 타이머 시작

        if (t_0 == 1 and check !=10) : # 타이머가 끝났으면
            _time_out() 
            seq_num-=1 
            send_sender() # 다시 재전송
            
        ack_r, receiverAddress = senderSocket.recvfrom(2048) #데이터에 대한 응답을 기다림

    

        # 시간내에 패킷 도착   
        print("--------------------------------------")
        t.run = False
        #ack_r = ack_r.decode('utf8')
        ack_receiver = ack_r[:1]
        data_r = ack_r[1:]
        ack = int(ack_receiver.decode('utf8')) # 정수로 변경
        data_r = data_r.decode('utf8')

        

        if ack == 2:
            print("RECEIVER에서 손실 발생!" )
            print("ACK ", pkt_sender, "손실")
            _time_out()
            print("다시 재전송!")
            ack = pkt_sender
            resend_check = 1
        
        if resend_check != 1 and seq_num != 0:
            print("S: R로부터 받은 데이터 -> ", data_r)
            print("S: rcv ack ", ack)
            # r_data = 
            
                    
        if resend_check != 1 and pkt_sender== ack: # 보낸 pkt에 대한 ack 도착
            if (pkt_sender == 1):
                 pkt_sender = 0
            elif (pkt_sender == 0):
                pkt_sender = 1

        
                

        
global t    
ack = 0 # receiver로 부터 받는 
pkt_sender = 0 
seq_num = 0

# TIMER 변수
t_0 = 0 # TIMER가 종료되었을 때 t_0 = 1
check = 0 # TIME OUT이 되었을 때 CHECK = 10

print("--------------------------------------")
print("S: S가 R에게 보내려는 데이터 -> ", data)

send_sender() # 함수 호출

senderSocket.close() # 소켓 닫기

