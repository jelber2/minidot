# minidot

A somewhat updated and more portable version of [Thomas Hackl's `minidot`](https://github.com/thackl/minidot). I've dropped the `bash` wrapper in favour of a Pythony one to improve support on Mac and make it a little more straightforward to use. Additionally, I've added a few extra plotting options and updated the R script to use the `PAF` `dv` tag as the sequence identity, which means it works with `minimap2` instead.

### Dependencies

* minimap2 (specify `--mapper path/to/minimap2` if not on your `$PATH`)
* python with pysam
* R-base with ggplot2, stringr, scales, argparse

### Install

    git clone https://github.com/samstudio8/minidot.git

### Usage

    python minidot/minidot.py minidot/minidot.R output.png seq1.fa seq2.fa [seq3.fa ...]

`minidot` will merge all sequences in each `FASTA`, using the first sequence name as the canonical sequence name. You can naively suppress sequences based on their name with `--drop-contains`.
`minimap2` will align every pairing of the new merged FASTAs to construct a PAF, which is then plotted as a diagonal plot by `minidot.R`.

### Maintenance

Patches welcome, but this was a best-effort revival of an older project.
