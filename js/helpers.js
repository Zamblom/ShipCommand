const toKebabCase = (str) => str.replace(/[A-Z]+(?![a-z])|[A-Z]/g, ($, ofs) => (ofs ? "-" : "") + $.toLowerCase())
const toCamelCase = (str) => str.replace(/-[a-z]/g, ($, ofs) => (ofs ? $[1].toUpperCase() : ""))

const statFromName = (name) => {return document.getElementById("stat-" + toKebabCase(name));}

const currentPlayer = () => {return /(?<=player=)\w+(?![^;])/.exec(document.cookie)[0];};
