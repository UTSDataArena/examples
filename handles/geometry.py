import math
import os

from cyclops import *
from daInput import *
from daHandles import *
from daHEngine import *

if __name__ == '__main__':
    """
    This simple example demonstrates how to load control geometry from a Houdini
    digital asset.   It shows how to use various features which are provided by
    the daHandles and daHEngine omegalib modules, including:

        - How to create and initialise a connection to the Houdini Engine
        - How to use the Houdini control geometry builder to load handle geometry
          from an OTL
    """

    path = os.path.dirname(__file__)
    if not path:
        path = os.getcwd()

    resources = os.path.join(path, 'resources')

    ui_context = UiContext()

    getDefaultCamera().setControllerEnabled(False)

    houdini = HoudiniEngine.createAndInitialize()
    houdini.setLoggingEnabled(False)

    geometry_builder = HoudiniControlGeometryBuilder()
    geometry_builder.set_engine(houdini)
    geometry_builder.set_otl_path(os.path.join(resources, 'otl', 'whisker_handle.otl'))
    geometry_builder.set_asset_name('Object/whisker_handle')
    geometry_builder.set_geometry_name('whisker_handle1')

    control_builder = WhiskerControlBuilder()
    control_builder.set_geometry_builder(geometry_builder)

    transform_builder = TransformControlGroupBuilder()
    transform_builder.set_ui_context(ui_context)
    transform_builder.set_control_builder(control_builder)

    geo = BoxShape.create(1, 1, 1)
    geo.setEffect('colored -d white')
    bbox = (geo.getBoundMinimum(), geo.getBoundMaximum())

    box = ControllableSceneNode('box', geo)
    box.add_control(transform_builder.set_parent(box).set_bounding_box(bbox).build())
    box.node.setPosition(Vector3(0, 1.5, -10))
    box.node.rotate(Vector3(0, 1, 0), math.radians(-45), Space.Local)

    light = Light.create()
    light.setEnabled(True)
    light.setPosition(Vector3(0, 5, -2))
    light.setColor(Color(1.0, 1.0, 1.0, 1.0))
    light.setAmbient(Color(0.1, 0.1, 0.1, 1.0))

    manager = SelectionManager(ui_context)
    manager.add(box)

    def on_event():
        manager.on_event()

    setEventFunction(on_event)
