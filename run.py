from OBlog import app
import sys


if __name__ == '__main__':
    args = sys.argv
    if len(sys.argv) == 1:
        app.run(debug=True, threaded=True)
    else:
        import importlib
        importlib.import_module('tools.'+args[1])
        
            
