const re = /version = '(\d\.\d\.\d)'/;

const updater = {
  readVersion: (contents) => contents.match(re)[1],
  writeVersion: (contents, version) => contents.replace(re, `version = '${version}'`)
};

const tracker = {
  filename: "./setup.py",
  updater
}

module.exports = {
  types: [
    {"type": "feat", "section": "Features"},
    {"type": "fix", "section": "Bug Fixes"},
    {"type": "chore", "section": "Misc"},
    {"type": "docs", "section": "Misc"},
    {"type": "style", "section": "Misc"},
    {"type": "refactor", "section": "Misc"},
    {"type": "perf", "section": "Misc"},
    {"type": "test", "section": "Misc"},
    {"type": "ci", "section": "Misc"}
  ],
  // read version
  packageFiles: [tracker],
  // write version
  bumpFiles: [tracker]
};
