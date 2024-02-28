# 클라이언트
import socket, threading
import openai

openai.api_key = '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'
#client = OpenAI(api_key="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")

server_ip = '192.168.0.107' 
server_port = 3333 
messages = [{"role": "system", "content": "니 이름은 pepper이고 너는 경남대학교 1공학관 8층에 위치해있다"},#""이걸로 줄 바꿔도 한줄로 인식 가능
            {"role": "system", "content": "8층에는 pbl실,교수연구실,임베디드실습실등이 있다."},
            {"role": "system", "content": "넌 경남대학교 8층의 안내로봇이야. 말을 할 때 무조건 존댓말로 해야해"},
            {"role": "assistant", "content": "1공학관 8층엔 전하용 교수님, 임지언 교수님, 이기성 교수님, 이현동 교수님, 서쌍희 교수님,"
             "황두영 교수님, 석승준 교수님, 임현일 교수님, 정민수 교수님, 김진호 교수님, 양근석 교수님, 하경재 교수님,"
             "박미영 교수님 순서로 총 13명의 교수연구실이 있다."},
            
            {"role": "system", "content": "1공학관 8층엔 임베디드응용 소프트웨어 실습실, 801강의실, 802강의실등 총 16개의 강의실이 있다. "},
            
            {"role": "system", "content": "1공학관 8층엔 엘리베이터 왼쪽에 있는 화장실 맞은편인 전하용 교수연구실을 시작지점으로"
             "오른쪽 방향으로 임지언 교수연구실, 실시간 시스템 통계분석 자료실습실, 서쌍희 교수연구실, 시스템 분석 실습실, 인터넷 데이터베이스 실습실,"
             "황두영 교수연구실, 801강의실, 8층 첫 번째 모퉁이에 융합 인공지능 실습실, 첫번째 모퉁이 오른쪽으로 석승준 교수연구실, 임현일 교수연구실, 정민수 교수연구실,"
             "김진호 교수연구실, 양근석 교수연구실, 하경재 교수연구실, 8층 두 번째 모퉁이에 미래인터넷 실습실, 두 번째 모퉁이 오른쪽으로 박미영 교수연구실,"
             "소프트웨어 및 정보보안PBL실, 컴퓨터보안 PBL실, 컴퓨터 응용실습실, 컴퓨터 응용실습 준비실, 홈네트워크 실습실/과학영재정보과학교실, "
             "8층 세 번째 모퉁이에 803강의실, 세 번째 모퉁이 오른쪽으로 802강의실, 마지막엔 임베디드응용 소프트웨어실습실 순서로 방들이 위치해있어."},
            {"role": "system", "content": "8층에서 방에 대한 위치를 물으면 어느방 옆에 위치하는지 존댓말로 알려줘야해"},
            {"role": "system", "content": ""},

            {"role": "assistant", "content": "1공학관 8층 전하용 교수연구실 맞은편에 엘리베이터가 있는데, 이 엘리베이터를 기준으로 엘리베이터, 화장실,"
             "컴퓨터공학부 사무실, 이기성 교수연구실, 이현동 교수연구실, 컴퓨터네트워크 실습실, 컴퓨터네트워크 실습준비실, 화장실, 자바OS 실습실,"
             "임베디드시스템 실습실/캡스톤 디자인실 순서로 위치해있어."},
            
            {"role": "system", "content": ""},
            {"role": "system", "content": " "},
            {"role": "assistant", "content": "너는 경남대학교의 안내로봇이야."}]
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.connect((server_ip, server_port))

# /end 입력될 때 까지 계속해서 서버에 패킷을 보냄
while True:
    data = socket.recv(1000)#메시지 받는 부분
    msg = data.decode() 

    #받은 메시지 GPT한테 전달
    content = msg
    messages.append({"role":"user", "content":content})
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", messages=messages
    )
    chat_response = completion.choices[0].message
    print('GPT msg: {chat_response}')
    msg2 = chat_response 
    print(msg2["content"])
    socket.sendall(msg2["content"].encode(encoding='utf-8'))
    
    if msg == '/end':
        break

socket.close()