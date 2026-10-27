import sys
import os
import subprocess

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    nexus_root = os.path.dirname(script_dir)
    
    if nexus_root not in sys.path:
        sys.path.insert(0, nexus_root)
    
    libs_dir = os.path.join(nexus_root, 'nexus', 'libs')
    os.makedirs(libs_dir, exist_ok=True)
    if libs_dir not in sys.path:
        sys.path.insert(0, libs_dir)
    
    required = ['psutil']
    missing = []
    for mod in required:
        try:
            __import__(mod)
        except ImportError:
            missing.append(mod)
    
    if missing:
        print('Installing required packages...')
        for pkg in missing:
            try:
                subprocess.check_call([
                    sys.executable, '-m', 'pip', 'install',
                    '--target', libs_dir,
                    '--quiet',
                    pkg
                ])
                print(f'Installed: {pkg}')
            except Exception as e:
                print(f'Failed to install {pkg}: {e}')
    
    sys.path.insert(0, libs_dir)
    
    from nexus.app.main import main as nexus_main
    nexus_main()

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")
