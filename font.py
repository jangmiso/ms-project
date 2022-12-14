# 1: 한글을 그냥 써보면 박스만 그려짐.
import matplotlib.pyplot as plt
plt.text(0.5, 0.5, ['한글', 'test'])
plt.show()

# 2: 아래와 같이 설정해주면 한글이 잘 동작함.
# ㄴ 시스템에 install이 잘 되어 있다면 mpl.rcParams[] 설정만 하면 되는데, docker에 띄운 jupyter에서는 왠지 apt-get으로 설치한 font를 인식하지 못한다.
import matplotlib as mpl
import matplotlib.font_manager as fm

# 여기서 쓰려는 nanum 폰트를 잘 다운받아서 원하는 디렉토리에 넣어줌.
font_dirs = ['/root/workspace/notebook/nanum_fonts', ]
font_files = fm.findSystemFonts(fontpaths=font_dirs)
font_list = fm.createFontList(font_files)
fm.fontManager.ttflist.extend(font_list)

mpl.rcParams['font.family'] = 'NanumGothicOTF'

""" 나 이렇게 해부럿는데 됏셔~~~~~
font_dirs = ['/home/pi/prj/gui/nanum-gothic', ]
font_files = fm.findSystemFonts(fontpaths=font_dirs)
font_list = fm.createFontList(font_files)
fm.fontManager.ttflist.extend(font_list)

mpl.rcParams['font.family'] = 'NanumGothic'
"""

# 3: 다시 실행해보면 한글이 잘 보여지는걸 확인할 수 있다.
plt.text(0.5, 0.5, ['한글', 'test'])
plt.show()

# etc: 폰트 목록 확인하기.
for font in set( [ (f.name, f.fname) for f in fm.fontManager.ttflist if 'Nanum' in f.name and 'Gothic' in f.name]  ) :
print( font )
