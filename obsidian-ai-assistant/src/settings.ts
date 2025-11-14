export interface AIAssistantSettings {
	apiUrl: string;
	apiKey: string;
	model: string;
	enableCache: boolean;
	enableSmartRouting: boolean;
	enableModelAdapter: boolean;
}

export const DEFAULT_SETTINGS: AIAssistantSettings = {
	apiUrl: "http://localhost:8000",
	apiKey: "",
	model: "qwen-turbo",
	enableCache: true,
	enableSmartRouting: true,
	enableModelAdapter: true,
};
