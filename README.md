# IRC-Chat-Server-Client

The following project zipped, has the user configured as –u Cesia, therefore when you first run the server and run the client, the chat box will automatically say “Hello Cesia…” You may add another client to the server, as the server should support more than one client. Each client has a different –u name which can be changed , in order to see how the different clients interact with one another. The DB class was largely implemented using hashmaps.

The following commands work if done in this order : 

/pass <password> 
  
/user <username> <# to represent either mode i or w or none> <unused> <real_name>
  
/rules

/version

/nick <nickname>
  
/info

/setname <name>
  
/users 

/quit

/join <channel>              (only one channel at a time)
  
/mode <nickname> <+ or -> <w,i,r,o,O>
  
/wallops <message>             ( must have had mode set to w, else: this wont work)
  
/topic <channel_name> <topic> 
  
if topic is set then you can check the topic with /topic <channel_name> 

/time

/userips <nickname>
  
/help

/die

/away <message>
  
/ison <nickname>
  
/ping <name>	 (after ison)
  
/pong <name>		(after ison)
  
/userhost <nickname nickname2> (supports up to 5 nicknames)

/who <name>  or /who <name> <o> to check if the user is an operator
  
/part <channels,channels,channels> <message>
  
/whois <nickname>
  
/list <channels,channels>

/knock <channel_name> <message>
  
/notice <channel_name> <message>	    (has a small bug that sometimes people receive it, sometimes they don’t)
  
/privmsg < name> <message>
  
/kill <nickname> <comment>
  
/oper <username> <password>
  
/silence <+ or - > <nickname>	
  
/kick <name> <comment>
  
/invite <nickname> <channel_name>

