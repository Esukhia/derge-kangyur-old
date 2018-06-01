# Digital Derge Kangyur (eKangyur)

Digital Derge Kangyur prepared by Esukhia in 2013 for [84000](http://84000.co/) and [SOAS](https://www.soas.ac.uk/) under the supervision of [TBRC](https://www.tbrc.org/) and [UVA](http://www.virginia.edu/).

## Methodology

This digital version of the Derge Kangyur, or eKangyur as it is called on BDRC, is intended as an exact representation of the Derge Kangyur edition help by the Library of Congress ([available on BDRC](https://www.tbrc.org/#!rid=W4CZ5369)). As an exact representation it preserved the likes of spelling mistakes, carving mistakes, archaic spellings and mistakes caused by wood-block damage.

This digital version isn't a new manual input but rather the result of comparing 4 different previous digital version. This process was chosen in order to minimize the creation of new errors, but of course you might still find some.

For more information on the workflow please refer to:
* [Project Descrition](https://docs.google.com/document/d/17RGGczT9bZl5Hoy7Z6Avo-xympw6eFDeHlecrdVadkM/edit?usp=sharing)
* [Compared-Proofreading Workflow](https://docs.google.com/document/d/1BobLBqSRvyOCissiYx9kCprbJsU5YDFpKf0NzPkX_Aw/edit?usp=sharing)

## Sources

After comparing the various unicode datasets, the team compared the resulting digital kangyur word by word with the [LOC scans](https://www.tbrc.org/#!rid=W4CZ5369) but had to fall back to the [edition printed by the 16th Karmapa](https://www.tbrc.org/#!rid=W22084) for missing pages or unreadable passages. The Karmapa edition wasn't used as the a main source because it was retouched with marker pens before printing in Delhi.

LOC scan:
[![image](https://user-images.githubusercontent.com/17675331/38198418-567be450-36bf-11e8-95d4-f2f7a087878a.png)](https://www.tbrc.org/browser/ImageService?work=W4CZ5369&igroup=I1KG9226&image=901&first=1&last=943&fetchimg=yes)
Karmapa edition:
[![image](https://user-images.githubusercontent.com/17675331/38198496-a61e22f2-36bf-11e8-8750-a40842c34643.png)](https://www.tbrc.org/browser/ImageService?work=W22084&igroup=0987&image=900&first=1&last=944&fetchimg=yes)

## Format

The texts contain the following structural markup at beginning of lines (except the first one):

* **[1b]** is _[Page and folio markers]_
* **[1b.1]** is _[Page and folio markers.line number]_

We follow the page numbers indicated in the original, this means that sometimes the page numbers go back to 1a (ex: vol. 31 after p. 256). Pages numbers that appear twice in a row are indicated with an `x`, example in volume 102: `[355xa]`.

They also contain a few error suggestions noted as example. It is far from an exhausted list of the issues found in the original, the staff was actually discouraged to add these.

* **(X,Y)** is _(potential error, correction suggestion)_ , example: `མཁའ་ལ་(མི་,མེ་)ཏོག་དམར་པོ་`

* **[X]** signals obvious errors or highly suspicious spellings (ex: `མཎྜལ་ཐིག་[ལ་]ལྔ་པ་ལ།`), or un-transcribable characters
* **#** signals an unreadable graphical unit
* **{TX}** signals the beginning of the text with Tohoku catalog number **X**. We use the following conventions:
  * when a text is missing from the Tohoku catalog, we indicate it with the preceding number followed by **a**, ex: **T7**, **T7a**, **T8**
  * when a text has subindexes, we separate them with a dash, ex: **T841-1**, **T841-2**, etc.

The files are UTF16-LE with BOM. `git` doesn't recognize them as text but you can still diff them with the trick exposed [here](https://stackoverflow.com/a/1300928/2560906).

The Unicode is in [NFD](http://unicode.org/reports/tr15/), and oM is rendered as `\u0F68\u0F7C\u0F7E` (`ཨོཾ`) and not `\u0F00` (`ༀ`).

The end of lines sometimes are preceded by a space character (when they end with a shad) so that the result of appending all the lines content is useabletext is correct.

## Volume numbers

Each physical volume is one file. We follow the volume order of the Parphud edition ; in the LoC edition, the main difference is that vol. 102 (of Parphud) is before vol. 100 (of Parphud).

## Completion status

The catalog, volume 103, wasn't digitized as part of this project since it isn't Buddha's words and probably won't be translated by 84,000. Esukhia is hoping to prepare it towards the end of 2018.

## TEI Export

You can find a script in the `scripts/` directory to validate the files and export into a TEI format that can be ingested by BDRC. Other exports should be straightforward taking this script as a template. Note that it exports the volumes in the LoC order.

# Feedback

The files are on Github hoping they'll improve, don't hesitate to signal errors with a pull request!

# How to cite

Use the following statemnent or the [bibtex](https://github.com/Esukhia/derge-kangyur/blob/master/derge-kangyur.bib) file.
    
     ཆོས་ཀྱི་འབྱུང་གནས། [1721–31], བཀའ་འགྱུར་སྡེ་དགེ་པར་མ།, input by Esukhia (2012-2018), https://github.com/Esukhia/derge-kangyur

# TODO
- probable error on vol 3 `[26b.4]` (བ།པ།)
- probable error on vol 57, `[77b.1]` (བྱེ།ད །སྒ)
- spacing error on vol 64, `[247a.7]` (ག།ག)
- spacing error on vol 68, `[14a.3]` (་ཛ་ཀ།ན་མ)
- spacings errors on vol 81, look for `ག།བ`, `ཀ།ཨ`, `ཀ།ས`
- check T533-T541, T663, T664, T674, T675
- vol 89, line [14b.7] : "[ཨོཾ་ཀྡིཾa྅།]"

# License

This work is a mechanical reproduction of a Public Domain work, and as such is also in the Public Domain.
