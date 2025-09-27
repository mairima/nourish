import importlib, traceback, sys
print("cwd:", sys.path[0])
importlib.invalidate_caches()
try:
    importlib.import_module("profiles")
    print("OK: imported profiles")
except Exception:
    traceback.print_exc()
