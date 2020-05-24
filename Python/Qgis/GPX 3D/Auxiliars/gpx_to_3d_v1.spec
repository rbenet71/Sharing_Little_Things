# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['gpx_to_3d.py'],
             pathex=['C:\\Roberto\\Visual_Studio_Code\\Sharing_Little_Things\\Python\\Qgis\\GPX 3D'],
             binaries=[],
             datas=[],
             hiddenimports=['PyQt5.QtSql','PyQt5.QtNetwork','PyQt5.QtXml','PyQt5.Qsci','PyQt5.QtPrintSupport'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='gpx_to_3d',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
        upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='gpx_to_3d')
