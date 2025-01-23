import vtk

# Create a named colors object
colors = vtk.vtkNamedColors()

# Create two spheres
sphere = vtk.vtkSphere()
sphere.SetRadius(1)
sphere.SetCenter(0.5, 0, 0)

sphere2 = vtk.vtkSphere()
sphere2.SetRadius(1)
sphere2.SetCenter(-0.5, 0, 0)

# Create three renderers for different boolean operations
renderers = [vtk.vtkRenderer() for _ in range(3)]

# Set the viewports for each renderer
renderers[0].SetViewport(0, 0, 1.0 / 3.0, 1)         # Difference
renderers[1].SetViewport(1.0 / 3.0, 0, 2.0 / 3.0, 1) # Union
renderers[2].SetViewport(2.0 / 3.0, 0, 1, 1)         # Intersection

# Shared camera (each renderer will adjust its own camera)
camera = vtk.vtkCamera()

# Create a color series
color_series = vtk.vtkColorSeries()
color_series.SetColorScheme(vtk.vtkColorSeries.BREWER_DIVERGING_SPECTRAL_3)

# Loop through each renderer and apply the necessary settings
for i, renderer in enumerate(renderers):

    # Combine the two spheres using vtkImplicitBoolean
    boolean = vtk.vtkImplicitBoolean()
    boolean.AddFunction(sphere)
    boolean.AddFunction(sphere2)

    # Set the boolean operation type for the current renderer
    if i == 0:
        boolean.SetOperationTypeToDifference()
    elif i == 1:
        boolean.SetOperationTypeToUnion()
    else:
        boolean.SetOperationTypeToIntersection()

    # Sample the implicit function
    sample = vtk.vtkSampleFunction()
    sample.SetImplicitFunction(boolean)
    sample.SetModelBounds(-2, 2, -2, 2, -2, 2)
    sample.SetSampleDimensions(200, 200, 200)
    sample.ComputeNormalsOff()

    # Generate a contour
    surface = vtk.vtkContourFilter()
    surface.SetInputConnection(sample.GetOutputPort())
    surface.SetValue(0, 0.0)
    surface.Update()

    # Invert the normals of the polydata
    inverted_normals = vtk.vtkPolyDataNormals()
    inverted_normals.SetInputConnection(surface.GetOutputPort())
    inverted_normals.FlipNormalsOn()
    inverted_normals.Update()

    # Clip with a plane
    plane = vtk.vtkPlane()
    plane.SetOrigin(0.25, 0.0, 0.0)
    plane.SetNormal(-1.0, 0.0, 0.0)  # Inverted normal

    plane_collection = vtk.vtkPlaneCollection()
    plane_collection.AddItem(plane)

    clipper = vtk.vtkClipClosedSurface()
    clipper.SetInputConnection(inverted_normals.GetOutputPort())
    clipper.SetClippingPlanes(plane_collection)
    clipper.SetGenerateFaces(1)  # Generate closed faces

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(clipper.GetOutputPort())
    mapper.ScalarVisibilityOff()

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(colors.GetColor3d("Peacock"))

    # Set the background color for the current renderer
    renderer.SetBackground(
        color_series.GetColor(i).GetRed() / 255.0,
        color_series.GetColor(i).GetGreen() / 255.0,
        color_series.GetColor(i).GetBlue() / 255.0,
    )

    # Assign the camera and actor to the renderer
    renderer.AddActor(actor)

# Create a render window and interactor
render_window = vtk.vtkRenderWindow()
for renderer in renderers:
    render_window.AddRenderer(renderer)

interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Configure the render window
render_window.SetSize(900, 300)
render_window.SetWindowName("ImplicitBooleanDemo with Clipping")

# Render the window
render_window.Render()

# Start the interactor
interactor.Initialize()
interactor.Start()
