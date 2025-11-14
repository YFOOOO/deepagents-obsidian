import { App, Plugin, PluginSettingTab, Setting, WorkspaceLeaf } from "obsidian";
import { AIAssistantView, VIEW_TYPE_AI_ASSISTANT } from "./ui/chat-view";
import { AIAssistantSettings, DEFAULT_SETTINGS } from "./settings";

export default class AIAssistantPlugin extends Plugin {
	settings: AIAssistantSettings;

	async onload() {
		await this.loadSettings();

		// Register the chat view
		this.registerView(VIEW_TYPE_AI_ASSISTANT, (leaf) => new AIAssistantView(leaf, this));

		// Add ribbon icon
		this.addRibbonIcon("bot", "AI Assistant", () => {
			this.activateView();
		});

		// Add command to open AI Assistant
		this.addCommand({
			id: "open-ai-assistant",
			name: "Open AI Assistant",
			callback: () => {
				this.activateView();
			},
		});

		// Add settings tab
		this.addSettingTab(new AIAssistantSettingTab(this.app, this));

		console.log("AI Assistant plugin loaded");
	}

	onunload() {
		console.log("AI Assistant plugin unloaded");
	}

	async loadSettings() {
		this.settings = Object.assign({}, DEFAULT_SETTINGS, await this.loadData());
	}

	async saveSettings() {
		await this.saveData(this.settings);
	}

	async activateView() {
		const { workspace } = this.app;

		let leaf: WorkspaceLeaf | null = null;
		const leaves = workspace.getLeavesOfType(VIEW_TYPE_AI_ASSISTANT);

		if (leaves.length > 0) {
			// View already exists, reveal it
			leaf = leaves[0];
		} else {
			// Create new leaf in right sidebar
			leaf = workspace.getRightLeaf(false);
			if (leaf) {
				await leaf.setViewState({
					type: VIEW_TYPE_AI_ASSISTANT,
					active: true,
				});
			}
		}

		if (leaf) {
			workspace.revealLeaf(leaf);
		}
	}
}

class AIAssistantSettingTab extends PluginSettingTab {
	plugin: AIAssistantPlugin;

	constructor(app: App, plugin: AIAssistantPlugin) {
		super(app, plugin);
		this.plugin = plugin;
	}

	display(): void {
		const { containerEl } = this;

		containerEl.empty();

		containerEl.createEl("h2", { text: "AI Assistant Settings" });

		new Setting(containerEl)
			.setName("Backend API URL")
			.setDesc("URL of your Python backend API (e.g., http://localhost:8000)")
			.addText((text) =>
				text
					.setPlaceholder("http://localhost:8000")
					.setValue(this.plugin.settings.apiUrl)
					.onChange(async (value) => {
						this.plugin.settings.apiUrl = value;
						await this.plugin.saveSettings();
					})
			);

		new Setting(containerEl)
			.setName("API Key")
			.setDesc("Optional API key for authentication")
			.addText((text) =>
				text
					.setPlaceholder("Enter API key")
					.setValue(this.plugin.settings.apiKey)
					.onChange(async (value) => {
						this.plugin.settings.apiKey = value;
						await this.plugin.saveSettings();
					})
			);

		new Setting(containerEl)
			.setName("Model")
			.setDesc("AI model to use (e.g., qwen-turbo, qwen-plus)")
			.addText((text) =>
				text
					.setPlaceholder("qwen-turbo")
					.setValue(this.plugin.settings.model)
					.onChange(async (value) => {
						this.plugin.settings.model = value;
						await this.plugin.saveSettings();
					})
			);

		new Setting(containerEl)
			.setName("Enable Caching")
			.setDesc("Cache responses to reduce API calls")
			.addToggle((toggle) =>
				toggle.setValue(this.plugin.settings.enableCache).onChange(async (value) => {
					this.plugin.settings.enableCache = value;
					await this.plugin.saveSettings();
				})
			);

		new Setting(containerEl)
			.setName("Enable Smart Routing")
			.setDesc("Automatically choose between local and web search")
			.addToggle((toggle) =>
				toggle
					.setValue(this.plugin.settings.enableSmartRouting)
					.onChange(async (value) => {
						this.plugin.settings.enableSmartRouting = value;
						await this.plugin.saveSettings();
					})
			);
	}
}
