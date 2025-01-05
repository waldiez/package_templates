import { act, fireEvent, render, screen, waitFor } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import axiosInstance from "@my/package/api/axiosInstance";
import { Main } from "@my/package/components";

vi.mock("@my/package/api/axiosInstance", () => ({
    default: {
        get: vi.fn(),
    },
}));

const setMockResponse = (response: string) => {
    const responseData = { data: response };
    (axiosInstance.get as ReturnType<typeof vi.fn>).mockResolvedValueOnce(responseData);
};

describe("Main Component", () => {
    afterEach(() => {
        vi.clearAllMocks();
    });
    it("renders correctly", () => {
        const { getByText, getByTestId } = render(<Main />);
        expect(getByText("App")).toBeInTheDocument();
        expect(getByTestId("toggle-theme-button")).toBeInTheDocument();
    });

    it("handles user input correctly", () => {
        const { getByTestId } = render(<Main />);
        const input = getByTestId("user-input");
        fireEvent.change(input, { target: { value: "John" } });
        expect(input).toHaveValue("John");
    });

    it("toggles input visibility", () => {
        const { getByTestId } = render(<Main />);
        const toggleButton = getByTestId("toggle-user-input-visibility-button");

        expect(getByTestId("user-input")).toHaveAttribute("type", "text");

        fireEvent.click(toggleButton);
        expect(getByTestId("user-input")).toHaveAttribute("type", "password");
    });

    it("greets the user", async () => {
        await act(async () => {
            render(<Main />);
        });
        setMockResponse("Hello, Alice!");
        const input = screen.getByTestId("user-input");
        const greetButton = screen.getByTestId("greet-button");
        fireEvent.change(input, { target: { value: "Alice" } });
        fireEvent.click(greetButton);
        await waitFor(() => {
            expect(screen.getByTestId("result")).toHaveTextContent("Hello, Alice!");
        });
    });
    it("toggles theme correctly", () => {
        const { getByTestId } = render(<Main />);
        const toggleButton = getByTestId("toggle-theme-button");
        fireEvent.click(toggleButton);
        expect(document.body.classList.contains("dark-theme")).toBe(true);
    });
    it("submits the input correctly", async () => {
        await act(async () => {
            render(<Main />);
        });
        setMockResponse("Hello, Alice!");
        const input = screen.getByTestId("user-input");
        fireEvent.change(input, { target: { value: "Alice" } });
        const greetButton = screen.getByTestId("greet-button");
        fireEvent.click(greetButton);
        await waitFor(() => {
            expect(screen.getByTestId("result")).toHaveTextContent("Hello, Alice!");
        });
    });
    it("handles Enter key correctly", async () => {
        await act(async () => {
            render(<Main />);
        });
        setMockResponse("Hello, Alice!");
        const input = screen.getByTestId("user-input");
        fireEvent.change(input, { target: { value: "Alice" } });
        fireEvent.keyDown(input, { key: "Enter", code: "Enter" });
        await waitFor(() => {
            expect(screen.getByTestId("result")).toHaveTextContent("Hello, Alice!");
        });
    });
    it("handles Escape key correctly", () => {
        const { getByTestId } = render(<Main />);
        const input = getByTestId("user-input");
        fireEvent.change(input, { target: { value: "Alice" } });
        fireEvent.keyDown(input, { key: "Escape", code: "Escape" });
        expect(input).toHaveValue("");
    });
});
