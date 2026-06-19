#!/usr/bin/env node
// Загрузчик MCP-сервера Bukvarix: читает .env из корня проекта (рядом с этим файлом),
// прокидывает переменные в окружение и запускает сам сервер. Ключ живёт только в .env
// (он в .gitignore) — в репозитории секретов нет.
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

const here = dirname(fileURLToPath(import.meta.url));

// .env: строки KEY=VALUE, # — комментарии. Существующие env-переменные не перезатираем.
try {
  const env = readFileSync(join(here, ".env"), "utf8");
  for (const line of env.split(/\r?\n/)) {
    const m = /^\s*([\w.-]+)\s*=\s*(.*)\s*$/.exec(line);
    if (!m || line.trim().startsWith("#")) continue;
    let [, key, val] = m;
    val = val.replace(/^["']|["']$/g, ""); // снять кавычки, если есть
    if (process.env[key] === undefined) process.env[key] = val;
  }
} catch {
  // нет .env — сервер сам подставит ключ "free" по умолчанию
}

// Путь к собранному серверу. Переопределяется через BUKVARIX_MCP_DIST в .env при необходимости.
const dist =
  process.env.BUKVARIX_MCP_DIST ||
  "C:/Users/ilya-/bukvarix-mcp-server/dist/index.js";
await import(`file://${dist}`);
