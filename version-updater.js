const re = /^version = '(\d\.\d\.\d)'/gm;

function readVersion(contents) {
	const matches = re.exec(contents);
	return matches[1];
}

function writeVersion(contents, version) {
	return contents.replace(re, `version = '${version}'`);
}

module.exports = {
	readVersion,
	writeVersion
};
