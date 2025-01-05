import axiosInstance from "@my/package/api/axiosInstance";

export const helloService = {
    async getHello(name: string): Promise<string> {
        const query = new URLSearchParams({ name });
        const response = await axiosInstance.get<string>(`/hello?${query}`);
        return response.data;
    },
};
