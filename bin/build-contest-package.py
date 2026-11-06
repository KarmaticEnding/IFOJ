"""Build AES-encrypted contest-N.zip containing one unencrypted down.zip."""
import sys, json, os, stat, zipfile
from pathlib import Path
sys.path.insert(0,str(Path.home()/'.local/share/ifoj-contest-packages/python'))
import pyzipper

def main():
    manifest=json.load(sys.stdin)
    password=manifest['password']
    if not password: raise ValueError('Password is required')
    destination=Path(manifest['destination'])
    inner=destination.parent/'down.zip'
    with zipfile.ZipFile(str(inner),'w',compression=zipfile.ZIP_DEFLATED) as archive:
        for item in manifest['files']:
            file=Path(item['source'])
            if not stat.S_ISREG(file.lstat().st_mode) or file.is_symlink(): raise ValueError('Unsupported source file')
            archive.write(str(file),item['name'])
    with pyzipper.AESZipFile(str(destination),'w',compression=pyzipper.ZIP_STORED,encryption=pyzipper.WZ_AES) as outer:
        outer.setpassword(password.encode('utf-8'))
        outer.setencryption(pyzipper.WZ_AES,nbits=256)
        outer.write(str(inner),'down.zip')
    os.chmod(str(destination),0o600)
try:
    main()
except Exception:
    print('Contest archive generation failed.',file=sys.stderr)
    sys.exit(1)
