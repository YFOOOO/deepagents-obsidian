# Obsidian AI Assistant Plugin - Copilot Instructions

## Project Overview
Creating an Obsidian plugin (TypeScript) that integrates with existing Python backend (DeepAgents-based AI assistant).

## Architecture
- **Frontend**: TypeScript Obsidian plugin (runs in Electron/Obsidian)
- **Backend**: Python API service (existing obsidian_assistant module)
- **Communication**: HTTP REST API

## Project Setup Checklist
- [x] Create .github directory and instructions
- [ ] Get TypeScript project setup info
- [ ] Create plugin folder structure
- [ ] Create manifest.json
- [ ] Create package.json with dependencies
- [ ] Create tsconfig.json
- [ ] Create main.ts (plugin entry)
- [ ] Create settings.ts (settings panel)
- [ ] Create api-client.ts (backend communication)
- [ ] Create chat-view.ts (UI component)
- [ ] Configure build tools (esbuild)
- [ ] Create README.md
- [ ] Install dependencies
- [ ] Build plugin
- [ ] Test in Obsidian

## Key Requirements
1. TypeScript plugin compatible with Obsidian API
2. Settings tab for Python backend URL and API key
3. Chat interface for user queries
4. Display results with Obsidian internal links `[[path|name]]`
5. Show sources and citations
6. Handle errors gracefully

## File Structure
```
obsidian-ai-assistant/
├── manifest.json
├── package.json
├── tsconfig.json
├── .eslintrc.json
├── .prettierrc
├── esbuild.config.mjs
├── src/
│   ├── main.ts
│   ├── settings.ts
│   ├── api/
│   │   └── client.ts
│   └── ui/
│       ├── chat-view.ts
│       └── search-modal.ts
├── styles.css
└── README.md
```
