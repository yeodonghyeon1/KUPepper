# 클라이언트
import socket, threading
import openai


openai.api_key = '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'
#client = OpenAI(api_key="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")

server_ip = 'localhost' 
server_port = 3333 
messages = [{"role": "system", "content": "니 이름은 pepper이고 너는 경남대학교 1공학관 8층에 위치해있어"},
            {"role": "system", "content": "8층에는 pbl실,교수연구실,임베디드실습실이 있다."},
            {"role": "system", "content": "넌 말할 때 존댓말로 해야해"},
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