# encoding: utf-8
import sys, glob

data_files = [
            ('images', ['images/websniffer.ico']),
            ('images/toolbar', glob.glob("images/toolbar/*.png")),
            ('images/menu', glob.glob("images/menu/*.png")),
            ('window', glob.glob('window/window.xrc')),
            ]
includes = ['MainFrame', 'RequestTree', 'TextCtrl', 'Preferences']

if sys.platform == 'win32':
    from distutils.core import setup
    import py2exe
    
    manifest = """
    <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
    <assembly xmlns="urn:schemas-microsoft-com:asm.v1"
    manifestVersion="1.0">
    <assemblyIdentity
    version="0.64.1.0"
    processorArchitecture="x86"
    name="Controls"
    type="win32"
    />
    <description>WebSniffer</description>
    <dependency>
    <dependentAssembly>
    <assemblyIdentity
    type="win32"
    name="Microsoft.Windows.Common-Controls"
    version="6.0.0.0"
    processorArchitecture="X86"
    publicKeyToken="6595b64144ccf1df"
    language="*"
    />
    </dependentAssembly>
    </dependency>
    </assembly>
    """
    
    setup(
          windows=[{
                    "script": 'WebSniffer.py',
                    "other_resources": [(24,1,manifest)],
                    'icon_resources': [(0, 'images/websniffer.ico')]
                    }],
          options = {"py2exe": {"optimize": 2,
                                "compressed": 1,
                                'includes': includes,
                                "bundle_files": 1}},
          zipfile = None,
          name="WebSniffer",
          description="The web debug proxy",
          version='0.1.0',
          author="yinzhigang",
          author_email="sxin.net@gmail.com",
          data_files = data_files
          )
elif sys.platform == 'linux2':
    from cx_Freeze import setup, Executable

    setup(
        name = "WebSniffer",
        version = "0.1.0",
        description = "The web debug proxy",
        data_files = data_files,
        options = dict(
                     build_exe = dict(includes = includes,
                                packages=['encodings'],
                                compressed = True,
                                ),
                  ),
        executables = [Executable("WebSniffer.py")]
    )
elif sys.platform == 'darwin':
    from distutils.core import setup
    import py2app
    
    setup(
        options=dict(
            py2app=dict(
                iconfile='images/websniffer.icns',
                optimize = 2,
                includes = includes,
                #resources=['resources/License.txt'],
                plist=dict(
                    CFBundleName               = "WebSniffer",
                    CFBundleShortVersionString = "0.1.0",     # must be in X.X.X format
                    CFBundleGetInfoString      = "WebSniffer 0.1.0",
                    CFBundleExecutable         = "WebSniffer",
                    CFBundleIdentifier         = "cn.websniffer.WebSniffer",
                ),
            ),
        ),
        data_files = data_files,
        app=[ 'WebSniffer.py' ]
    )
