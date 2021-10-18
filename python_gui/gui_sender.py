#!/usr/bin/python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

from PyQt5 import QtGui, QtCore, QtWidgets
from lxml import etree
import sys
from rclpy.exceptions import ParameterNotDeclaredException
from rcl_interfaces.msg import ParameterType

class EventSender(QtWidgets.QWidget,Node):
    
    def __init__(self):
        #QtWidgets.QWidget.__init__(self,node_name='prova')
        super(EventSender, self).__init__(node_name='prova')
        self.initUI()
      
        
    def initUI(self):      


        #ros related stuff
        self.declare_parameter('topic_name', '/events')
        self.declare_parameter('xml_button_file','/home/gborghesan/Desktop/yumi_etasl_apps/cartesian_trj_1/cpf/buttons.xml')#todo - set default value
        
        topic_name=self.get_parameter('topic_name').get_parameter_value().string_value
        
        #topic_name="/events"
        self.pub=self.create_publisher(String,topic_name,10)
        self.string_map={}
        self.buttons={}
        self.create_buttons()



        
    def create_buttons(self):
        QtWidgets.QToolTip.setFont(QtGui.QFont('SansSerif', 10))
        file_name=self.get_parameter('xml_button_file').get_parameter_value().string_value
        if file_name=="":
           #file_name =(get_pkg_dir("python_gui"))+"/xml/default.xml"
           print("file not found - ERROR")
           
           
        print("file {} loaded".format(file_name))
        
            
        #print "file name:\n"+file_name
        file_map = etree.parse(file_name)
        
        list_event =  file_map.getroot()
        grid = QtWidgets.QGridLayout()
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
        #self.setWindowIcon(QtGui.QIcon((get_pkg_dir("python_gui")) + '/resources/es_ico.png'))
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