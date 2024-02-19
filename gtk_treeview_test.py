#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Module to a GTK+ window with a treeview control.
'''

# System libraries for the initial phase.
import sys
import os
import platform
import argparse

# Application librararies.





if __name__ == '__main__':
    # Process the command line arguments.
    # This might end the program (--help).
    argParse = argparse.ArgumentParser(prog='gtk_treeview_test', description='Display a treeview control.')
    argParse.add_argument('-i', '--install', help='Install the program and desktop link.', action='store_true')
    argParse.add_argument('-u', '--uninstall', help='Uninstall the program.', action='store_true')
    argParse.add_argument('-3', '--gtk3', help='Use GTK3.', action='store_true')
    argParse.add_argument('-4', '--gtk4', help='Use GTK3.', action='store_true')
    args = argParse.parse_args()

    if args.install:
        print('Not implemented.')
        sys.exit(0)

    if args.uninstall:
        print('Not implemented.')
        sys.exit(0)

    # Welcome message.
    print('\033[1;31mGTK+ Treeview Test\033[0;m by Steve Walton.')
    print('Python Version {}.{}.{} (expecting 3).'.format(sys.version_info.major, sys.version_info.minor, sys.version_info.micro))
    print('Operating System is "{}".  Desktop is "{}".'.format(platform.system(), os.environ.get('DESKTOP_SESSION')))

    if args.gtk3:
        import gtk3.main_window
        # Main GTK loop.
        mainWindow = gtk3.main_window.MainWindow(args)
        mainWindow.runMainLoop()
    else:
        import gtk4.main_window
        # Main GTK loop.
        app = gtk4.main_window.TreeViewApp(application_id='com.example.GtkApplication')
        app.run()


    # A final message
    print('Goodbye from the \033[1;31mGTK+ Treeview Test\033[0;m program.')
