
from socket import *
import random

data = "HIJKLMN"


def wait_send(receiverSocket):
    
    global count # 총 몇번 돌아가는 지 확인하기 위한 변수
    global ack 
    global senderAddress
    
    while True: # 무한루프

        
            
        ACK_error = random.randint(1,1000) # 1부터 1000까지 중 랜덤으로 하나
        if count!=0 and ACK_error == 10: # 1000분의 확률
            print("RECEIVER LOSS")
            print("--------------------------------------")
            ack = 2 # 비정상적인 ack
            packet = str(ack) + data # ack와 data를 합침
            receiverSocket.sendto(packet.encode('utf8'), senderAddress) # packet 보냄
            count-=1
            
            if pkt_s == 0:
                ack = 1
            elif pkt_s == 1:
                ack = 0
            wait_send(receiverSocket)
            
        count+=1
        pkt_s, senderAddress = receiverSocket.recvfrom(2048) # sender의 요청 대기

        pkt = pkt_s[0:1] # 정수
        data_s = pkt_s[1:] # data
        pkt_sender = pkt.decode('utf8')
        data_s = data_s.decode('utf8')
        pkt_s = int(pkt_sender)


        if pkt_s == 0:
            if ack == 0:
                packet = str(ack) + data
                receiverSocket.sendto(packet.encode('utf8'), senderAddress)
                print("R: S로부터 받은 데이터 -> ", data_s)
                print("R: ack ", ack, "보냄")
                print("--------------------------------------")
                ack = 1
            else:
                if pkt_s == 0:
                    ack = 0
                elif pkt_s == 1:
                    ack = 1
                packet = str(ack) + data
                receiverSocket.sendto(packet.encode('utf8'), senderAddress)
                print("R: S로부터 받은 데이터 -> ", data_s)
                print("R: ack ", ack, "보냄")
                print("--------------------------------------")
                    

        elif pkt_s == 1:
            if ack == 1:
                packet = str(ack) + data
                receiverSocket.sendto(packet.encode('utf8'), senderAddress)
                print("R: S로부터 받은 데이터 -> ", data_s)
                print("R: ack ", ack, "보냄")
                print("--------------------------------------")
                ack = 0
            else:
                if pkt_s == 0:
                    ack = 0
                elif pkt_s == 1:
                    ack = 1
                packet = str(ack) + data
                receiverSocket.sendto(packet.encode('utf8'), senderAddress)
                print("R: S로부터 받은 데이터 -> ", data_s)
                print("R: ack ", ack, "보냄")
                print("--------------------------------------")
                
        if count == 500:
            print("종료")
            exit()
            
            
        

if __name__ == '__main__':

    count = 0 # 총 반복문을 몇 번 돌릴지를 count하는 변수
    ack = 0 # 0으로 초기화 
    receiverPort = 12000

    # 설정
    print("--------------------------------------")
    print("***RECEIVER START!***")
    receiverSocket = socket(AF_INET, SOCK_DGRAM) # 소켓 생성
    receiverSocket.bind(('', receiverPort))

    
    print('THE SERVER IS READY')
    print("R: R가 S에게 보내려는 데이터 -> ", data) 
    
    wait_send(receiverSocket) # 함수 호출

    
    



                                    

