import struct 
import socket
import sys
import _thread
import time

group = '239.255.255.250'
mport = 1900

hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)
ip_port = 8080

# Trata requisicoes chamada socket na porta 8080
def on_new_client(cliSocket, addr):
    print(f'Conectou-se com {str(addr)}')
    while True:
        msg = cliSocket.recv(1024)
        if msg:
            print(f'\n{msg.decode()}')
            break
        else:   
            break

    # Envia uma resposta ao cliente
    header = 'HTTP/1.1 200 OK\n'
    header += 'Cache-Control: no-cache\n'
    time_now = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
    header += 'Date: {now}\n'.format(now=time_now)
    header += 'Server: Web Server Python\n'
    header += 'Connection: close\n\n'
    
    print(f'\n\nResposta do Servidor \n{header}')
    cliSocket.sendall(header.encode())
    cliSocket.close()
    

# definer o procedimento que irá tratar a chamada de pesquisa do 
# multicast
def multicastServer(group,mport):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.bind((group,mport))
    except:
        sock.bind(('', mport))
    print('Pronto para escutar na porta '+ str(mport)+'\n')
    mreq = struct.pack("4sl", socket.inet_aton(group), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
    while True:
        (data, address) = sock.recvfrom(12000)
        if data:
            message = data.decode()
            print(message)
            if message.__contains__('M-SEARCH'):
                sock.sendto(f'{ip};{5000}'.encode(), address)


# criar o servidor HTTP
sockHttp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    sockHttp.bind((ip,ip_port))
except socket.error:
    sockHttp.bind(('',ip_port))
sockHttp.listen(1)

_thread.start_new_thread(multicastServer,(group,mport))
while True:
    client, addr = sockHttp.accept()
    _thread.start_new_thread(on_new_client,(client,addr))

sockHttp.close()