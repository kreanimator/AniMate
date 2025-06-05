from .. import bl_info

def get_addon_version_string():
    version = ".".join(map(str, bl_info['version']))
    try:
        from ..__dev_build__ import __dev_build__
        version += f" (dev: {__dev_build__})"
    except Exception:
        pass
    return version 
