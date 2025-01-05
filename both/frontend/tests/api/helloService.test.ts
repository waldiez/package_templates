import { describe, expect, it, vi } from "vitest";

import axiosInstance from "@my/package/api/axiosInstance";
import { helloService } from "@my/package/api/helloService";

vi.mock("@my/package/api/axiosInstance", () => ({
    default: {
        get: vi.fn(), // we only need to mock the get method, update this if needed
    },
}));

describe("helloService", () => {
    afterEach(() => {
        vi.clearAllMocks();
    });
    it("should call axiosInstance.get with the correct URL", async () => {
        const name = "Alice";
        const responseData = { data: `Hello, ${name}!` };
        (axiosInstance.get as ReturnType<typeof vi.fn>).mockResolvedValueOnce(responseData);
        await helloService.getHello(name);
        expect(axiosInstance.get).toHaveBeenCalledWith("/hello?name=Alice");
    });
    it("should return the response data", async () => {
        const name = "Alice";
        const responseData = { data: `Hello, ${name}!` };
        (axiosInstance.get as ReturnType<typeof vi.fn>).mockResolvedValueOnce(responseData);
        const result = await helloService.getHello(name);
        expect(result).toBe(`Hello, ${name}!`);
    });
});
