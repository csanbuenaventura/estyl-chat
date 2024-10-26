import api from "./configs/axiosConfig";

export const ChatAPI = {
  sendMessage: async (message: string) => {
    const res = await api.post("http://127.0.0.1:8000/ai", message);
    return res;
  },
};
