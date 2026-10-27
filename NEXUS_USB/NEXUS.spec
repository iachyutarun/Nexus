# -*- mode: python ; coding: utf-8 -*-
import os

nexus_root = r'H:\NEXUS_USB'
datas = [
    (os.path.join(nexus_root, 'nexus', 'config'), 'nexus/config'),
    (os.path.join(nexus_root, 'nexus', 'assets'), 'nexus/assets'),
]
if os.path.exists(os.path.join(nexus_root, 'models')):
    datas.append((os.path.join(nexus_root, 'models'), 'models'))

a = Analysis(
    [os.path.join(nexus_root, 'nexus', 'app', 'bootstrap.py')],
    pathex=[nexus_root],
    binaries=[],
    datas=datas,
    hiddenimports=[
        'psutil',
        'nexus',
        'nexus.core',
        'nexus.core.utils',
        'nexus.config',
        'nexus.config.settings',
        'nexus.ui',
        'nexus.ui.login',
        'nexus.ui.terminal',
        'nexus.ai',
        'nexus.ai.engine',
        'nexus.ai.rule_based',
        'nexus.ai.local_model',
        'nexus.commands',
        'nexus.commands.calculator',
        'nexus.commands.notes',
        'nexus.commands.system',
        'nexus.commands.files',
        'nexus.commands.history',
        'nexus.commands.about',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'ctransformers',
        'huggingface_hub',
        'huggingface',
        'transformers',
        'torch',
        'tensorflow',
        'keras',
        'numpy',
        'PIL',
        'pygame',
        'pydantic',
        'rich',
        'pygments',
        'cryptography',
        'setuptools',
        'pytest',
    ],
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='NEXUS',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)
