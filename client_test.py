import socket

HOST = "localhost"
PORT = 9999
MESSEAGE="This is a picture of a cool cat."
FORMAT='utf-8'
FILENAME="tt.jpg"
DELIMITER='EOF'

def send_data(c):
    #Add a delimiter after the message and encode 
    msg=MESSEAGE+DELIMITER
    msg_bytes = msg.encode('utf-8')

    with open(FILENAME, 'rb') as img_file:
        img_data = img_file.read()
    #Combine message and image into a binary data and calculate file size
    data_bytes=msg_bytes+img_data
    data_size = len(data_bytes).to_bytes(4,byteorder='big')
    #Pass the total file size to server
    c.sendall(data_size)
    #Wait for the server to confirm file size
    response=c.recv(1024)
    print(f"{response.decode(FORMAT)}")
    try :
        #Send whole data
        c.sendall(data_bytes)
    except :
        #If the file is invalid ,client will be closed by the server and an exception will occur.
        print("[SYSTEM] File sent unsuccessfully!!")
        return        
  
if __name__ == "__main__": 
    client_socket= socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        client_socket.connect((HOST, PORT))
        #Press 's' to send file
        while True:
            user_input = input("Press 's' to send data: ")
            if user_input.lower() == 's':
                send_data(client_socket)
                break
    except ConnectionRefusedError:
        print("[ERROR]Connection refused. Server may be offline.")
   
   
        
