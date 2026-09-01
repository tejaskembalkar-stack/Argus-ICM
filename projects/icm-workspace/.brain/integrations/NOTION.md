# Notion Integration

Notion is optional and queried only when a task needs product or business context.

Required local variables (never commit values):

- `NOTION_TOKEN`
- `NOTION_ROOT_PAGE_ID` or a task-specific database/page ID

Grant the integration access only to required pages. Query narrow properties and page blocks; do not import an entire workspace. Before writes, confirm the page/database ID and payload. After writes, fetch the exact page/record and verify changed properties. Never print the token or copy it into agent context.
