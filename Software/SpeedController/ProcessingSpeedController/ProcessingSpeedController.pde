
import processing.serial.*;
import g4p_controls.*;


Serial myPort;  // Create object from Serial class
GCustomSlider sdr1;

final int MIN = 800;
final int MAX = 3300;
       

void setup() 
{
  size(600, 200);
  println(Serial.list());
  String portName = Serial.list()[3];
  myPort = new Serial(this, portName, 115200);

  reset();

  // slider
  sdr1 = new GCustomSlider(this, 100, 50, 400, 50, null);
  // show          opaque  ticks value limits
  sdr1.setShowDecor(false, true, true, true);
  sdr1.setNbrTicks(1);
  sdr1.setLimits(800, 800, 3300);
}

void draw() {
  background(255);  
}

void mouseDragged()
{
  writeDAC((int)map(mouseX, 0,width,MIN,MAX));
}

void serialEvent(Serial p) { 
  String inString = p.readString(); 
  // println(inString);
} 

void writeDAC(int val)
{
  String json= "{\"cmd\":\"dac\",\"data\":\""+val+"\"}\r\n";
  myPort.write(json);
  print(json);
}

void reset()
{
  writeDAC (MIN);
}

public void handleSliderEvents(GValueControl slider, GEvent event) { 
 // println("integer value:" + slider.getValueI() + " float value:" + slider.getValueF());
 writeDAC((int)slider.getValueF());
}

