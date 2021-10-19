
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
