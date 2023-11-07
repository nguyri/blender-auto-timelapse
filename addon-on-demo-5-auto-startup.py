import bpy
import time
import ctypes
import os

global blender_id

interval = 10
path = "C:/tmp/"
    
bl_info =  {'name': 'Screenshot Timelapse',
            'author': 'Richard Nguyen',
            'version': ( 0, 0, 1),
            'blender': ( 3, 0, 0),
            'category': 'Output',
            'location': 'Output -> Right sidebar -> Screen Timelapse',
            'description': 'Takes a timelapse of the entire screen by simply taking screenshots'}

# Define the function
class SimpleOperator(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.simple_operator"
    bl_label = "Simple Object Operator"

    def execute(self, context):
        # the code that the button executes
        run_timer()
        running = bpy.app.timers.is_registered(check_focus)
        report = "" if running else "NOT "
        report = "Screenshot is " + report + "running"
        self.report({'INFO'}, report )
        return {'FINISHED'}

def run_timer():
    running = bpy.app.timers.is_registered(check_focus)
    if (running):
        bpy.app.timers.unregister(check_focus)
    else:
        bpy.app.timers.register(check_focus)
    running = bpy.app.timers.is_registered(check_focus)
    


# Define the panel
class SimplePanel(bpy.types.Panel):
    
    """Creates a Panel in the Object properties window"""
    bl_label = "Auto Screenshot"
    bl_idname = "OBJECT_PT_simple"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "output"

    def draw(self, context):
        layout = self.layout

        # Add a button that calls the function
        layout.operator(SimpleOperator.bl_idname, text="Toggle Auto Screenshot")

def register():
    bpy.utils.register_class(SimpleOperator)
    bpy.utils.register_class(SimplePanel)

def unregister():
    bpy.utils.unregister_class(SimpleOperator)
    bpy.utils.unregister_class(SimplePanel)

# The function that runs the script
def run_script():
    # The code you want to execute
    extension = ".png"

    file_path = path + str(counter) + extension
    bpy.ops.screen.screenshot(filepath=file_path)

# The function that checks the focus
def check_focus():
    # Get the current window
    global counter
#    print(f'in interval, blender_id: {blender_id} active_window():{active_window}')
    
    # Get the handle of the current window
    blender_is_active = blender_id == active_window()
    if blender_is_active:
        run_script()
        counter += 1

    return interval

def active_window(): 
    user32 = ctypes.WinDLL('user32', use_last_error=True)
    current_window = user32.GetForegroundWindow()
    return current_window

# Function to extract numbers from a string
def extract_numbers(filename):
    try:
        # Split the filename by '.' to separate the extension
        name, ext = os.path.splitext(filename)
        # Split the filename by non-digit characters and get the last part
        parts = name.split('_')
        return int(parts[-1])
    except (ValueError, IndexError):
        return None

# Get a list of .png files in the directory
def find_max_png(directory):
    png_files = [filename for filename in os.listdir(directory) if filename.endswith(".png")]

    if not png_files:
        return 0
    else:
        # Extract numbers from the file names and find the maximum
        numbers = [extract_numbers(filename) for filename in png_files]
        numbers = [num for num in numbers if num is not None]  # Remove None values
        if numbers:
            max_number = max(numbers)
            return max_number
        else:
            return 0



if __name__ == "__main__":
    counter = find_max_png(path)
    run_timer()
    global blender_id
    blender_id = active_window()
    register()