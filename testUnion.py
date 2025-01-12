import vtk

# Create a cone

# Create a torus
torus = vtk.vtkParametricTorus()
cone = vtk.vtkParametricFunctionSource()
cone.SetParametricFunction(torus)
cone.Update()

# Transform the cone to overlap with the cylinder
cone_transform = vtk.vtkTransform()
cone_transform.Translate(0, -1.5, 0)
cone_transform_filter = vtk.vtkTransformPolyDataFilter()
cone_transform_filter.SetInputConnection(cone.GetOutputPort())
cone_transform_filter.SetTransform(cone_transform)
cone_transform_filter.Update()

# Triangulate the cone
cone_triangulator = vtk.vtkTriangleFilter()
cone_triangulator.SetInputConnection(cone_transform_filter.GetOutputPort())
cone_triangulator.Update()

# Create a cylinder
cylinder = vtk.vtkCylinderSource()
cylinder.SetHeight(3.0)
cylinder.SetRadius(0.8)
cylinder.SetResolution(100)
cylinder.SetCapping(True)

# Triangulate the cylinder
cylinder_triangulator = vtk.vtkTriangleFilter()
cylinder_triangulator.SetInputConnection(cylinder.GetOutputPort())
cylinder_triangulator.Update()

# Apply the union operation
boolean_filter = vtk.vtkBooleanOperationPolyDataFilter()
boolean_filter.SetOperationToUnion()
boolean_filter.SetInputData(0, cone_triangulator.GetOutput())
boolean_filter.SetInputData(1, cylinder_triangulator.GetOutput())
boolean_filter.Update()

# Check the output
print(f"Union: {boolean_filter.GetOutput().GetNumberOfPoints()} points")

# Create a mapper and actor for the result
mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(boolean_filter.GetOutputPort())

actor = vtk.vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetRepresentationToWireframe()  # Show as wireframe

# Renderer and Render Window
renderer = vtk.vtkRenderer()
render_window = vtk.vtkRenderWindow()
render_window.AddRenderer(renderer)

# Render Window Interactor
render_window_interactor = vtk.vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Add the actor to the scene
renderer.AddActor(actor)
renderer.SetBackground(0.1, 0.2, 0.4)  # Background color

# Render and interact
render_window.Render()
render_window_interactor.Start()
