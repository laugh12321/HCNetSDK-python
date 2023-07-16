import sys
import argparse
import shutil
import re
from pathlib import Path
from setuptools import setup, find_packages

# Settings
FILE = Path(__file__).resolve()
PARENT = FILE.parent  # root directory
README = (PARENT / "README.md").read_text(encoding="utf-8")

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--platform', help='Platform')
    parser.add_argument('--library-dirs', nargs='+', help='Library directories')
    return parser.parse_known_args()


def get_version():
    file = PARENT/'HCNetSDK/__init__.py'
    return re.search(r'__version__ = "(.*)"', file.read_text(encoding="utf-8"), re.M)[1]


args, unknown_args = get_args()
sys.argv = [sys.argv[0]] + unknown_args

target_library_dir = PARENT / 'HCNetSDK/Libs'
Path(target_library_dir / 'log').mkdir(parents=True, exist_ok=True)
Path(target_library_dir / 'log/.keep').touch()
if 'win' in args.platform:
    target_library_dir /= 'windows'
    target_library_dir.mkdir(parents=True, exist_ok=True)
    for library_dir in args.library_dirs:
        # 判断HCNetSDKCom文件夹是否存在
        HCNetSDKCom_dir = Path(library_dir, 'HCNetSDKCom')
        if HCNetSDKCom_dir.exists():
            target_com_dir = target_library_dir / 'HCNetSDKCom'
            target_com_dir.mkdir(parents=True, exist_ok=True)
            for dll_file in HCNetSDKCom_dir.glob('*.dll'):
                shutil.copy(dll_file, target_com_dir)
        for dll_file in Path(library_dir).glob('*.dll'):
            shutil.copy(dll_file, target_library_dir)
elif 'linux' in args.platform:
    target_library_dir /= 'linux'
    target_library_dir.mkdir(parents=True, exist_ok=True)
    for library_dir in args.library_dirs:
        HCNetSDKCom_dir = Path(library_dir, 'HCNetSDKCom')
        if HCNetSDKCom_dir.exists():
            target_com_dir = target_library_dir / 'HCNetSDKCom'
            target_com_dir.mkdir(parents=True, exist_ok=True)
            for dll_file in HCNetSDKCom_dir.glob('*.*'):
                shutil.copy(dll_file, target_com_dir)
        for so_file in Path(library_dir).glob('*.*'):
            shutil.copy(so_file, target_library_dir)


setup(
    name='HCNetSDK-python',
    version=get_version(),
    author='laugh12321',
    author_email='laugh12321@vip.qq.com',
    description='HKVISION SDK for Python',
    log_description=README,
    long_description_content_type='text/markdown',
    url='',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
    ],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    keywords='hikvision, sdk, HCNetSDK',
    python_requires='>=3.6',
)


shutil.rmtree(PARENT / 'HCNetSDK_python.egg-info')
shutil.rmtree(PARENT / 'build')
shutil.rmtree(target_library_dir)

platform2whl = {
    'win32': 'win32',
    'win64': 'win_amd64',
    'linux32': 'manylinux1_i686',
    'linux64': 'manylinux1_x86_64',
}

dist_directory = Path(__file__).resolve().parent / 'dist'
whl_filename = f'HCNetSDK_python-{get_version()}-py3-none-{platform2whl[args.platform]}.whl'
target_whl_file = dist_directory / whl_filename
dist_directory.mkdir(exist_ok=True)
shutil.move(dist_directory / f'HCNetSDK_python-{get_version()}-py3-none-any.whl', target_whl_file)