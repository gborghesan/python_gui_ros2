#!/usr/bin/python3
from curses import has_key
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

from PyQt5 import QtGui, QtCore, QtWidgets
from lxml import etree
import sys
from rclpy.exceptions import ParameterNotDeclaredException
from rcl_interfaces.msg import ParameterType
from ament_index_python.packages import get_package_share_directory
import json
class EventSender(QtWidgets.QWidget,Node):
    
    def __init__(self):
        #QtWidgets.QWidget.__init__(self,node_name='prova')
        super(EventSender, self).__init__(node_name='event_sender')
        self.initUI()
      
        
    def initUI(self):      


        #ros related stuff
        self.declare_parameter('topic_name', '/events')
        self.declare_parameter('use_json', False)
        self.declare_parameter('xml_button_file', get_package_share_directory('python_gui')+'/json/default.json')
        self.declare_parameter('json_button_file', get_package_share_directory('python_gui')+'/xml/default.xml')
        
        topic_name=self.get_parameter('topic_name').get_parameter_value().string_value
        
        #topic_name="/events"
        self.pub=self.create_publisher(String,topic_name,10)
        self.string_map={}
        self.buttons={}
        self.create_buttons()



        
    def create_buttons(self):
        QtWidgets.QToolTip.setFont(QtGui.QFont('SansSerif', 10))
        use_json=self.get_parameter('use_json').get_parameter_value().bool_value
        grid = QtWidgets.QGridLayout()
        if not use_json:
            file_name=self.get_parameter('xml_button_file').get_parameter_value().string_value
            if file_name=="":
            #file_name =(get_pkg_dir("python_gui"))+"/xml/default.xml"
                self.get_logger().error("file {} not found".format(file_name))
    
            self.get_logger().info("file {} loaded".format(file_name))
            
                
            #print "file name:\n"+file_name
            file_map = etree.parse(file_name)
            
            list_event =  file_map.getroot()
            
            i=0
            for child  in list_event:
                self.string_map[child.get('name')]=child.get('event')
                btn=QtWidgets.QPushButton(child.get('name'), self)
                grid.addWidget(btn,i,0)
                btn.clicked.connect(self.buttonClicked) 
                tooltip_text=child.get('tooltip')
                if tooltip_text!=None:
                    btn.setToolTip(tooltip_text)
                
                i=i+1
        else:
            file_name=self.get_parameter('json_button_file').get_parameter_value().string_value
            print ("file name:\n"+file_name)
            with open(file_name) as json_file:
                data = json.load(json_file)
                self.buttons=data['buttons']
                print("here")
                i=0
                for button  in data['buttons']:
                    print("button {}".format(button['name']) )
                    self.string_map[button['name']]=button['event']
                    btn=QtWidgets.QPushButton(button['name'], self)
                    grid.addWidget(btn,i,0)
                    i=i+1
                    btn.clicked.connect(self.buttonClickedJson) 
                    tooltip_text=button.get('tooltip')
                    if tooltip_text!=None:
                        btn.setToolTip(tooltip_text)

            
 
        #layout: a vbox divided in 3 parts
        # the grid, a Stretch to fill in the space and a status bar
        
        vbox = QtWidgets.QVBoxLayout()
        vbox.addLayout(grid)
        self.statBar = QtWidgets.QStatusBar(self)
        vbox.addStretch(1)
        vbox.addWidget(self.statBar)
        self.statBar.showMessage("Event sender by GB")
        
        self.setLayout(vbox)
        self.setGeometry(300, 300, 290, 150)
        self.move(1500, 150)
        self.setWindowTitle('Event sender')
        self.setWindowIcon(QtGui.QIcon((get_package_share_directory("python_gui")) + '/icons/es_ico.png'))
        self.show()
        
            
    def buttonClicked(self):
      
        sender = self.sender()
        string_key=(sender.text()) 
        event_to_send=self.string_map[string_key]
        self.statBar.showMessage(string_key + ' pressed.\n->sent: '+
                                    event_to_send)
        s=String()
        s.data=event_to_send
        self.pub.publish(s)

    def buttonClickedJson(self):
      
        sender = self.sender()
        string_key=(sender.text()) 
        event_to_send=self.string_map[string_key]
        self.statBar.showMessage(string_key + ' pressed.\n->sent: '+
                                    event_to_send)
        s=String()
        s.data=event_to_send
        self.pub.publish(s)

def sigint_handler(*args):
    """Handler for the SIGINT signal."""
    sys.stderr.write('\r')
    QtWidgets.QApplication.quit()
import signal 

def main(args=None):
    rclpy.init(args=args)
    
    signal.signal(signal.SIGINT, sigint_handler)
    app = QtWidgets.QApplication(sys.argv)
    timer = QtCore.QTimer()
    timer.start(500)  # You may change this if you wish.
    timer.timeout.connect(lambda: None)  # Let the interpreter run each 500 ms.
    ex = EventSender()
     
    status = app.exec_()
    sys.exit(status)
   

if __name__ == '__main__':
    main()