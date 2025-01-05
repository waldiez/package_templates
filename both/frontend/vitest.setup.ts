import "@testing-library/jest-dom";
import { cleanup } from "@testing-library/react";
import { afterEach, beforeAll, beforeEach, vi } from "vitest";

vi.mock("axios", async importOriginal => {
    const actualAxios = await importOriginal<typeof import("axios")>();
    const mockedAxios = {
        ...actualAxios,
        create: vi.fn(() => {
            const instance = {
                get: vi.fn(),
                post: vi.fn(),
                put: vi.fn(),
                delete: vi.fn(),
                request: vi.fn(),
                interceptors: {
                    request: { use: vi.fn(), eject: vi.fn() },
                    response: {
                        use: vi.fn((_onFulfilled, onRejected) => {
                            instance._onRejected = onRejected; // Capture the rejection handler for testing.
                        }),
                        eject: vi.fn(),
                    },
                },
                defaults: { headers: {} },
                _onRejected: null, // Placeholder for the rejection handler.
            };
            return instance;
        }),
    };
    return {
        ...mockedAxios,
        default: { ...mockedAxios },
    };
});

export const mockMatchMedia = (matches: boolean = false) => {
    // window.matchMedia("(prefers-color-scheme: dark)");
    Object.defineProperty(window, "matchMedia", {
        writable: true,
        value: vi.fn().mockImplementation(query => ({
            matches,
            media: query,
            onchange: null,
            addListener: vi.fn(), // deprecated
            removeListener: vi.fn(), // deprecated
            addEventListener: vi.fn(),
            removeEventListener: vi.fn(),
            dispatchEvent: vi.fn(),
        })),
    });
};

beforeEach(() => {
    vi.useFakeTimers({ shouldAdvanceTime: true });
});
afterEach(() => {
    cleanup();
    vi.useRealTimers();
});
beforeAll(() => {
    mockMatchMedia();
    // window.URL.createObjectURL = vi.fn();
    // window.URL.revokeObjectURL = vi.fn();
});
afterAll(() => {
    vi.resetAllMocks();
});
