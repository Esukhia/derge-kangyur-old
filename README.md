# Digital Derge Kangyur

Welcome to the working repository of the ongoing 2014-2018 Esukhia-Barom proofreading project!

The Digital Derge Kangyur you'll find on our repository is based on the UVA-SOAS 2013 eKangyur and is currently undergoing many changes -- use at your own risk!

## The 2013 UVA-SOAS eKangyur

The UVA-SOAS 2013 eKangyur was created by diff-proofreading the previous UVA input against BDRC's OCRed etexts, ACIP's etexts, and Adharsha's early etexts; in a 2013 project overviewed by [UVA](http://www.virginia.edu/) and funded by [SOAS](https://www.soas.ac.uk/) and [KF](https://khyentsefoundation.org/) (for [84000](http://84000.co/)). This version is currently published on UVA, Adharsha, BDRC, and as part of SOAS's ACTIB corpus.

It was intended as an exact representation of the Derge Kangyur edition help by the Library of Congress ([available on BDRC](https://www.tbrc.org/#!rid=W4CZ5369)). As an exact representation it preserved the likes of spelling mistakes, carving mistakes, archaic spellings and mistakes caused by wood-block damage.

## The Esukhia-Barom revision

The current digital version is an attempt at using linguistics and informatics to improve and normalize the digital Kangyur while preserving the spelling of the Derge woodblocks.

For more information on the workflow please refer to:
* [Project Description](https://docs.google.com/document/d/17RGGczT9bZl5Hoy7Z6Avo-xympw6eFDeHlecrdVadkM/edit?usp=sharing)
* [Compared-Proofreading Workflow](https://docs.google.com/document/d/1BobLBqSRvyOCissiYx9kCprbJsU5YDFpKf0NzPkX_Aw/edit?usp=sharing)

## Image Sources

Each time an issue is found, our team checks the [LOC scans](https://www.tbrc.org/#!rid=W4CZ5369) and sometimes falls back on the [edition printed by the 16th Karmapa](https://www.tbrc.org/#!rid=W22084) in case of missing pages or unreadable passages. The Karmapa edition isn't used as a main source because it was retouched with marker pens before printing in Delhi.

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
  * when a text has subindexes, we separate them with a dash, ex: **T841-1**, **T841-2**, etc. The source of the subindexes are 84000, Adarsha and *The Nyingma Edition of the sDe dGe bKa' 'Gyur and bsTan 'Gyur: Research Catalogue and Bibliography*.

The files are UTF16-LE with BOM. `git` doesn't recognize them as text but you can still diff them with the trick exposed [here](https://stackoverflow.com/a/1300928/2560906).

The Unicode is in [NFD](http://unicode.org/reports/tr15/), and oM is rendered as `\u0F68\u0F7C\u0F7E` (`ཨོཾ`) and not `\u0F00` (`ༀ`).

The end of lines sometimes are preceded by a space character (when they end with a shad) so that the result of appending all the lines content is useabletext is correct.

## Volume numbers

Each physical volume is one file. We follow the volume order of the Parphud edition ; in the LoC edition, the main difference is that vol. 102 (of Parphud) is before vol. 100 (of Parphud).

## Page numbering issues

- vol. 48, page 211 was skipped (both #210 and #211 are written on 210a as ང་ ཉིས་བརྒྱ་ བཅུ་ བཅུ་གཅིག་)
- vol. 77, page 21b, 22a are blank (#22 is written on 22b)
- vol. 77, page 150b, 151a are blank (#151 is written on 151b)
- vol. 77, page 212b, 213a are blank (#213 is written on 213b)
- vol. 86, page 93 is doubled (marked as གོ་གསུམ་གོང་མ་ on 93a/93b and གོ་གསུམ་འོག་མ་ on 93xa/93xb)
- vol. 86, page 261 was skipped (#260 marked as ཉིས་བརྒྱ་དྲུག་ཅུ on 260a and #261 as ཉིས་བརྒྱ་ རེ་གཅིག་ རྒྱུད་འབུམ་ on 260b)
- vol. 90, page 63 was skipped
- vol. 93, page 205 was skipped (#204 marked as ཉིས་བརྒྱ་བཞི་ རྒྱུད་འབུམ་ on 204a and #205 as ཉིས་བརྒྱ་ལྔ་ རྒྱུད་འབུམ་ on 204b)
- vol. 100, page 57 was skipped (#56 marked as ང་དྲུག་ གཟུངས་བསྡུས་ on 56a and #57 as ང་བདུན་ གཟུངས་བསྡུས་ on 56b)

## Completion status

The catalog, volume 103, wasn't digitized as part of this project since it isn't Buddha's words and probably won't be translated by 84,000. Esukhia is hoping to prepare it towards the end of 2018.

## TEI Export

You can find a script in the `scripts/` directory to validate the files and export into a TEI format that can be ingested by BDRC. Other exports should be straightforward taking this script as a template. Note that it exports the volumes in the LoC order.

# Feedback

The files are on Github hoping they'll improve, don't hesitate to signal errors with a pull request!

# How to cite

Use the following statemnent or the [bibtex](https://github.com/Esukhia/derge-kangyur/blob/master/derge-kangyur.bib) file.
    
     ཆོས་ཀྱི་འབྱུང་གནས། [1721–31], བཀའ་འགྱུར་སྡེ་དགེ་པར་མ།, Etexts from UVA, BDRC OCR, ACIP, and Adarsha combined and further proofread by Esukhia, 2012-2018, https://github.com/Esukhia/derge-kangyur

# License

This work is a mechanical reproduction of a Public Domain work, and as such is also in the Public Domain.
