AnalogRemote analog;
AnalogOutputRemote ao;
ButtonRemote button;

public class DeviceRead implements vrpn.AnalogRemote.AnalogChangeListener, vrpn.ButtonRemote.ButtonChangeListener {

  float sptx, spty, sptz, sprx, spry, sprz;
  String deviceName = "spaceNav@127.0.0.1:3891";
  boolean button1;
  boolean button2;

  public void vrpnSetup() {
    analog = null;
    ao = null;
    try {
      analog = new vrpn.AnalogRemote(deviceName, null, null, null, null );
      ao = new vrpn.AnalogOutputRemote(deviceName, null, null, null, null );
      button = new ButtonRemote(deviceName, null, null, null, null );
    }
    catch(InstantiationException e) {
      System.out.println("We couldn't connect to analog " + deviceName + ".");
      System.out.println(e.getMessage());
      return;
    }
    analog.addAnalogChangeListener(read);
    button.addButtonChangeListener(read);
    ao.requestValueChange(2, 5);
  }

  public void analogUpdate( vrpn.AnalogRemote.AnalogUpdate u, vrpn.AnalogRemote tracker) {
    sptx = (float)u.channel[0];
    spty = (float)u.channel[1];
    sptz = (float)u.channel[2];
    sprx = (float)u.channel[3];
    spry = (float)u.channel[4];
    sprz = (float)u.channel[5];
  }

  public void buttonUpdate( ButtonRemote.ButtonUpdate u, ButtonRemote button) {
    if (u.button == 0) {
      if (u.state == 1) {
        button1 = true;
      } else if (u.state == 0) {
        button1 = false;
      }
    }
    if (u.button == 1) {
      if (u.state == 1) {
        button2 = true;
      } else if (u.state == 0) {
        button2 = false;
      }
    }
  }
}