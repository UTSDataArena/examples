import os

from cyclops import *

from daAudio import *
from daInput import *

if __name__ == '__main__':
    """
    This example demonstrates how to introduce audio into an omegalib visualisation.   It shows 
    how to use various features which are provided by the daAudio and daInput omegalib modules, 
    including:

        - How to create an input cursor and use it to control the position of a sound source
        - How to load and play an audio effect in a continuous loop
    """

    path = os.path.dirname(__file__)
    if not path:
        path = os.getcwd()

    resources = os.path.join(path, 'resources')

    ui_context = UiContext()
    ui_context.add_cursor(SpaceNavControllerCursor('spacenav', 0, TriAxisCursorGeometryBuilder().set_position(0, 2, -4).build(), ui_context))

    getDefaultCamera().setControllerEnabled(False)

    light = Light.create()
    light.setEnabled(True)
    light.setPosition(Vector3(0, 0, 0))
    light.setColor(Color(1.0, 1.0, 1.0, 1.0))
    light.setAmbient(Color(0.1, 0.1, 0.1, 1.0))

    player = AudioPlayer()

    mosquito = AudioEmitter('mosquito')
    mosquito.set_position([0, 2, -4])
    mosquito.set_looping(True)
    mosquito.queue(load_wav_file(os.path.join(resources, 'mosquito.wav')))

    player.play(mosquito)
    player.update()

    def on_event():
        event = getEvent()

        ui_context.on_event(event)
        cursor = ui_context.get_cursor(event)

        if ControllerCursor.is_interested(event) and isinstance(cursor, ControllerCursor):
            position = cursor.get_position()

            mosquito.set_position([position.x, position.y, position.z])
            player.update() 

    setEventFunction(on_event)
