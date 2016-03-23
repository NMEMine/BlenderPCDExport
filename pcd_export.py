bl_info = {
    "name": "PCD Exporter",
    "author": "Michael Bechtel",
    "version": (0, 1),
    "blender": (2, 74, 0),
    "location": "File->Export",
    "description": "Export vertices of active object into .pcd format",
    "category": "Import-Export"}
    

import bpy, textwrap

pcd_header = textwrap.dedent("""\
    # .PCD v.7 - Point Cloud Data file format
    VERSION .7
    FIELDS x y z  
    SIZE 4 4 4
    TYPE F F F
    COUNT 1 1 1
    WIDTH %(n_vertices)i
    HEIGHT 1
    VIEWPOINT 0 0 0 1 0 0 0
    POINTS %(n_vertices)i
    DATA ascii\n""")

class PointCloudExporter(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.pcd_export"
    bl_label = "Export PCD"
    bl_options = {'REGISTER', 'UNDO'}

    filepath = bpy.props.StringProperty(subtype = 'FILE_PATH')

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        vertices = context.active_object.data.vertices
        file = open(self.filepath,'w')
        file.write(pcd_header % {"n_vertices": len(vertices)})
        
        # iterate over all vertices of active object and write coordinates to file
        for vertex in vertices:
            vert_string = "%(x)f %(y)f %(z)f\n" % {"x" : vertex.co[0], "y" : vertex.co[1], "z" : vertex.co[2]}
            file.write(vert_string)
        file.close()
      
        return {'FINISHED'}
        
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

def register():
    bpy.utils.register_class(PointCloudExporter)


def unregister():
    bpy.utils.unregister_class(PointCloudExporter)


if __name__ == "__main__":
    register()
