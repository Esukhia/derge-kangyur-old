# This script "fixes" the files by:
# - not using deprecated unicode characters
# - converting to NFD (Tibetan composed forms are not preferred)
# - adding tshegs between ང and ། (maybe this should also include vowels)
# - converting unbreakable tshegs into normal tshegs

#sed -i 's/ང།/ང་།/g;s/༌/་/g;s/ཱྀ/ཱྀ/g;s/ཱུ/ཱུ/g;s/ༀ/ཨོཾ/g;s/  +/ /g;s/་་+/་/g;s/།་/།/g;s/་ /་/g;s/། ་/། /g;s/ ་/་/g' derge-kangyur-tags/*
for f in derge-kangyur-tags/*.txt ; do
	cat "$f" | sed 's/ང།/ང་།/g;s/༌/་/g;s/ཱྀ/ཱྀ/g;s/ཱུ/ཱུ/g;s/ༀ/ཨོཾ/g;s/  +/ /g;s/་་+/་/g;s/།་/།/g;s/་ /་/g;s/། ་/། /g;' | uconv -f UTF-8 -x Any-NFKD -t UTF-8 | sponge "$f"
done
