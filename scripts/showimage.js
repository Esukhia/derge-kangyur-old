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
	volId22 = 'bdr:V22084_I0'.concat(parseInt(volStr)+885);
	volId4C = 'bdr:V4CZ5369_I1KG9'.concat(parseInt(volStr)+126);
	volId30 = 'bdr:V30532_I6'.concat(parseInt(volStr)+347);
	return [volId4C, volId22, volId30];
}

function getImageName(volume, imageNum) {
	res = [];
	var volInt = parseInt(volume);
	var paddedImageNum = pad(''+imageNum, 4, '0');
	var	volNum = volInt+126;
	res[0] = 'I1KG9'+volNum+paddedImageNum+'.jpg';
	volNum = volInt+885;
	res[1] = '0'+volNum+paddedImageNum+'.tif';
	volNum = volInt+347;
	res[2] = '6'+volNum+paddedImageNum+'.tif';
	return res;
}

function printimage() {
	var volume = document.getElementById('volume').value;
	var page = document.getElementById('page').value;
	var imageNum = getPageInfo(page);
	if (imageNum == null) {
		return;
	}
	var volIds = getVolInfo(volume);
	var imageNames = getImageName(volume, imageNum);
	for (var i = 0 ; i < 3 ; i++) {
		var imageUrl = 'http://iiif.bdrc.io/image/v2/'+volIds[i]+'::'+imageNames[i]+'/full/full/0/default.jpg';
		document.getElementById('theimage'+(i+1)).src = imageUrl;
	}
}