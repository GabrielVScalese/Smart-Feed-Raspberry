import socket
 
# Messagem M-SEARCH
MS = \
    'M-SEARCH * HTTP/1.1\r\n' \
    'HOST:239.255.255.250:1900\r\n' \
    'ST:upnp:rootdevice\r\n' \
    'MX:2\r\n' \
    'MAN:"ssdp:discover"\r\n' \
    '\r\n'
 
# Prepara o socket UDP para realizar o multicast
SOC = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
SOC.settimeout(2)
 
# Envia a mensagem para o endereço do multicast por UPNP
SOC.sendto('M-SEARCH'.encode('utf-8'), ('239.255.255.250', 1900) )
 
# Ouvi e captura respostas
try:
    while True:
        data, addr = SOC.recvfrom(8192)
        message = data.decode('utf-8')
        print (addr, message)
except socket.timeout:
        pass