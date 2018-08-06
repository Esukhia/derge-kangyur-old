function getPageInfo(pageStr) {
	var letter = 'a';
	var indexLetter = pageStr.indexOf('a');
	if (indexLetter == -1) {
		indexLetter = pageStr.indexOf('b');
		letter = 'b';
	}
	if (indexLetter == -1)
		return null;
	var numbers = pageStr.substring(0, indexLetter);
	var imageNum = 2*parseInt(numbers)+1;
	if (letter == 'b')
		imageNum += 1;
	return imageNum;
}

function pad(n, width, z) {
  z = z || '0';
  n = n + '';
  return n.length >= width ? n : new Array(width - n.length + 1).join(z) + n;
}

function getVolInfo(volStr) {
	volId = 'bdr:V22084_I0'.concat(parseInt(volStr)+885);
	return volId;
}

function getImageName(volume, imageNum) {
	var volNum = parseInt(volume)+885;
	var paddedImageNum = pad(''+imageNum, 4, '0');
	return '0'+volNum+paddedImageNum+'.tif';
}

function printimage() {
	var volume = document.getElementById('volume').value;
	var page = document.getElementById('page').value;
	var imageNum = getPageInfo(page);
	var volId = getVolInfo(volume);
	var imageName = getImageName(volume, imageNum);
	var imageUrl = 'http://iiif.bdrc.io/image/v2/'+volId+'::'+imageName+'/full/full/0/default.jpg';
	document.getElementById('theimage').src = imageUrl;
}