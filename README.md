# simpleirc
An IRC server and client for CS494P

To connect to the "cloud" server, simply use

`python3 start_client.py`

To connect to another server, use two arguments to specify the IP address and port

`python3 start_client.py localhost 2020`

To view the commands available after joining, use `\help` or `\h`

```
Commands available:
\quit	:	quit - disconnect from the server
\q	:	
\list	:	list - lists objects in server
\ls	:		\ls users
			\list rooms
			\list specific room
\help	:	help - displays the helpful list you are currently reading
\h	:	
\name	:	username - check username, or change it to something else
\n	:		\n new name
\join	:	join - join a selected room
\j	:		\join example_room
\leave	:	leave - leave a selected room
\l	:		\leave room_name
\create	:	create - creates a new chat room other users can join.
\cr	:		\create room_name, (optional) room_message
\1-9	:	specific server message - send a message to only one server at a time
			\1 this message is for the first server only
\dm	:	direct message - send a message to another user.
			\dm user, message
```