# minidot

A somewhat updated and more portable version of [Thomas Hackl's `minidot`](https://github.com/thackl/minidot). I've dropped the `bash` wrapper in favour of a Pythony one to improve support on Mac and make it a little more straightforward to use. Additionally, I've added a few extra plotting options and updated the R script to use the `PAF` `dv` tag as the sequence identity, which means it works with `minimap2` instead.

### Dependencies

* minimap2
* R-base with ggplot2, stringr, scales, argparse

### Install

    git clone https://github.com/samstudio8/minidot.git

### Usage

    python minidot.py ./minidot.R output.png seq1.fa seq2.fa

### Maintenance

Patches welcome, but this was a best-effort revival of an older project.
