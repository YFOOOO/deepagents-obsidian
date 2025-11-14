import { ItemView, WorkspaceLeaf, MarkdownRenderer } from "obsidian";
import type AIAssistantPlugin from "../main";
import { APIClient, QueryResponse } from "../api/client";

export const VIEW_TYPE_AI_ASSISTANT = "ai-assistant-view";

export class AIAssistantView extends ItemView {
	plugin: AIAssistantPlugin;
	apiClient: APIClient;
	private chatContainer: HTMLElement;
	private inputEl: HTMLTextAreaElement;
	private sendButton: HTMLButtonElement;

	constructor(leaf: WorkspaceLeaf, plugin: AIAssistantPlugin) {
		super(leaf);
		this.plugin = plugin;
		this.apiClient = new APIClient(plugin.settings);
	}

	getViewType(): string {
		return VIEW_TYPE_AI_ASSISTANT;
	}

	getDisplayText(): string {
		return "AI Assistant";
	}

	getIcon(): string {
		return "bot";
	}

	async onOpen() {
		const container = this.containerEl.children[1];
		container.empty();
		container.addClass("ai-assistant-view");

		// Title
		const titleEl = container.createEl("div", { cls: "ai-assistant-title" });
		titleEl.createEl("h4", { text: "AI Assistant" });

		// Status indicator
		const statusEl = container.createEl("div", { cls: "ai-assistant-status" });
		this.updateStatus(statusEl);

		// Chat container
		this.chatContainer = container.createEl("div", { cls: "ai-assistant-chat" });

		// Input area
		const inputContainer = container.createEl("div", { cls: "ai-assistant-input" });

		this.inputEl = inputContainer.createEl("textarea", {
			placeholder: "Ask me anything about your notes...",
			cls: "ai-assistant-textarea",
		});

		this.inputEl.addEventListener("keydown", (e) => {
			if (e.key === "Enter" && !e.shiftKey) {
				e.preventDefault();
				this.sendQuery();
			}
		});

		this.sendButton = inputContainer.createEl("button", {
			text: "Send",
			cls: "ai-assistant-send-btn",
		});

		this.sendButton.addEventListener("click", () => {
			this.sendQuery();
		});

		// Welcome message
		this.addMessage("assistant", "Hello! I'm your AI assistant. Ask me anything about your notes or general questions.");
	}

	async onClose() {
		// Cleanup
	}

	private async updateStatus(statusEl: HTMLElement) {
		statusEl.empty();
		const isHealthy = await this.apiClient.healthCheck();

		const indicator = statusEl.createEl("span", {
			cls: isHealthy ? "status-indicator online" : "status-indicator offline",
		});

		statusEl.createEl("span", {
			text: isHealthy ? "Connected" : "Disconnected",
			cls: "status-text",
		});
	}

	private async sendQuery() {
		const query = this.inputEl.value.trim();

		if (!query) {
			return;
		}

		// Clear input
		this.inputEl.value = "";

		// Add user message
		this.addMessage("user", query);

		// Add loading indicator
		const loadingEl = this.addMessage("assistant", "Thinking...");
		loadingEl.addClass("loading");

		try {
			// Send query to backend
			const response = await this.apiClient.query({ query });

			// Remove loading indicator
			loadingEl.remove();

			if (response.error) {
				this.addMessage("error", `Error: ${response.error}`);
				return;
			}

			// Add assistant response
			this.addMessage("assistant", response.answer);

			// Add sources if available
			if (response.sources && response.sources.length > 0) {
				this.addSources(response);
			}

			// Add metadata
			if (response.token_usage) {
				this.addMetadata(response);
			}
		} catch (error) {
			loadingEl.remove();
			this.addMessage("error", `Error: ${error instanceof Error ? error.message : "Unknown error"}`);
		}
	}

	private addMessage(type: "user" | "assistant" | "error", content: string): HTMLElement {
		const messageEl = this.chatContainer.createEl("div", {
			cls: `ai-message ai-message-${type}`,
		});

		const contentEl = messageEl.createEl("div", { cls: "ai-message-content" });

		// Render markdown content
		MarkdownRenderer.renderMarkdown(content, contentEl, "", this);

		// Scroll to bottom
		this.chatContainer.scrollTop = this.chatContainer.scrollHeight;

		return messageEl;
	}

	private addSources(response: QueryResponse) {
		const sourcesEl = this.chatContainer.createEl("div", { cls: "ai-sources" });

		sourcesEl.createEl("div", { text: "Sources:", cls: "ai-sources-title" });

		const sourcesList = sourcesEl.createEl("ul", { cls: "ai-sources-list" });

		response.sources.forEach((source) => {
			const item = sourcesList.createEl("li");

			if (source.path) {
				// Internal link
				const link = item.createEl("a", {
					text: source.title,
					cls: "internal-link",
				});

				link.addEventListener("click", (e) => {
					e.preventDefault();
					this.app.workspace.openLinkText(source.path!, "", false);
				});
			} else if (source.url) {
				// External link
				item.createEl("a", {
					text: source.title,
					href: source.url,
					cls: "external-link",
				});
			} else {
				item.setText(source.title);
			}

			if (source.relevance) {
				item.createEl("span", {
					text: ` (${Math.round(source.relevance * 100)}%)`,
					cls: "ai-source-relevance",
				});
			}
		});
	}

	private addMetadata(response: QueryResponse) {
		const metaEl = this.chatContainer.createEl("div", { cls: "ai-metadata" });

		const items: string[] = [];

		if (response.route_strategy) {
			items.push(`Route: ${response.route_strategy}`);
		}

		if (response.cache_hit) {
			items.push("Cached");
		}

		if (response.token_usage) {
			const { total_tokens, cost } = response.token_usage;
			items.push(`Tokens: ${total_tokens}`);
			if (cost) {
				items.push(`Cost: ¥${cost.toFixed(4)}`);
			}
		}

		metaEl.setText(items.join(" • "));
	}
}
