const vscode = require('vscode');

function hello() {
    vscode.window.showInformationMessage('cp/hello');
}

async function activate(context) {
    vscode.window.showInformationMessage('cp/activate');
    context.subscriptions.push(
        vscode.commands.registerCommand('dponyatov.cp.hello', hello)
    );
}

function deactivate() {
    vscode.window.showInformationMessage('cp/deactivate');
}

module.exports = {
    activate,
    deactivate,
    hello,
};
