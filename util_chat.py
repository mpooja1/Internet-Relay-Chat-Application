# handles all functionalities such as join , leave , switch room , sending personal message.

import socket, pdb

MAX_CLIENTS = 30
PORT = 22222
QUIT_STRING = '<$quit$>'


def create_socket(address):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setblocking(0)
     
    return s

class ChatHall:
    def __init__(self):
        self.rooms = {} # {room_name: Room}
        

    def welcome_new(self, new_member):
        new_member.socket.sendall(b'Welcome to pychat.\nPlease tell us your name:\n')
	

    def list_rooms(self, member):
        
        if len(self.rooms) == 0:
            msg = 'Oops, no active rooms currently. Create your own!\n' \
                + 'Use [<join> room_name] to create a room.\n'
            member.socket.sendall(msg.encode())
        else:
            msg = 'Listing current rooms and members...\n'
            for room in self.rooms:
		if 'personal' not in room:
			print (self.rooms[room].members)
		
		        msg += room + ": " + str(len(self.rooms[room].members)) + " member(s)\n"
			 
    
    def msg_handler(self, member, msg):
        
        instructions = b'Instructions:\n'\
            + b'[<list>] to list all rooms\n'\
            + b'[<join> room_name] to join/create/switch to a room\n' \
	    + b'[<personal> member_name] to chat personally\n'\
            + b'[<manual>] to show instructions\n' \
	    + b'[<switch>] to switch room\n' \
	    + b'[<leave>] to leave room\n'\
            + b'[<quit>] to quit\n' \
            + b'Otherwise start typing and enjoy!' \
            + b'\n'

        print(member.name + " says: " + msg)
        if "name:" in msg:
            name = msg.split()[1]
            member.name = name
            

        elif "<join>" in msg:
            same_room = False
            if len(msg.split()) >= 2: # error check
                if member.name+"-"+room_name in self.room_member_map: # switching?
                    if self.room_member_map[member.name+"-"+room_name] == room_name:
                        member.socket.sendall(b'You are already in room: ' + room_name.encode())
                    else: # switch
                        old_room = self.room_member_map[member.name+"-"+room_name]
                       # self.rooms[old_room].remove_member(member)
                if not same_room:
                    if not room_name in self.rooms: # new room:
                        new_room = Room(room_name)
                        self.rooms[room_name] = new_room
                    else:
                member.socket.sendall(instructions)

        elif "<list>" in msg:
	    print self.rooms
	    print self.room_member_map
            self.list_rooms(member) 

        elif "<manual>" in msg:
            member.socket.sendall(instructions)
	
	elif "<leave>" in msg:
	    
	    if len(msg.split()) >= 2: # error check
		    leaveroomname=msg.split()[1]
		   
		    if member.name+"-"+leaveroomname in self.room_member_map:
			del self.room_member_map[member.name+"-"+member.currentroomname]
			self.rooms[leaveroomname].remove_member(member)
	       		 
		    else :
			msg = "you entered wrong room name please try again\n"
			member.socket.sendall(msg.encode())
	    else:
                member.socket.sendall(instructions)

        
        elif "<quit>" in msg:
            member.socket.sendall(QUIT_STRING.encode())
            self.remove_member(member)

	elif "<switch>" in msg:
	    if len(msg.split()) >= 2:
		    switchroomname=msg.split()[1]
		 #   isroom = self.room_member_map[member.name+"-"+switchroomname]
		 #   if isroom == switchroomname :
	 	    
		    else:
			msg = "you are not in entered room please join"
			member.socket.sendall(msg.encode())
	    else:
		member.socket.sendall(instructions)
		

	elif "<personal>" in msg:
	    if len(msg.split()) >= 2:
		    membername = msg.split()[1]
		    if membername in self.members_map:
			    newmember = self.members_map[membername]
			    newmember.currentroomname = "personal-"+member.name+"-"+membername
		    else:
			msg = "Entered member does not exsist!!"
			member.socket.sendall(msg.encode())
	    else:
		    member.socket.sendall(instructions)
		
	elif not msg:
	    self.remove_member(member)

        else:
            # check if in a room or not first
            if member.name+"-"+member.currentroomname in self.room_member_map:
                self.rooms[self.room_member_map[member.name+"-"+member.currentroomname]].broadcast(member, msg.encode())
            else:
                msg = 'You are currently not in any room! \n' \
                    + 'Use [<list>] to see available rooms! \n' 
                     
                member.socket.sendall(msg.encode())
    
    def remove_member(self, member):
        if member.name +"-"+member.currentroomname in self.room_member_map:
            self.rooms[self.room_member_map[member.name+"-"+member.currentroomname]].remove_member(member)
             
    
class Room:
    def __init__(self, name):
        self.members = [] # a list of sockets
        self.name = name

    def welcome_new(self, from_member):
        msg = self.name + " welcomes: " + from_member.name + '\n'
        for member in self.members:
            member.socket.sendall(msg.encode())
    
    def broadcast(self, from_member, msg):
        msg = from_member.name.encode() + b":" + msg
        for member in self.members:
            member.socket.sendall(msg)

    def remove_member(self, member):
        self.members.remove(member)
        leave_msg = member.name.encode() + b"has left the room\n"
        self.broadcast(member, leave_msg)

class ChatMember:
    def __init__(self, socket, name = "new" , currentroomname="new"):
        socket.setblocking(0)
        self.socket = socket
        self.name = name
	self.currentroomname=currentroomname

    
    def fileno(self):
        return self.socket.fileno()

    
