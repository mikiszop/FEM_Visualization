import vtk
import pyvista as pv
#Name of the .k or .txt data file with *NODE and *ELEMENT_SOLID sections
f = open('file.k')

uGrid = pv.UnstructuredGrid()
points = vtk.vtkPoints()
stress = vtk.vtkFloatArray()
stress.SetName('Stress')

line = f.readline()
#empty nodes for proper id acusition
points.InsertNextPoint(0,0,0)
#empty nodes for proper id acusition
stress.InsertNextTuple1(0)
for line in iter(lambda: f.readline(), ""):
    if '*NODE' in line:
        continue
    if '*ELEMENT_SOLID' in line:
        break
    v = line.split(',')
    #insert x, y, z
    points.InsertNextPoint(float(v[1]),
                           float(v[2]),
                           float(v[3]))
    #insert value
    stress.InsertNextTuple1(float(v[4]))

for line in iter(lambda: f.readline(), ""):
    if '*ELEMENT_SOLID' in line:
        continue
    if '*END' in line:
        break
    v = line.split(',')
    #create hexahedron VTK object
    hex = vtk.vtkHexahedron()
    #addding vertex x 8
    hex.GetPointIds().SetId(0,int(v[9]))
    hex.GetPointIds().SetId(1,int(v[8]))
    hex.GetPointIds().SetId(2,int(v[7]))
    hex.GetPointIds().SetId(3,int(v[6]))
    hex.GetPointIds().SetId(4,int(v[5]))
    hex.GetPointIds().SetId(5,int(v[4]))
    hex.GetPointIds().SetId(6,int(v[3]))
    hex.GetPointIds().SetId(7,int(v[2]))
    #adding each hexahedron to UnstructuredGrid
    uGrid.InsertNextCell(hex.GetCellType(), hex.GetPointIds())
f.close()
# adding nodes (x, y, z) array
uGrid.SetPoints(points)
# adding nodes values array
uGrid.GetPointData().AddArray(stress)
plotter = pv.Plotter()
plotter.add_mesh(uGrid)
# py vista show scene and screenshot save
plotter.show(screenshot='beam.png')
