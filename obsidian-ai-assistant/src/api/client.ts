import { AIAssistantSettings } from "../settings";

export interface QueryRequest {
	query: string;
	model?: string;
	enable_cache?: boolean;
	enable_smart_routing?: boolean;
	enable_model_adapter?: boolean;
}

export interface QueryResponse {
	answer: string;
	sources: Array<{
		title: string;
		path?: string;
		url?: string;
		relevance: number;
	}>;
	route_strategy?: string;
	token_usage?: {
		prompt_tokens: number;
		completion_tokens: number;
		total_tokens: number;
		cost: number;
	};
	cache_hit?: boolean;
	error?: string;
}

export class APIClient {
	private settings: AIAssistantSettings;

	constructor(settings: AIAssistantSettings) {
		this.settings = settings;
	}

	async query(request: QueryRequest): Promise<QueryResponse> {
		const url = `${this.settings.apiUrl}/query`;

		const headers: Record<string, string> = {
			"Content-Type": "application/json",
		};

		if (this.settings.apiKey) {
			headers["Authorization"] = `Bearer ${this.settings.apiKey}`;
		}

		try {
			const response = await fetch(url, {
				method: "POST",
				headers,
				body: JSON.stringify({
					query: request.query,
					model: request.model || this.settings.model,
					enable_cache: request.enable_cache ?? this.settings.enableCache,
					enable_smart_routing:
						request.enable_smart_routing ?? this.settings.enableSmartRouting,
					enable_model_adapter:
						request.enable_model_adapter ?? this.settings.enableModelAdapter,
				}),
			});

			if (!response.ok) {
				throw new Error(`API request failed: ${response.status} ${response.statusText}`);
			}

			const data = await response.json();
			return data as QueryResponse;
		} catch (error) {
			console.error("API request failed:", error);
			return {
				answer: "",
				sources: [],
				error: error instanceof Error ? error.message : "Unknown error",
			};
		}
	}

	async healthCheck(): Promise<boolean> {
		try {
			const response = await fetch(`${this.settings.apiUrl}/health`);
			return response.ok;
		} catch (error) {
			console.error("Health check failed:", error);
			return false;
		}
	}
}
