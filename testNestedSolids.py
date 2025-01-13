import vtk

# Create a sphere source with radius 10
sphere1 = vtk.vtkSphereSource()
sphere1.SetRadius(10)
sphere1.SetPhiResolution(100)
sphere1.SetThetaResolution(100)
sphere1.Update()

# Create a sphere source with radius 5
sphere2 = vtk.vtkSphereSource()
sphere2.SetRadius(5)
sphere2.SetPhiResolution(100)
sphere2.SetThetaResolution(100)
sphere2.Update()

# Create a clipping plane (normal to -Z, passing through the origin)
plane = vtk.vtkPlane()
plane.SetOrigin(0, 0, 0)
plane.SetNormal(0, 0, -1)

# Create a vtkPlaneCollection and add the plane to it
plane_collection = vtk.vtkPlaneCollection()
plane_collection.AddItem(plane)

# Create a clipper for the first sphere (large sphere)
clipper1 = vtk.vtkClipPolyData()
clipper1.SetInputData(sphere1.GetOutput())
clipper1.SetClipFunction(plane)
clipper1.Update()

# Create a clipper for the second sphere (small sphere)
clipper2 = vtk.vtkClipPolyData()
clipper2.SetInputData(sphere2.GetOutput())
clipper2.SetClipFunction(plane)
clipper2.Update()

# Create a composite poly data mapper for the multi-block dataset
multi_block = vtk.vtkMultiBlockDataSet()
multi_block.SetBlock(0, clipper1.GetOutput())  # Set clipped large sphere as block 0
multi_block.SetBlock(1, clipper2.GetOutput())  # Set clipped small sphere as block 1

# Create a composite poly data mapper and set the multi-block dataset as input
multi_block_mapper = vtk.vtkCompositePolyDataMapper()
multi_block_mapper.SetInputDataObject(multi_block)

# Create the actor
multi_block_actor = vtk.vtkActor()
multi_block_actor.SetMapper(multi_block_mapper)

# Set colors for the blocks in the multi-block dataset
multi_block_mapper.SetBlockColor(0, 1, 0, 0)  # Red for the large sphere (block 0)
multi_block_mapper.SetBlockColor(1, 0, 0, 1)  # Blue for the small sphere (block 1)

# Create a renderer, render window, and interactor
renderer = vtk.vtkRenderer()
render_window = vtk.vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(1024, 1024)  # Set window size to 1024x1024

render_window_interactor = vtk.vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Add the actor to the renderer
renderer.AddActor(multi_block_actor)
renderer.SetBackground(0.1, 0.1, 0.1)  # Set background to dark gray

# Start the render window interactor
render_window.Render()
render_window_interactor.Start()
