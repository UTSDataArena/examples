import os

from cyclops import *
from omegaToolkit import *

from daHEngine import *
from daHandles import *


if __name__ == '__main__':
    """
    This example demonstrates how to set up a scene containing houdini engine
    objects with parameters which may be manipulated using on-screen handles.
    It shows how to use various features which are provided by the daHandles and
    daHEngine omegalib modules, including:

        - How to use the Houdini Engine to load an OTL into an omegalib scene
        - How to use the Houdini Engine to access parameters exported by an OTL
        - How to attach controls to the parameters and manipulate their values
    """

    path = os.path.dirname(__file__)
    if not path:
        path = os.getcwd()

    resources = os.path.join(path, 'resources')

    ui_context = UiContext()

    getDefaultCamera().setControllerEnabled(False)

    houdini = HoudiniEngine.createAndInitialize()
    houdini.setLoggingEnabled(False)

    houdini.loadAssetLibraryFromFile(os.path.join(resources, 'otl', 'axisA1.otl'))
    houdini.instantiateAsset('Object/axisA1')
    houdini.instantiateGeometry('axisA11')

    parameters = HoudiniParameter.load_parameters(houdini, 'Object/axisA1')

    geometry_builder = SphereControlGeometryBuilder()

    control_builder = HoudiniParameterControlBuilder()
    control_builder.set_geometry_builder(geometry_builder)
    control_builder.set_control_parameter(parameters['len'])
    control_builder.set_control_rate_limiter(RateLimiter(10))

    single_builder = SingleControlGroupBuilder()
    single_builder.set_ui_context(ui_context)
    single_builder.set_control_builder(control_builder)

    axis = ControllableSceneNode('axis', StaticObject.create('axisA11'))
    axis.add_control(single_builder.set_parent(axis).build())
    axis.node.setPosition(-1, 2, -10)
    axis.node.rotate(Vector3(0, 1, 0), math.radians(-45), Space.Local)

    light = Light.create()
    light.setPosition(0, 4, 0)

    manager = SelectionManager(ui_context)
    manager.add(axis)

    def on_event():
        manager.on_event()

    setEventFunction(on_event)
