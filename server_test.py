import socket
import threading

HOST = "localhost"
PORT = 9999
#Maximum file size in bits
MAX_SIZE = 5*1024*1024
FORMAT='utf-8'
DELIMITER=b'EOF'
received_filename = 'received_image.jpg'

def handle_client(c,addr):
    print(f"[NEW CONNECTION] {addr}\n")
    #Recieve file size sent by the client
    data_size = c.recv(4)
    data_size=int.from_bytes(data_size, byteorder='big')
    print(data_size)
    #If the file size exceeds the maximum ,send error message and shut down client  
    if data_size>MAX_SIZE:
        c.sendall(b'[ERROR] Size of the file is too big,please reconnect and retry')
        print(f"[SYSTEM] {addr} Try to transfer invalid files " )
        c.close()
        return
    else:
        c.sendall(b'[SERVER] Start transfering')
        data = b''
        while True:
            pack = c.recv(1024)
            if not pack:
                break
            data += pack
        #Separate  message and image by delimiter in data and decode the message
        if DELIMITER in data:
            parts = data.split(DELIMITER)
            msg = parts[0].decode()
            img = parts[1]  
        print(f"[SYSTEM] Message by {addr}: {msg}") 
        #Write the image to file
        with open(received_filename, 'wb') as f:
            f.write(img)
        print(f"[SYSTEM] Image by {addr} received and saved!!")   

def start_server (host,port):
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
        s.bind((host,port))
        s.listen(5)
        print(f"[LISTENING] Server is listening on  {PORT}...\n")
        s.settimeout(5)
        try:
            while True:
                try:
                    client_socket,addr=s.accept()
                    #Handle different client
                    thread=threading.Thread(target=handle_client,args=(client_socket,addr))
                    thread.daemon = True 
                    thread.start()
                    #Count of connected client number
                    print(f"[ACTIVE CONNECTION] {threading.active_count()-1}\n")
                except socket.timeout:
                    pass  
        except KeyboardInterrupt:
            print("\n[SYSTEM] Shutting down server...\n")


if __name__ == "__main__": 
    start_server(HOST, PORT)