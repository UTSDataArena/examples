import os
import math

from cyclops import *
from omegaToolkit import *

from daInput import *
from daHEngine import *
from daHandles import *

if __name__ == '__main__':
    """
    This simple example demonstrates how to load geometry from a Houdini digital 
    asset and attach handles to multiple different parameters that are also 
    exported by the asset (and used to adjust the underlying geometry). It shows
    how to use the following features of the daHandles omegalib module:

        - How to use a complex control group, which maps individual Houdini
          Engine parameters to individual controls within the group
        - How to apply a minimum and maximum value to a parameter loaded from
          the Houdini Engine
    """

    path = os.path.dirname(__file__)
    if not path:
        path = os.getcwd()

    resources = os.path.join(path, 'resources')

    ui_context = UiContext()

    getDefaultCamera().setControllerEnabled(False)

    houdini = HoudiniEngine.createAndInitialize()
    houdini.setLoggingEnabled(False)

    houdini.loadAssetLibraryFromFile(os.path.join(resources, 'otl', 'sphere.hdanc'))
    houdini.instantiateAsset('Object/sphere')
    geo = houdini.instantiateGeometry('sphere1')

    parameters = HoudiniParameter.load_parameters(houdini, 'Object/sphere')

    control_builder = HoudiniParameterControlBuilder()
    control_builder.set_geometry_builder(CylinderControlGeometryBuilder())
    control_builder.set_increment(Scale.INCREMENT)
    control_builder.set_rate_limiter(RateLimiter(10))

    group_builder = HoudiniParameterScaleControlGroupBuilder()
    group_builder.set_ui_context(ui_context)
    group_builder.set_control_builder(control_builder)
    group_builder.set_bounding_box((geo.getBoundMinimum(), geo.getBoundMaximum()))
    group_builder.set_parameter_mapping({Axis.X_AXIS: parameters['radx'], 
                                         Axis.Y_AXIS: parameters['rady'], 
                                         Axis.Z_AXIS: parameters['radz']})
    group_builder.set_min_value(0.1)
    group_builder.set_max_value(2.0)

    sphere = ControllableSceneNode('sphere', geo)
    sphere.add_control(group_builder.set_parent(sphere).build())
    sphere.node.setPosition(Vector3(0, 1.5, -10))
    sphere.node.rotate(Vector3(0, 1, 0), math.radians(-45), Space.Local)

    light = Light.create()
    light.setPosition(0, 5, -2)
    light.setColor(Color(1.0, 1.0, 1.0, 1.0))
    light.setAmbient(Color(0.2, 0.2, 0.2, 1.0))

    manager = SelectionManager(ui_context)
    manager.add(sphere)

    def on_event():
        manager.on_event()

    setEventFunction(on_event)
