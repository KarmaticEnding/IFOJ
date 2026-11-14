"""Official tuack renderer with automatic fitting of cover filename cells.

Run from the contest root:
    python3 day1/subsequence/tools/render_noi.py noi -s
Only the renderer's temporary copy of the cover is adapted. The installed tuack
package, problem statements, configuration and actual filenames are unchanged.
"""
from pathlib import Path
import hashlib,json,re
import tuack.ren as ren

original_before=ren.Base.before
original_path=Path(ren.base.path)/'templates/tuoi.tex.jinja'
original_hash=hashlib.sha256(original_path.read_bytes()).hexdigest()
adaptations=[]

def before_with_fitted_cover(self):
 original_before(self)
 if self.comp not in ('noi','tuoi'):return
 path=Path(ren.tmp_path)/'tuoi.tex.jinja'
 source=path.read_text()
 definition=r'''{% raw %}
\newsavebox{\CoverFilenameBox}
\newcommand{\CoverFilename}[1]{%
  \sbox{\CoverFilenameBox}{\ttfamily #1}%
  \ifdim\wd\CoverFilenameBox>\linewidth
    \resizebox{\linewidth}{!}{\usebox{\CoverFilenameBox}}%
  \else
    \usebox{\CoverFilenameBox}%
  \fi
}
{% endraw %}
'''
 marker='{% block cover %}'
 assert source.count(marker)==1
 source=source.replace(marker,marker+'\n'+definition,1)
 pattern=r"\{\\ttfamily\s+(\{\{\s*prob\['name'\].*?\}\}[^{}]*)\}"
 source,count=re.subn(pattern,lambda m:r'\CoverFilename{ '+m.group(1)+'}',source)
 assert count>=8,count
 path.write_text(source)
 adaptations.append({'temporary_cover_cells_adapted':count,'official_template_sha256':original_hash})

if __name__=='__main__':
 ren.Base.before=before_with_fitted_cover
 try:
  assert ren.base.init(),'Use: python3 tools/render_noi.py noi -s'
  ren.base.check_install('jinja2')
  for ren.base.work in ren.base.works:
   for ren.base.lang in ren.base.langs:
    ren.class_list[ren.base.work](ren.comp_list[ren.base.work]).run()
 finally:
  ren.Base.before=original_before
  assert hashlib.sha256(original_path.read_bytes()).hexdigest()==original_hash
 (Path(__file__).resolve().parent/'cover-render-audit.json').write_text(json.dumps({'official_package_unchanged':True,'adaptations':adaptations},indent=2))
