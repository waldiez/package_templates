import { act, renderHook } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import axiosInstance from "@my/package/api/axiosInstance";
import { useMain } from "@my/package/components/Main/useMain";

vi.mock("@my/package/api/axiosInstance", () => ({
    default: {
        get: vi.fn(),
    },
}));

describe("useMain Hook", () => {
    afterEach(() => {
        vi.clearAllMocks();
    });
    it("toggles theme correctly", () => {
        const { result } = renderHook(() => useMain());

        act(() => {
            result.current.toggleTheme();
        });
        expect(result.current.theme).toBe("dark");

        act(() => {
            result.current.toggleTheme();
        });
        expect(result.current.theme).toBe("light");
    });
    it("fetches data correctly", async () => {
        const { result } = renderHook(() => useMain());
        const responseData = { data: "Hello, Alice!" };
        (axiosInstance.get as ReturnType<typeof vi.fn>).mockResolvedValueOnce(responseData);
        result.current.userInput.value = "Alice";
        await act(async () => {
            await result.current.onSubmit();
        });
        expect(result.current.apiResponse).toBe("Hello, Alice!");
    });
    it("should not fetch data if input is empty", async () => {
        const { result } = renderHook(() => useMain());
        result.current.userInput.value = "";
        await act(async () => {
            await result.current.onSubmit();
        });
        expect(result.current.apiResponse).toBe("");
    });
    it("should handle Enter key correctly", async () => {
        const { result } = renderHook(() => useMain());
        const responseData = { data: "Hello, Alice!" };
        (axiosInstance.get as ReturnType<typeof vi.fn>).mockResolvedValueOnce(responseData);
        result.current.userInput.value = "Alice";
        await act(async () => {
            result.current.onKeyDown({ key: "Enter" } as any);
        });
        expect(result.current.apiResponse).toBe("Hello, Alice!");
    });
    it("should handle Escape key correctly", () => {
        const { result } = renderHook(() => useMain());
        result.current.userInput.value = "Alice";
        act(() => {
            result.current.onKeyDown({ key: "Escape" } as any);
        });
        expect(result.current.userInput.value).toBe("");
        expect(result.current.apiResponse).toBe("");
    });
});
