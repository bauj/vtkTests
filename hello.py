import vtk

# Create a cone
# cone = vtk.vtkConeSource()
# cone.SetHeight(3.0)
# cone.SetRadius(1.0)
# cone.SetResolution(50)  # Adjust resolution for finer mesh
# cone.SetCapping(True)

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

# Create a cylinder
cylinder = vtk.vtkCylinderSource()
cylinder.SetHeight(3.0)
cylinder.SetRadius(0.8)
cylinder.SetResolution(50)
cylinder.SetCapping(True)

# Apply the union operation
boolean_filter = vtk.vtkBooleanOperationPolyDataFilter()
boolean_filter.SetOperationToUnion()
boolean_filter.SetInputData(0, cone_transform_filter.GetOutput())
boolean_filter.SetInputData(1, cylinder.GetOutput())
boolean_filter.Update()

# Triangulate the cone and cylinder for better Boolean operation
cone_triangulator = vtk.vtkTriangleFilter()
cone_triangulator.SetInputConnection(cone_transform_filter.GetOutputPort())
cone_triangulator.Update()

cylinder_triangulator = vtk.vtkTriangleFilter()
cylinder_triangulator.SetInputConnection(cylinder.GetOutputPort())
cylinder_triangulator.Update()

# Create mappers for cone, cylinder, and union result
cone_mapper = vtk.vtkPolyDataMapper()
cone_mapper.SetInputConnection(cone_triangulator.GetOutputPort())

cylinder_mapper = vtk.vtkPolyDataMapper()
cylinder_mapper.SetInputConnection(cylinder_triangulator.GetOutputPort())

union_mapper = vtk.vtkPolyDataMapper()
union_mapper.SetInputConnection(boolean_filter.GetOutputPort())

# Create actors for cone, cylinder, and union result

union_actor = vtk.vtkActor()
union_actor.SetMapper(union_mapper)
union_actor.GetProperty().SetRepresentationToWireframe()  # Show as wireframe
union_actor.GetProperty().SetColor(0.0, 0.0, 1.0)  # Blue union result

# Renderer and Render Window
renderer = vtk.vtkRenderer()
render_window = vtk.vtkRenderWindow()
render_window.AddRenderer(renderer)

# Render Window Interactor
render_window_interactor = vtk.vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

renderer.AddActor(union_actor)
renderer.SetBackground(0.1, 0.2, 0.4)  # Background color

# Render and interact
render_window.Render()
render_window_interactor.Start()
