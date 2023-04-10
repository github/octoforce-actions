const core = require("@actions/core");
const github = require("@actions/github");

(function start() {
  try {
    const issuePrefix = process.env?.ISSUE_PREFIX;
    let ref = process.env?.BRANCH_NAME;
    if (!ref) {
      ref = github.context.ref;
    }
    const branchName = ref.substring(ref.lastIndexOf("/") + 1);
    console.log(`branchName = ${branchName}`);
    core.setOutput("branchName", branchName);
    const re = new RegExp("^" + issuePrefix + "(\\d+)");
    const prefixMatches = branchName.match(re);
    let matches = "false";
    let issueNumber = "";
    if (prefixMatches) {
      matches = "true";
      issueNumber = prefixMatches[1];
    }
    core.setOutput("matches", matches);
    core.setOutput("issueNumber", issueNumber);
    console.log(`matches = ${matches}; issueNumber = ${issueNumber}`);
  } catch (e) {
    core.setFailed(e.message);
  }
})();
