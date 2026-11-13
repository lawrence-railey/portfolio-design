"""Enable/disable the local hover experiment without reverting other edits."""
from pathlib import Path
import argparse, subprocess, sys

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('state', choices=('on','off'))
args=parser.parse_args()
root=Path(__file__).resolve().parents[1]
flag=root/'content/hover-fx-preview.enabled'
if args.state=='on':
    flag.write_text('Local hover preview enabled.\n',encoding='utf-8')
else:
    flag.unlink(missing_ok=True)
subprocess.run([sys.executable,str(root/'scripts/build.py')],check=True)
print(f'Hover preview {args.state}.')
