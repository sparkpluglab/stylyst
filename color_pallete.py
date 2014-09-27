'''
Created on Sep 21, 2014

@author: ranjeetbhatia

http://99designs.com/tech-blog/blog/2012/05/11/color-analysis/
'''

from colorific import palette
from StringIO import StringIO
from urllib2 import urlopen


url = 'http://a9.zassets.com/images/z/2/2/4/3/5/4/2243543-p-MULTIVIEW.jpg'
image_file = StringIO(urlopen(url).read())
p = palette.extract_colors(image_file)
print p
