/** Run tests in the project's subdirectories. */
import path from "path";
import fs from "fs-extra";

import { packageJson, rootDir, runCommandInDir, getPackageManager } from "./_lib";

const runTests = () => {
    for (const project of packageJson.packages.ts) {
        const projectDir = path.join(rootDir, project);
        const packageJsonPath = path.join(projectDir, "package.json");
        if (fs.existsSync(packageJsonPath)) {
            const packageManager = getPackageManager(projectDir);
            runCommandInDir(projectDir, packageManager, ["run", "test"]);
        } else {
            console.log(`No package.json in ${projectDir} skipping ...`);
        }
    }
};

runTests();
