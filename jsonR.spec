# -*- mode: python ; coding: utf-8 -*-
import os
import importlib
proot = os.path.dirname(importlib.import_module('praw').__file__)
datas = [(os.path.join(proot, 'praw.ini'), 'praw'), ('icon_transparent.ico', '.')]

block_cipher = None


a = Analysis(['jsonR.py'],
             pathex=[],
             binaries=[],
             datas=datas ,
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
a.datas += [('logo.png', 'D:\\Downloads\\Comment Grabber\\icon_transparent.ico','DATA')]
a.datas += [('client credentials.txt', 'D:\\Downloads\\Comment Grabber\\client credentials.txt', 'DATA')]
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,  
          [],
          name='jsonR',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None,
          icon='D:\\Downloads\\Comment Grabber\\icon_transparent.ico')
