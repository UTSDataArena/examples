# Omegalib / osg camera handling
The main interaction between omegalib and osg concerns the setting and updating of cameras. When implementing or porting an application with dynamic cameras, which can move around, rotate/orbit, etc. care must be taken to apply the correct transform.
In osg, cameras can be part of the scene graph in lower levels. When their reference frame is set to RELATIVE_RF, they will reference all underlying geomertry from a relative coordinate frame. However omega cameras are commonly set in an absolute reference frame. When calculating transforms, e.g. taking the output of a osg camera manipulator, care must be taken to convert the local transform into the world transform. 

An example for such a transformation is the updateCamera method of the nodetrackermanipulator, which orbits around a tracked node and sets the camera in every frame. The nodetrackermanipulator computes a center and rotation around the tracked node and when updating the camera, it uses the inverse of this transform to set its lookat:

```cpp
void NodeTrackerManipulator::updateCamera(osg::Camera& camera) 
{ 
	osg::Vec3d eye, center, up, unused;
    osg::Matrixd invMatrix = getInverseMatrix();
	invMatrix.getLookAt(eye, center, up);
	camera.setViewMatrixAsLookAt(eye,center,up);
}
```
The *omega::Camera* also has a lookat method, however, if you update the *omega::Camera* by using its lookat method, it will produce weird, incorrect rotations, which are a symptom of the wrong coordinate frame of the center vector: The coordinate frame of the calculated center vector is in the camera view space but should really be in the world space.

```cpp
void NodeTrackerManipulator::updateOmegaCamera(omega::Camera *cam){
    osg::Vec3d eye, unused_center, up;

    // call same method, that osg internally uses for its camera updates
    osg::Matrixd invMatrix = getInverseMatrix();
	invMatrix.getLookAt(eye, unused_center, up);

   	osg::NodePath nodePath;
   	//get the path from the tracked node to the top level element
   	getTrackNodePath().getNodePath(nodePath);
   	//compute a transform from the tracked node space to world space
    osg::Matrixd localToWorld = osg::computeLocalToWorld(nodePath, true);
    // apply this transformation to the cameramanipulator center
    // this is normally the tracked node center, but might be panned
    osg::Vec3d worldCenter = _center * localToWorld;

    omega::Vector3f oCenterVec = OSGVEC3_OMEGA(worldCenter);
    // set the lookat of omega camera
    //order is important here, setting lookat before position 
    // will result in choppy camera rotation
    cam->setPosition( OSGVEC3_OMEGA(eye) );
    cam->lookAt(oCenterVec, OSGVEC3_OMEGA(up) );     
}
```

### Executing pre-render cameras

In osg, cameras can have different render orders: Pre-render, normal, and post-render.
Pre-render cameras are often used, to render a certain effect into a texture, which are then used in the actual rendering of the scene. A common use case is rendering reflections on surfaces.

In our game, we want to render a very shiny surface. A pre-render camera is used, to render the scene with a flipped z-transform:

(todo: extract and insert snapshot from presentation)

Our camera therefore moves with the main camera and its position has to be updated accordingly. Setting the transformation of the reflection camera at the right time is crucial, because setting it too late will result in the reflection lagging one frame behind and too early will result in the main camera not being updated with the new transform yet. A hacky method  could be to directly copy over the main camera transform to the reflection camera, when it is set in the cameramanipulator. However, this could break as soon as we have other methods influencing the camera position: imagine a method setting the field of view dynamically or a method preventing cameras flying into obstacles. Another problem is, that in omega multiple windows can be created on one machine, each update method is therefore executed once for each camera.If you have two windows, you will probably see constantly switching reflections between the windows, because the transform is applied to the wrong reflection camera. What we actually want is to have a camera callback executed right before the reflection camera is rendered. 

In osg, the cull traverse decides what objects to render and what to cull away. The Cullvisitor actually computes the correct transformation of each node and pushes objects into the the draw stage, which is executed after the Cullvisitor has visited all nodes. Therefore, the CullCallback is the latest point, we can influence a nodes transform before it is rendered. However the cullcallback is executed after the node transforms have already been pushed into the render stage.If we would therefore execute the cullcallback directly on the camera, we would not see any positional change. We must therefore set the cullcallback on a node above the camera (we named it cameragroup) and then access its child:

```cpp
class CUpdateCameraCallback : public osg::NodeCallback
{
public:	
	CUpdateCameraCallback() : NodeCallback(){}
	void operator()(osg::Node *node, osg::NodeVisitor *nv)
	{
	    // only execute this callback if in the culling stage
		if (nv->getVisitorType() == osg::NodeVisitor::CULL_VISITOR)
		{
		    // the camera is the only child of the camera group
			osg::Camera	*camera = dynamic_cast<osg::Camera *>(node->asGroup()->getChild(0));
			// The cullvisitor holds information about the current (main) camera
			osgUtil::CullVisitor* cv = static_cast<osgUtil::CullVisitor*>(nv);

			if (camera != NULL)
			{
			    // copy over the transforms of the main camera
				camera->setProjectionMatrix(cv->getCurrentCamera()->getProjectionMatrix() );
				camera->setViewMatrix(cv->getCurrentCamera()->getViewMatrix());
				// set the eye point in the shader
				g_cameraEyeU->set(cv->getEyePoint());
			}
		}
		this->traverse(node, nv);
	}
};
```

Now we show , how to set up the camera correctly:
```cpp
	cameraGroup = new osg::Group();
	m_reflectionCamera = new osg::Camera();
	reflectionTransform = new osg::MatrixTransform();
	
	cameraGroup->addChild(m_reflectionCamera);
	m_reflectionCamera->addChild(reflectionTransform);

    m_reflectionCamera->setClearMask(GL_DEPTH_BUFFER_BIT | GL_COLOR_BUFFER_BIT);
    // render the camera before the main camera
	m_reflectionCamera->setRenderOrder(osg::Camera::PRE_RENDER);
	// write into a frame buffer later used as texture
	m_reflectionCamera->setRenderTargetImplementation(osg::Camera::FRAME_BUFFER_OBJECT);
	// prevent near clipping
	m_reflectionCamera->setComputeNearFarMode(osg::CullSettings::DO_NOT_COMPUTE_NEAR_FAR);
	// calculate all transforms in world space
	m_reflectionCamera->setReferenceFrame(osg::Transform::ABSOLUTE_RF);
	// set the viewport to the size of the texture
	m_reflectionCamera->setViewport(0, 0, texSize, texSize);
	m_reflectionCamera->setClearDepth(1.0);

    //Important: set our cull callback on the cameragroup, not the camera itself
	m_cameraGroupCallback = new CUpdateCameraCallback();
	cameraGroup->setCullCallback(m_cameraGroupCallback);
```

Calculating the actual reflection does not need any extra adjustements for distributed rendering, but is shown here for reference:
```cpp
    // add a clipping plane, to clip everything below z=0.0. 
    //beware, that vec4(a,b,c,d) is a plane equation with a,b,c the plane normal and d the plane height
	m_reflectionClipPlane = new osg::ClipPlane(0, osg::Vec4d(0.0, 0.0, 1.0, 0.0));
	m_reflectionClipNode = new osg::ClipNode;
	m_reflectionClipNode->addClipPlane(m_reflectionClipPlane);
	reflectionTransform->addChild(m_reflectionClipNode);
	// mirror the scene along the z axis
	reflectionTransform->setMatrix(osg::Matrix::scale(1.0, 1.0, -1.0));

    // render the reflection camera into a texture
	osg::ref_ptr<osg::Texture2D> texture = new osg::Texture2D();
	texture->setTextureSize(texSize, texSize);
	m_reflectionCamera->attach((osg::Camera::BufferComponent) osg::Camera::COLOR_BUFFER0, texture);

    osg::StateSet *cameraState = m_reflectionCamera->getOrCreateStateSet();
	cameraState->setMode(GL_CULL_FACE, osg::StateAttribute::OFF | osg::StateAttribute::OVERRIDE);
	// Set reflection textures
	osg::StateSet* floorStateSet = reflectingSurface->getOrCreateStateSet();
	floorStateSet->setTextureAttributeAndModes(0, texture, osg::StateAttribute::ON);
```
The complete reflection code is found in source/view/reflection.cpp and shaders/grid.(vert|frag)
