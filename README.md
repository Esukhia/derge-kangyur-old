# Digital Derge Kangyur (eKangyur)

Digital Derge Kangyur prepared by Esukhia in 2013 for [84000](http://84000.co/) and [SOAS](https://www.soas.ac.uk/) under the supervision of [TBRC](https://www.tbrc.org/) and [UVA](http://www.virginia.edu/).

## Methodology
This digital version of the Derge Kangyur, or eKangyur as it is called on tbrc.org, is intended as an exact representation of the Derge Kangyur edition help by the Library of Congress ([available on BDRC](https://www.tbrc.org/#!rid=W4CZ5369)). As an exact representation it preserved the likes of spelling mistakes, carving mistakes, archaic spellings and mistakes caused by wood-block damage.

This digital version isn't a new manual input but rather the result of comparing 4 different previous digital version. This process was chosen in order to minimize the creation of new errors, but of course you might still find some.

For more information on the workflow please refer to:
* [Project Descrition](https://docs.google.com/document/d/17RGGczT9bZl5Hoy7Z6Avo-xympw6eFDeHlecrdVadkM/edit?usp=sharing)
* [Compared-Proofreading Workflow](https://docs.google.com/document/d/1BobLBqSRvyOCissiYx9kCprbJsU5YDFpKf0NzPkX_Aw/edit?usp=sharing)

## Format

The texts contain the following structural markup at beginning of lines (except the first one):

* **[1b]** is _[Page and folio markers]_
* **[1b.1]** is _[Page and folio markers.line number]_

They also contain a few error suggestions noted as example. It is far from an exhausted list of the issues found in the original, the staff was actually discouraged to add these.

* **(X,Y)** is _(potential error, correction suggestion)_ , example: `མཁའ་ལ་(མི་,མེ་)ཏོག་དམར་པོ་`

* **[X]** signals obvious errors or highly suspicious spellings (ex: `མཎྜལ་ཐིག་[ལ་]ལྔ་པ་ལ།`), or un-transcribable characters
* **#** signals an unreadable graphical unit

The Unicode is in [NFD](http://unicode.org/reports/tr15/), and oM is rendered as `\u0F68\u0F7C\u0F7E` (`ཨོཾ`) and not `\u0F00` (`ༀ`).

## Technical details

The files are UTF16-LE with BOM. `git` doesn't recognize them as text but you can still diff them with the trick exposed [here](https://stackoverflow.com/a/1300928/2560906).

# Feedback

The files are on Github hoping they'll improve, don't hesitate to signal errors with a pull request!

# License

This work is a mechanical reproduction of a Public Domain work, and as such is also in the Public Domain.
