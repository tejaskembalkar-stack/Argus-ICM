# Windows CMD Shims

When Python launches `.cmd` or `.bat` tools such as `npx`, resolve the executable with `shutil.which()` and use shell mode only for the shim case.

This avoids Windows `FileNotFoundError` during local tool execution.
