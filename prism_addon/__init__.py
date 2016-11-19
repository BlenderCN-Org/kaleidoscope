bl_info = {
    "name": "Prism - A small package of nodes for Cycles Materials",
    "author": "Akash Hamirwasia",
    "version": (1, 0),
    "blender": (2, 75, 0),
    "location": "Cycles > NodeEditor > MaterialView > Add Node Menu",
    "description": "A Complete Toolkit of Nodes to Make your Materials even more colorful and physically accurate",
    "warning": "",
    "wiki_url": "http://www.blenderskool.cf",
    "tracker_url": "http://bit.ly/prismbugbs",
    "category": "Node"}


if "bpy" in locals():
    import importlib
    importlib.reload(spectrum)
    importlib.reload(intensity)
else:
    from . import spectrum, intensity

import bpy
import bpy.utils.previews
import nodeitems_utils, zipfile, os
from nodeitems_utils import NodeCategory, NodeItem
from bpy_extras.io_utils import ImportHelper, ExportHelper

class PrismCategory(NodeCategory):
    @classmethod
    def poll(cls, context):
        b = False
        if context.space_data.tree_type == 'ShaderNodeTree':
            b = True
        return b

# all categories in a list
node_categories = [
    PrismCategory("PRISMNODES", "Prism", items=[
        NodeItem("spectrum_palette.node"),
        NodeItem("intensity.node")
        ]),
    ]

class Prism(bpy.types.AddonPreferences):
    bl_idname = __name__

    def draw(self, context):
        prism_spectrum_props=bpy.context.scene.prism_spectrum_props
        layout = self.layout
        box = layout.box()
        col = box.column()
        row = col.row()
        row.alignment ='CENTER'
        row.label("INSTALLING FILES")
        col.label()
        col.label("1) Download the .zip files which has the files to import. DO NOT EXTRACT IT")
        col.label("2) Click the 'Import Files' button below, and select the .zip file")
        col.label("     NOTE: SELECT ONLY 1 ZIP FILE ONCE")
        col.label("3) Click the 'Install Files' button. The files should be installed")
        col.label()
        row = col.row()
        row.scale_y = 1.2
        row.label("")
        row.operator(PrismImport.bl_idname, text='Import Files', icon='PACKAGE') #Install Presets button
        row.label("")
        col.separator()
        row = col.row()
        row.scale_y = 1.12
        row.label("")
        row.operator(PrismExport.bl_idname, text='Export Files', icon='OOPS') #Install Presets button
        row.label("")
        if bpy.context.scene.prism_props_import_files == True:
            col.label("There was a problem in importing the files.", icon='ERROR')
        col.label()
        col.prop(prism_spectrum_props, "sync_path", text="Path to Sync Palettes")
        col.separator()

        box2 = box.box()
        col2 = box2.column(align=True)
        if prism_spectrum_props.sync_help == False:
            col2.prop(prism_spectrum_props, "sync_help", text="View Information for Syncing Palettes", toggle=True, icon='LAYER_USED')
        else:
            col2.prop(prism_spectrum_props, "sync_help", text="Hide Information for Syncing Palettes", toggle=True, icon='LAYER_ACTIVE')
            col3 = box2.column(align=True)
            col3.separator()
            col3.label("Prism add-on has the feature to sync the Saved Palettes of Spectrum Node in a cloud storage.")
            col3.label("This allows you to Use Saved palettes on any system, anywhere.")
            col3.label()
            col3.label("Instructions to setup Syncing of Palettes:")
            col3.label("   1) Start by signing up with a Cloud Storage Service (Eg. Dropbox, Google Drive, etc.)")
            col3.label("   2) Then install the Desktop Application (NOTE: Only Popular Cloud Services Provide this)")
            col3.label("   3) Select the Sync folder that was created by Desktop Application, in the sync path above")
            col3.label()
            col3.label("It's done. Whatever is saved in that folder, would automatically transfer to the Cloud which can be used later on.")
            col3.label()
            row3 = col3.row(align=True)
            row3.alignment='CENTER'
            row3.label("Keys:")
            row3 = col3.row(align=True)
            row3.alignment='CENTER'
            row3.label("- Palette saved Locally, and is NOT synced.", icon='FILE')
            row3 = col3.row(align=True)
            row3.alignment='CENTER'
            row3.label("- Palette is NOT saved Locally, but is synced.", icon='WORLD')
            row3 = col3.row(align=True)
            row3.alignment='CENTER'
            row3.label("- Palette is saved Locally and synced too.", icon='URL')
            col3.separator()
            col3.separator()
            row = col3.row(align=True)
            row.scale_y = 1.15
            row.label()
            row.operator('wm.url_open', text="Video Tutorial", icon='CLIP').url = "http://www.blenderskool.cf"
            row.label()
            col3.separator
        col4 = box.column(align=True)
        col4.separator()
        row4 = col4.row()
        split = row4.split(percentage=0.8)
        col4_1s = split.column(align=True)
        row4 = col4_1s.row()
        row4.separator()
        row4.operator('wm.url_open', text="", icon_value=icons_dict["twitter"].icon_id, emboss=False).url="http://www.twitter.com/blenderskool"
        row4.operator('wm.url_open', text="", icon_value=icons_dict["googleplus"].icon_id, emboss=False).url="https://plus.google.com/+AkashHamirwasia1"
        row4.operator('wm.url_open', text="", icon_value=icons_dict["youtube"].icon_id, emboss=False).url="http://www.youtube.com/AkashHamirwasia1"
        row4.operator('wm.url_open', text="", icon_value=icons_dict["blenderskool"].icon_id, emboss=False).url="http://www.blenderskool.cf"
        row4_1 = row4.row(align=True)
        row4_1.alignment = 'CENTER'
        row4_1.label("Created by Akash Hamirwasia")
        col4_2s = split.column(align=True)
        row4_2 = col4_2s.row()
        row4_2.scale_y = 1.2
        row4_2.operator('wm.url_open', text="Donate", icon='SOLO_ON').url="http://bit.ly/donatetobs"

class PrismImport(bpy.types.Operator, ImportHelper): #Importing Presets
    """Install .zip file in the add-on"""
    bl_idname = "prism.install_files"
    bl_label = "Install Files"

    filename_ext = ".zip"

    filter_glob = bpy.props.StringProperty(
            default="*.zip",
            options={'HIDDEN'},
            )
    def execute(self, context):
        try:
            zipref = zipfile.ZipFile(self.filepath, 'r')
            path = os.path.dirname(__file__)
            if (path != ""):
                zipref.extractall(path) #Extract to the Enrich add-on Folder
                zipref.close()
                bpy.conte
            bpy.context.scene.prism_props_import_files = False
        except:
            bpy.context.scene.prism_props_import_files = True
        return {'FINISHED'}

class PrismExport(bpy.types.Operator, ExportHelper):
    """Export the Color Palettes in a .zip format"""
    bl_idname = 'prism.export_files'
    bl_label = 'Export Files'

    filename_ext = ".zip"

    filter_glob = bpy.props.StringProperty(
            default="*.zip",
            options={'HIDDEN'}
            )

    def execute(self, context):
        try:
            if self.filepath.endswith(".zip") == False:
                self.filepath = self.filepath+".zip"

            zf = zipfile.ZipFile(self.filepath, "w", zipfile.ZIP_DEFLATED)
            path = os.path.dirname(__file__)
            abs_src = os.path.abspath(path)
            for dirname, subdirs, files in os.walk(path):
                if '__pycache__' in subdirs:
                    subdirs.remove('__pycache__')
                for filename in files: #Do not include the main code files
                    if filename.endswith(".json"):
                        absname = os.path.abspath(os.path.join(dirname, filename))
                        arcname = absname[len(abs_src) + 1:]
                        zf.write(absname, arcname)
            zf.close()
            self.report({'INFO'}, "Palettes Exported Successfully to "+self.filepath)
        except:
            self.report({'ERROR'}, "There was an error, please check the file path!")
        return{'FINISHED'}

def register():
    try:
        bpy.utils.register_module(__name__)
    except:
        pass
    global icons_dict
    spectrum.register()
    intensity.register()
    icons_dict = bpy.utils.previews.new()
    icons_dir = os.path.join(os.path.dirname(__file__), "icons")
    icons_dict.load("blenderskool", os.path.join(icons_dir, "blenderskool_logo.png"), 'IMAGE')
    icons_dict.load("youtube", os.path.join(icons_dir, "youtube_icon.png"), 'IMAGE')
    icons_dict.load("twitter", os.path.join(icons_dir, "twitter_icon.png"), 'IMAGE')
    icons_dict.load("googleplus", os.path.join(icons_dir, "googleplus_icon.png"), 'IMAGE')
    bpy.types.Scene.prism_props_import_files = bpy.props.BoolProperty(name="Prism Import", description="Checks if the zip file is properly imported", default=False)
    nodeitems_utils.register_node_categories("PRISM_NODES", node_categories)

def unregister():
    global icons_dict
    bpy.utils.previews.remove(icons_dict)
    nodeitems_utils.unregister_node_categories("PRISM_NODES")
    spectrum.unregister()
    intensity.unregister()
    del bpy.types.Scene.prism_props_import_files
    bpy.utils.unregister_module(__name__)
