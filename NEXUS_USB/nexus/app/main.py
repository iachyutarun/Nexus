import sys
import os

def main():
    nexus_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    if nexus_root not in sys.path:
        sys.path.insert(0, nexus_root)
    from nexus.core.utils import ensure_directories
    from nexus.config.settings import settings
    from nexus.ui.login import LoginScreen
    from nexus.ui.terminal import TerminalUI

    ensure_directories()

    def start_terminal(username):
        settings.set('username', username)
        app = TerminalUI(username)
        app.run()

    login = LoginScreen(on_success=start_terminal)
    login.run()

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"Fatal error: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")
