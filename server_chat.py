#server_chat.py allows multiple client to connect

import select, socket, sys, pdb
from util_chat import ChatHall, Room, ChatMember
import util_chat

READ_BUFFER = 4096

while True:
    
    read_players, write_players, error_sockets = select.select(connection_list, [], [])
   
    
	    
    for member in read_players:
        if member is listensocket: # new connection, member is a socket
            new_socket, add = member.accept()
            new_member = ChatMember(new_socket)
            connection_list.append(new_member)
            chat_hall_list.welcome_new(new_member)
	
         
    
    for sock in error_sockets: # close error sockets
        sock.close()
        connection_list.remove(sock)
