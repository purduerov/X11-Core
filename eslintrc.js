module.exports = {
    "extends": "airbnb",
    "rules":{
        "linebreak-style": 0,   // Ignore issues, git should be set up to fix upon pushing to the repo
        "indent": ["error", 4],
        "react/jsx-indent": ["error", 4],
        "no-var": 0,     // We lean on global-scoped variables for some files (electron-setup.js), fix later
        "object-curly-newline": 0,
        "no-plusplus": 0,
        "react/jsx-indent-props": ["error", 4],
        "react/destructuring-assignment": ["enabled", "never"],
        "react/jsx-one-expression-per-line": 0,
    }
};