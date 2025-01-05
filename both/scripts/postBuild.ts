/* St*/
import fs from "fs-extra";
import path from "path";
import url from "url";

const __filename = url.fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const __rootDir = path.resolve(__dirname, "..");
const __dotLocal = path.resolve(__rootDir, ".local");

const main = () => {
    const buildDt = new Date().toISOString();
    if (!fs.existsSync(__dotLocal)) {
        fs.mkdirSync(__dotLocal, { recursive: true });
    }
    const dstPath = path.resolve(__dotLocal, "last-build.txt");
    if (fs.existsSync(dstPath)) {
        fs.unlinkSync(dstPath);
    }
    fs.writeFileSync(dstPath, buildDt);
};

main();
