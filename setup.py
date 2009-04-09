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
                "script": 'ProxyApp.py',
                "other_resources": [(24,1,manifest)],
                'icon_resources': [(1, 'websniffer.ico')]
                }],
      options = {"py2exe": {"optimize": 2,
                            "compressed": 1,
                            'includes': ['MainFrame', 'RequestTree', 'TextCtrl'],
                            "bundle_files": 1}},
      zipfile = None,
      name="WebSniffer",
      description="The web debug proxy",
      version='0.0.1',
      author="yinzhigang",
      author_email="sxin.net@gmail.com",
      data_files = [
        ('websniffer.ico', 'websniffer.ico'),
      ]
      )