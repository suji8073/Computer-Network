## receiver_gbn

import random
import socket
from struct import *
from socket import *
from threading import *
import threading

exp_num = 0
receiverName  = "127.0.0.1"
receiverPort = 12000
window_size = 50
sender_window = 4
pkt = 0
seq_num = 0
received = []
received_Buffer = []

def send_Error(sendError, pkt, receiverSocket):
    global senderAddress
    global error_check
    if sendError == 10: # 1000분의 1의 확률
        print("RECEIVER LOSS")
        print("ACK", pkt , " 손실")
        print("--------------------------------------")
    
        error_check = -1 
        receiverSocket.sendto(str(error_check).encode('utf8'), senderAddress) # 비정상적 오류 전송
    
def receiver(receiverSocket):
    global exp_num

    global window_size
    global sender_window
    global pkt
    global seq_num
    global sendError

    global received 
    global received_Buffer 
    int_check = 0 # pkt와 data를 구분하기 위한 변수
    
    
    while True: # 무한루프
        if exp_num==99:
            print("종료")
            exit() # 프로그램 종료
            
        pkt_s, senderAddress = receiverSocket.recvfrom(2048) # sender로 부터 packet이 도착할 때까지 대기

        pkt_s = pkt_s.decode()

        for i in range(1, len(pkt_s)): # pkt와 data를 구분하기 위함
            if (pkt_s[:i].isdigit()):
                int_check = i
            else:
                break

        pkt = int(pkt_s[:int_check])# pkt
        data = pkt_s[int_check:] # 문자열

        error_check = 0
        sendError = random.randint(1, 1000)
       

            
        if pkt == exp_num : # receiver에서 기대한 pkt가 왔을 경우
            receiverSocket.sendto(str(exp_num).encode('utf8'), senderAddress) # ack 전송
            print("R: S로부터 전달된 데이터 -> ", data) # data 출력
            print("R: receive pkt ", pkt)
            print("R: send ack ", exp_num, "보냄") 
            
            send_Error(sendError, pkt, receiverSocket) # 손실 오류 검사
            if error_check == -1 :
                  receiver(receiverSocket) # 손실
                  
      
            print("--------------------------------------")
            
            received.append(exp_num)
            exp_num+=1 
            
        else:
            r_length = len(received)
            receiverSocket.sendto(str(received[r_length-1]).encode('utf8'), senderAddress)
            print("R: receive pkt ", pkt)
            
            print("R: send ack ", received[r_length-1], "보냄")

        receiver(receiverSocket)

        
        

def main():
    global receiverPort
    
    print("***RECEIVER_GBN START!***")
    receiverName  = "127.0.0.1" # 포트 번호
    
    receiverSocket = socket(AF_INET, SOCK_DGRAM) # 소켓 생성
    receiverSocket.bind(('', receiverPort)) # 
    # 설정 끝!

    print('THE RECEIVER IS READY!! _ GBN')
    print("--------------------------------------")

   

    receiver(receiverSocket)

    

            

    
         
if __name__ == '__main__':
    main()
