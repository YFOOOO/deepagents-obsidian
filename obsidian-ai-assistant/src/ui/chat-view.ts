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
		void this.addMessage("assistant", "Hello! I'm your AI assistant. Ask me anything about your notes or general questions.");
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
		await this.addMessage("user", query);

		// Add loading indicator
		const loadingEl = await this.addMessage("assistant", "Thinking...");
		loadingEl.addClass("loading");

		try {
			// Send query to backend
			const response = await this.apiClient.query({ query });

			// Remove loading indicator
			loadingEl.remove();

			if (response.error) {
				await this.addMessage("error", `Error: ${response.error}`);
				return;
			}

			// Add assistant response
			await this.addMessage("assistant", response.answer);

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
			await this.addMessage("error", `Error: ${error instanceof Error ? error.message : "Unknown error"}`);
		}
	}

	private async addMessage(type: "user" | "assistant" | "error", content: string): Promise<HTMLElement> {
		const messageEl = this.chatContainer.createEl("div", {
			cls: `ai-message ai-message-${type}`,
		});

		const contentEl = messageEl.createEl("div", { cls: "ai-message-content" });

		// Render markdown content with correct sourcePath for internal link resolution
		// Use "/" as vault root to ensure [[path|title]] links work correctly
		await MarkdownRenderer.renderMarkdown(content, contentEl, "/", this);

		// Ensure any [[path|title]] internal links in the original content become clickable
		this.linkifyInternalLinks(contentEl, content);

		// Scroll to bottom
		this.chatContainer.scrollTop = this.chatContainer.scrollHeight;

		return messageEl;
	}

	// Post-process rendered content to make internal [[path|title]] links open correctly
	private linkifyInternalLinks(container: HTMLElement, originalContent: string) {
		const regex = /\[\[([^\]|]+)(?:\|([^\]]+))?\]\]/g;
		let match: RegExpExecArray | null;
		const links: Array<{ path: string; title: string }> = [];
		while ((match = regex.exec(originalContent)) !== null) {
			const p = match[1].trim();
			const disp = (match[2] || match[1]).trim();
			links.push({ path: p.replace(/\.md$/, ""), title: disp });
		}

		if (links.length === 0) return;

		// Collect text nodes under container
		const walker = document.createTreeWalker(container, NodeFilter.SHOW_TEXT, null);
		const textNodes: Text[] = [];
		let node: Node | null;
		while ((node = walker.nextNode()) as Node) {
			textNodes.push(node as Text);
		}

		// For each parsed link, replace the first occurrence of title in the text nodes
		for (const l of links) {
			for (const tnode of textNodes) {
				if (!tnode.nodeValue) continue;
				const idx = tnode.nodeValue.indexOf(l.title);
				if (idx >= 0) {
					const before = tnode.nodeValue.slice(0, idx);
					const after = tnode.nodeValue.slice(idx + l.title.length);
					const parent = tnode.parentNode as Node;
					if (!parent) continue;
					const beforeNode = document.createTextNode(before);
					const linkEl = document.createElement("a");
					linkEl.textContent = l.title;
					linkEl.className = "ai-internal-link";
					linkEl.href = "#";
					linkEl.addEventListener("click", (e) => {
						e.preventDefault();
						this.app.workspace.openLinkText(l.path, "", false);
					});
					const afterNode = document.createTextNode(after);
					parent.insertBefore(beforeNode, tnode);
					parent.insertBefore(linkEl, tnode);
					parent.insertBefore(afterNode, tnode);
					parent.removeChild(tnode);
					break; // go to next parsed link
				}
			}
		}
	}

	private addSources(response: QueryResponse) {
		const sourcesEl = this.chatContainer.createEl("div", { cls: "ai-sources" });

		sourcesEl.createEl("div", { text: "Sources:", cls: "ai-sources-title" });

		const sourcesList = sourcesEl.createEl("ul", { cls: "ai-sources-list" });

		// De-duplicate sources by key (path/url/title) - use stricter key generation
		const seen = new Set<string>();
		response.sources.forEach((source) => {
			// Generate unique key with type prefix to avoid collisions
			const key = source.path ? `internal:${source.path}` : 
			            source.url ? `external:${source.url}` : 
			            `text:${source.title}`;
			if (seen.has(key)) return;
			seen.add(key);

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

			// Only show relevance percent when it's meaningful (not the default 1.0 or 100%)
			if (typeof source.relevance === 'number' && source.relevance > 0 && source.relevance !== 1.0) {
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
