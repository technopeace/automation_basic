# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['automation.py'],
    pathex=[],
    binaries=[],
    datas=[('isim_label.png', '.')],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=['matplotlib', 'pandas'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='automation',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_console=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name='automation',
)

app = BUNDLE(
    coll,
    name='Automation.app',
    icon=None,
    bundle_identifier='com.bariskahraman.automation',
)
