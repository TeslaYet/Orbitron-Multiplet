# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['multiplet_gui.py'],
    pathex=[],
    binaries=[],
    datas=[('multiplet', '.'), ('requirements.txt', '.'), ('GUI_README.md', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='Orbitron-Multiplet',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['cube-molecule_icon-icons.com_53025.icns'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='Orbitron-Multiplet',
)
app = BUNDLE(
    coll,
    name='Orbitron-Multiplet.app',
    icon='cube-molecule_icon-icons.com_53025.icns',
    bundle_identifier=None,
)
