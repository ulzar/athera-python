"""
These functions are helpers to generate the argument set required by Athera Compute job submissions, for different apps.

They follow the pattern provided by Compute submission plugins for in-Athera Apps. Some are recognizably the app arguments, others are interpreted by a script.

Placeholders are interpreted during Job creation, to enable splitting of Job frame ranges for a set of Parts.
"""
def get_houdini_arguments(output):
    return [
        "{{FRAME_RANGE_START}}",
        "{{FRAME_RANGE_FINISH}}",
        "{{FRAME_RANGE_INCREMENT}}",
        "{{FILE_PATH}}",
        output
    ]

def get_katana_arguments(render_node):
    return [
        "--batch",
        "--render-node",
        render_node,
        "--katana-file",
        "{{FILE_PATH}}",
        "-t",
        "{{FRAME_RANGE_START}}-{{FRAME_RANGE_FINISH}}"
    ]

def get_modo_arguments():
    return [
        "{{FILE_PATH}}",
        "default", # Output location not used, setting to default
        "{{FRAME_RANGE_START}}",
        "{{FRAME_RANGE_FINISH}}",
        "{{FRAME_RANGE_INCREMENT}}"
    ]

def get_nuke_arguments(write_node):
    return [
        "-X",
        write_node,
        "{{FILE_PATH}}",
        "{{FRAME_RANGE_START}}-{{FRAME_RANGE_FINISH}}"
    ]

