# main.py
# from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog
from PyQt5 import QtWidgets, QtGui, QtCore
from coppeliasim_zmqremoteapi_client import RemoteAPIClient
from PyQt5.QtCore import QTimer, Qt
from PyQt5.uic import loadUi
import numpy as np
import cv2
# from PyQt5.QtGui import QImage, QPixmap
from icecream import ic
import sys

class MainApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainApp, self).__init__()
        loadUi("CS_mrnd_drone_oink.ui", self)
        self.actionCall_CS_sript.setCheckable(True)
        self.actionLive_camera.setCheckable(True)
        self.actionWaypoint_init.setCheckable(True)
        self.actionCall_CS_sript.triggered.connect(self.on_call_cs_script)
        self.actionStart_Simulation.triggered.connect(self.on_start_simulation)
        self.actionStop_Simulation.triggered.connect(self.on_stop_simulation)
        self.actionArialShot.triggered.connect(self.on_arialshot)
        self.actionSnapShot.triggered.connect(self.on_snapshot)
        self.actionRotate_camera.triggered.connect(self.on_rotate_cam)
        self.actionLive_camera.triggered.connect(self.on_live_cam)
        self.actionWaypoint_init.triggered.connect(self.on_Waypt_init)
        self.actionPetrol_drone.triggered.connect(self.on_petrol_drone)
        self.actionDrone_pause.triggered.connect(self.on_pause_drone)
        self.actionmove_Dummy.triggered.connect(self.on_move_goal)
        self.actionmove_Robot.triggered.connect(self.on_move_robot)
        self.actionpause_Robot.triggered.connect(self.on_pause_robot)
        self.actionset_Algo_num.triggered.connect(self.nav_setnum)
        # Init all the event-driven click to be disabled
        self.falsify_click()
        self.mapView = self.findChild(QtWidgets.QGraphicsView, "mapView")
        self.mapView.__class__ = ClickableGView
        self.mapView.parent().registerClick = self.registerClick

        self.timer = QTimer()
        self.timer.timeout.connect(self.perform_task)
        self.robArrtimer = QTimer()
        self.robArrtimer.timeout.connect(self.query_arr)
                
    def nav_setnum(self):
        strnum = self.nav_val.text()
        result = self.sim.callScriptFunction("updateSearchAlgorithm", self.childRobotHandle, strnum)
        self.nav_selected.setText(result)
        ic(result)

    def falsify_click(self):
        self.actionStart_Simulation.setEnabled(False)
        self.actionStop_Simulation.setEnabled(False)
        self.actionArialShot.setEnabled(False)
        self.actionLive_camera.setEnabled(False)
        self.actionSnapShot.setEnabled(False)
        self.actionRotate_camera.setEnabled(False)
        self.actionWaypoint_init.setEnabled(False)
        self.actionPetrol_drone.setEnabled(False)
        self.actionDrone_pause.setEnabled(False)
        self.actionmove_Dummy.setEnabled(False)
        self.actionmove_Robot.setEnabled(False)
        self.actionpause_Robot.setEnabled(False)

    def drone_command(self, command, data=None):
        input_data = {"command": command, "data":data}
        result2 = self.sim.callScriptFunction("handleCommand", self.floorHandle, input_data)
        ic(result2)
        return(result2)

    def on_call_cs_script(self):
        self.client = RemoteAPIClient()
        self.sim = self.client.require('sim')
        self.sim.loadScene(self.sim.getStringParam(self.sim.stringparam_scenedefaultdir) + '/mrnd/mstmrnd4.ttt')
        self.visionSensorHandle = self.sim.getObject('/Vision_csRobot')
        self.floorHandle = self.sim.getScript(self.sim.scripttype_childscript, "/Floor")
        self.myDummyHandle = self.sim.getObject('./goalDummy')
        self.childRobotHandle = self.sim.getScript(self.sim.scripttype_childscript, "/mobileRobot")
        self.mapSensorHandle = self.sim.getObject('/Vision_sensor')
        self.cam_angle_val.setText("90")
        self.x_val.setText("0.0")
        self.y_val.setText("0.0")
        self.z_val.setText("0.0")
        self.actionCall_CS_sript.setEnabled(False) 
        self.actionStart_Simulation.setEnabled(True) 
        status = "Script Loaded"
        ic(status)
        self.status.setText(status)

    def on_Waypt_init(self):
        self.waypoints = [
            [2.5, -2.5, 2],
            [-2.5, -2.5, 2],
            [-2.5, 2.5, 2],
            [2.5, 2.5, 2],
            [2.5, -2.5, 2]
        ]
        status = self.drone_command("SET_WAYPOINTS", self.waypoints) 
        self.actionWaypoint_init.setEnabled(False)
        self.actionPetrol_drone.setEnabled(True)        
        ic(status)
        self.status.setText(status)

    def on_petrol_drone(self):
        status = self.drone_command("START_WAYPOINTS")
        self.actionPetrol_drone.setEnabled(False)       
        self.actionDrone_pause.setEnabled(True)       
        ic(status)
        self.status.setText(status)

    def on_pause_drone(self):       
        status = self.drone_command("STOP_WAYPOINTS")
        self.actionDrone_pause.setEnabled(False)   
        self.actionPetrol_drone.setEnabled(True)        
        ic(status)
        self.status.setText(status)

    def on_start_simulation(self):
        self.sim.startSimulation()
        self.actionStart_Simulation.setEnabled(False) 
        self.actionStop_Simulation.setEnabled(True)      
        self.actionArialShot.setEnabled(True)
        self.actionLive_camera.setEnabled(True)
        self.actionSnapShot.setEnabled(True)
        self.actionRotate_camera.setEnabled(True)  
        self.actionWaypoint_init.setEnabled(True)
        self.actionmove_Dummy.setEnabled(True)
        status = "Simulation Started"
        ic(status)
        self.status.setText(status)

    def on_stop_simulation(self):
        if self.robArrtimer.isActive():
            self.robArrtimer.stop()
        self.sim.stopSimulation()
        self.falsify_click()
        self.actionStart_Simulation.setEnabled(True)
        status = "Simulation Stopped"
        ic(status)
        self.status.setText(status)

    def on_arialshot(self):
        img, [self.resX, self.resY] = self.sim.getVisionSensorImg(self.mapSensorHandle)
        img = np.frombuffer(img, dtype=np.uint8).reshape(self.resY, self.resX, 3)
        img = cv2.flip(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), 0)
        self.img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        height, width, channel = img.shape
        bytes_per_line = 3 * width
        q_img = QtGui.QImage(self.img_rgb.data, width, height, bytes_per_line, QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap.fromImage(q_img)
        scene = QtWidgets.QGraphicsScene()
        scene.addPixmap(pixmap)
        self.mapView.setScene(scene)
        status = "Map View"
        ic(status)
        self.status.setText(status)

    def registerClick(self, x, y):
        display_Width  = self.mapView.width()
        display_Height  = self.mapView.height()
        displayWidth  = 250
        displayHeight  = 250
        centerX = displayWidth // 2
        centerY = displayHeight // 2
        temp_X = ((x - centerX) / displayWidth) * 10.0
        temp_Y = ((centerY - y) / displayHeight) * 10.0
        coordX = temp_X - 0.16
        coordY = temp_Y + 0.16
        self.x_val.setText(f"{coordX:.2f}")
        self.y_val.setText(f"{coordY:.2f}")
        ic(displayWidth,displayHeight,self.x_val.text(),self.y_val.text())
        imgX = int(((temp_X/10)*display_Width + centerX)/display_Width * self.resX)
        imgY = int((-(temp_Y/10)*display_Height + centerY)/display_Height * self.resY)
        img = np.copy(self.img_rgb) # GET THE MAP COPY
        img = cv2.circle(img, (imgX, imgY), 3, (255, 0, 0), -1) # RED DOT
        height, width, channel = img.shape
        bytes_per_line = 3 * width
        q_img = QtGui.QImage(img.data, width, height, bytes_per_line, QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap.fromImage(q_img)
        scene = QtWidgets.QGraphicsScene()
        scene.addPixmap(pixmap)
        self.mapView.setScene(scene)
        status = "Goal Shifted"
        ic(status)
        self.status.setText(status)


    def on_snapshot(self):
        img, [resX, resY] = self.sim.getVisionSensorImg(self.visionSensorHandle)
        img = np.frombuffer(img, dtype=np.uint8).reshape(resY, resX, 3)
        img = cv2.flip(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), 0)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        height, width, channel = img.shape
        bytes_per_line = 3 * width
        q_img = QtGui.QImage(img_rgb.data, width, height, bytes_per_line, QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap.fromImage(q_img)
        scene = QtWidgets.QGraphicsScene()
        scene.addPixmap(pixmap)
        self.graphicsView.setScene(scene)
        status = "Snap_shot Robot Camera"
        ic(status)
        self.status.setText(status)

    def on_rotate_cam(self):
        camera_rotate_angle_text = self.cam_angle_val.text()
        camera_rotate_angle = float(camera_rotate_angle_text)
        camera_rotate_angle_formatted = format(camera_rotate_angle, ".1f")
        current_pose = self.sim.getObjectPose(self.visionSensorHandle, -1)
        # current_pose = position and an orientation (quaternion) has 7 float values
        rotation_axis = [0, 0, 1];  # y-axis
        axis_pos = current_pose[:3]  # Extracting the first three elements (position part)
        camera_rotate_angle
        new_pose = self.sim.rotateAroundAxis(current_pose, rotation_axis, axis_pos, (camera_rotate_angle/360)* 6.28)
        self.sim.setObjectPose(self.visionSensorHandle, -1, new_pose)
        status = f'Camera {camera_rotate_angle_text} rotated'
        ic(status)
        self.status.setText(status)

    def query_arr(self):
        rob_status = self.sim.callScriptFunction("pauseRunSetnavQuery", self.childRobotHandle, "QUERY")
        if (rob_status == "NAV"):
            self.actionmove_Robot.setEnabled(False)       
            self.actionpause_Robot.setEnabled(False)    
            self.robArrtimer.stop()
            status = "Destination Reached"
            self.status.setText(status)

    def perform_task(self):
        # Capture the image from the vision sensor
        img, [resX, resY] = self.sim.getVisionSensorImg(self.visionSensorHandle)
        img = np.frombuffer(img, dtype=np.uint8).reshape(resY, resX, 3)
        img = cv2.flip(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), 0)
        
        # Convert the image to HSV color space for easier color detection
        hsv_img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

        # Define the range for the brown color in HSV space
        lower_brown = np.array([10, 50, 50])  # Lower bound of brown
        upper_brown = np.array([30, 150, 150])  # Upper bound of brown

        # Create a mask for brown pixels
        brown_mask = cv2.inRange(hsv_img, lower_brown, upper_brown)
        cv2.imshow("Brown Mask", brown_mask)  # Show detected brown areas
        cv2.waitKey(1)  # Refresh the window

        # Find contours of detected brown regions
        contours, _ = cv2.findContours(brown_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours:  # Only update status if brown is detected
            cv2.drawContours(img, contours, -1, (0, 255, 0), 3)  # Draw contours in green
            status = "Intruder detected!"
        else:
            status = "No Intruder detected."

        # Update UI status text only if it has changed
        if self.status.text() != status:
            ic(status)  # Debugging print
            self.status.setText(status)

        # Convert the processed image back to RGB for display
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        height, width, channel = img.shape
        bytes_per_line = 3 * width
        q_img = QtGui.QImage(img_rgb.data, width, height, bytes_per_line, QtGui.QImage.Format_RGB888)
        pixmap = QtGui.QPixmap.fromImage(q_img)
        scene = QtWidgets.QGraphicsScene()
        scene.addPixmap(pixmap)
        self.graphicsView.setScene(scene)
 

    def on_live_cam(self):
        if self.actionLive_camera.isChecked():
            self.timer.start(1) 
            status = "Robot Camera goes Live"
            ic(status)
            self.status.setText(status)
        else:
            self.timer.stop() 
            status = "Robot Camera Off"
            ic(status)
            self.status.setText(status)

    def on_move_goal(self):
        endRefX_txt = self.x_val.text()
        endRefX = float(endRefX_txt)
        endRefX = format(endRefX, ".2f")    
        endRefY_txt = self.y_val.text()
        endRefY = float(endRefY_txt)
        endRefY = format(endRefY, ".2f")     
        new_position = [endRefX , endRefY, 0]
        self.sim.setObjectPosition(self.myDummyHandle, -1, new_position)
        status = "Goal Dummy is moved"
        self.actionmove_Robot.setEnabled(True)   
        ic(status)
        self.status.setText(status)

    def on_move_robot(self):
        result = self.sim.callScriptFunction("pauseRunSetnavQuery", self.childRobotHandle, "PAUSE")
        self.actionmove_Robot.setEnabled(False)       
        self.actionpause_Robot.setEnabled(True)    
        if not self.robArrtimer.isActive():
            self.robArrtimer.start(1000)
        ic(result)
        self.status.setText(result)

    def on_pause_robot(self):
        result = self.sim.callScriptFunction("pauseRunSetnavQuery", self.childRobotHandle, "PAUSE")
        self.actionpause_Robot.setEnabled(False)   
        self.actionmove_Robot.setEnabled(True)        
        ic(result)
        self.status.setText(result)

class ClickableGView(QtWidgets.QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAlignment(Qt.AlignCenter)
        self.setMouseTracking(True)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            x = event.pos().x()
            y = event.pos().y()
            self.parent().registerClick(x, y)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    main_app = MainApp()
    main_app.show()
    sys.exit(app.exec_())
