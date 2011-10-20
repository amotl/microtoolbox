#!/usr/bin/env python

# http://alperyilmaz.org/blog/2010/10/16/plot-one-liner-generated-data-with-gnuplot/

import os

DATAFILE = '/tmp/histplot.data'
PLOTFILE = '/tmp/histplot.script'

def history_top(histfile, count_max=20):
    if os.path.exists(DATAFILE):
        os.unlink(DATAFILE)
    #perl -F"\||<\(|;|\`|\\$\(" -alne 'foreach (@F) {{ print $1 if /^.*?(\w+)\\b/i }}' | \
    cmd_tpl = """
        cat {histfile} | \
        grep -v "^#" | \
        perl -F"\||<\(|;|\`|\\$\(" -alne 'foreach (@F) {{ print $1 if /^.*?([\w\/.]+)\\b/i }}' | \
        sort | \
        uniq -c | \
        sort -nr | \
        head -{count_max} | \
        awk '{{print $2"\\t"$1}}' > \
        {DATAFILE}"""
    subs = {}
    subs.update(locals())
    subs.update(globals())
    cmd = cmd_tpl.format(**subs)
    os.system(cmd)

def plot_png(pngfile):

    username = os.environ.get('USER')
    subs = {}
    subs.update(locals())
    subs.update(globals())

    plot_script = """
    # http://stackoverflow.com/questions/1376720/how-do-i-access-various-true-type-fonts-through-gnuplot-with-png-terminal/1426123#1426123
    set terminal png font "/Library/Fonts/Arial.ttf" 11
    #set terminal png font "/Library/Fonts/Andale Mono.ttf" 11
    set term png size 800,600
    set title 'topmost used commands of user "{username}"'
    set boxwidth 0.5
    set style fill solid noborder
    set xtics nomirror rotate by -60
    set format x '-%s'
    plot '{DATAFILE}' using 2:xticlabels(1) with boxes notitle
    """.format(**subs)

    file(PLOTFILE, 'w').write(plot_script)
    #cmd_tpl = "gnuplot -persist {PLOTFILE}"
    cmd_tpl = "gnuplot {PLOTFILE} > {pngfile}"
    cmd = cmd_tpl.format(**subs)
    os.system(cmd)

def main():
    histfile = os.path.join('~', '.bash_history')
    history_top(histfile, count_max=30)
    plot_png('/tmp/histplot.png')

if __name__ == '__main__':
    main()
