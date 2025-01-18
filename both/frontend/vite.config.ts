import react from "@vitejs/plugin-react";
import dotenv from "dotenv";
import fs from "fs-extra";
import path from "path";
import { relative, resolve } from "path";
import { fileURLToPath } from "url";
import { defineConfig } from "vite";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const coverageInclude = relative(process.cwd(), resolve(__dirname, "src")).replace(/\\/g, "/");
const coverageDir = relative(process.cwd(), resolve(__dirname, "..", "coverage", "frontend")).replace(
    /\\/g,
    "/",
);
let relativePath = relative(process.cwd(), resolve(__dirname)).replace(/\\/g, "/");
if (!relativePath.endsWith("/")) {
    relativePath += "/";
}
if (relativePath.startsWith("/")) {
    relativePath = relativePath.substring(1);
}
const testsInclude = `${relativePath}tests/**/*.test.{ts,tsx}`;

dotenv.config();

const thresholdLimit = 50;
const thresholds = {
    statements: thresholdLimit,
    branches: thresholdLimit,
    functions: thresholdLimit,
    lines: thresholdLimit,
};

// https://vitejs.dev/config/
export default defineConfig(({ command }) => {
    const envFile = resolve(__dirname, "..", ".env");
    if (fs.existsSync(envFile)) {
        const envConfig = dotenv.parse(fs.readFileSync(envFile));
        process.env = { ...process.env, ...envConfig };
    }
    let apiDevPortStr = process.env["MY_PACKAGE_PORT"] || "8000";
    let apiDevPort = 8000;
    try {
        apiDevPort = parseInt(apiDevPortStr, 10);
    } catch (error) {
        console.error(error);
    }
    if ([80, 443].includes(apiDevPort)) {
        apiDevPortStr = "";
    } else {
        apiDevPortStr = `:${apiDevPortStr}`;
    }
    const apiDevHost = process.env["MY_PACKAGE_BASE_HOST"] || "localhost";
    const apiDevScheme = ["localhost", "0.0.0.0", "127.0.0.1"].includes(apiDevHost) ? "http" : "https";
    let base = command === "build" ? process.env["MY_PACKAGE_BASE_URL"] || "/static/" : "/";
    if (!base.endsWith("/")) {
        base += "/";
    }
    const publicDir = resolve(__dirname, "..", "public");
    command === "build";
    // const apiDewsScheme = apiDevScheme.replace("http", "ws");
    return {
        publicDir,
        base,
        server: {
            proxy: {
                "/api": {
                    target: `${apiDevScheme}://${apiDevHost}${apiDevPortStr}`,
                    changeOrigin: true,
                },
                // "/ws": {
                //     target: `${apiDewsScheme}://${apiDevHost}${apiDevPortStr}`,
                //     rewriteWsOrigin: true,
                //     ws: true,
                // },
            },
        },
        build: {
            emptyOutDir: true,
            minify: "terser",
            outDir: resolve(__dirname, "..", "my_package", "static"),
            rollupOptions: {
                output: {
                    manualChunks: {
                        react: ["react"],
                        "react-dom": ["react-dom"],
                    },
                },
            },
        },
        plugins: [react()],
        resolve: {
            alias: {
                "@my/package": resolve(__dirname, "src"),
            },
        },
        test: {
            include: [testsInclude],
            // support `describe`, `test` etc. globally,
            globals: true,
            // pool: 'vmThreads',
            // isolate: false,
            bail: 1,
            // run tests in jsdom environment
            environment: "jsdom",
            coverage: {
                provider: "v8",
                reporter: ["lcov", "text", "text-summary", "html"],
                include: [coverageInclude],
                reportsDirectory: coverageDir,
                exclude: [],
                ignoreEmptyLines: true,
                thresholds,
                all: true,
            },
            // global test setup
            setupFiles: [resolve(__dirname, "vitest.setup.ts")],
        },
    };
});
