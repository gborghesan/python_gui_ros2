gui_sender.py
-------------------------
A simple interface that reads from an _xml_ or _json_ file with the format
Xml example:

```xml
<list>
    <button name='Start' event='e_start' tooltip='start the robot'/>
    <button name='Stop' event='e_stop'/>
</list>
```
Json example:

```json
{
"buttons" :[
	{"name":"Start", "event":"e_start","tooltip":"start the robot" },
	{"name":"Stop", "event":"e_stop"}
	]
}
```


Each button group produces a button that, if pressed sends the named event.
The default topic is /events, but can be altered using the ros parameter 'topic_name', see gui_sender.launch for an example on how to change this.
The tooltip is an optional field (text when hovering over a button).
The xml file is stored in the rosparam "xml_button_file", that defauts to default.xml in the xml directory of this package.

Use example:
-----
```
ros2 launch python_gui gui.launch.py 
```
or
```
ros2 launch python_gui gui_json.launch.py 
```

parameters
----------
See launch files for an examples with the default values.

 * use\_json: (bool) if set to true, the node uses the json specification, otherwise use the xml (default: False)
 * topic\_name: (string) name of the topic to publish the events on (default: "\events")
 * xml\_button\_file: (string) absolute location of the xml file with the event buttons to create.
 * json\_button\_file: (string) absolute location of the xjsonml file with the event buttons to create.


orocos integration 
-----
The file 'lua_components/signal_echo.lua'  is a an orocos component realized in lua, that reads a std_msgs/String from a topic and echos as a normal string.
to connect easily with components running rFSM.  

for loading the component check the code in the `test_deploy/deploy_echo.lua`, that  can be run with:


```
rttlua -i `ros2 pkg prefix python_gui`/share/python_gui/test_deploy/deploy_echo.lua
```

the code in he file is 

```
require "rttlib"
require "rttros"

tc=rtt.getTC()
if tc:getName() == "lua" then
  depl=tc:getPeer("Deployer")
elseif tc:getName() == "Deployer" then
  depl=tc
end
depl:import("rtt_ros2")
ros=rtt.provides("ros")
ros:import("rtt_ros2_std_msgs")
ros_application_name = "echo_test"

rtt.provides("ros"):create_named_node_with_namespace("Main_node",ros_application_name)


depl:loadComponent("eventEcho", "OCL::LuaComponent")
--... and get references to them
eventEcho = depl:getPeer("eventEcho")
 -- load the Lua hooks
eventEcho:exec_file(rtt.provides("ros"):find("python_gui").."/lua_components/signal_echo.lua")
--configure and starts
eventEcho:configure()
eventEcho:start()

-- in the end create a stream
depl:stream("eventEcho.event_in", ros:topic("/events",false))
```
