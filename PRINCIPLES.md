# Engineering Principles

These are general principles that must be followed in the repo. If deviations would surface, escalate.

1. **Simplicity**: Prefer simple, straightforward solutions. Avoid unnecessary complexity, abstractions, layers and patterns. Write the minimum code that solves the problem — if you write 200 lines and it could be 50, rewrite it. Gut-check: would a senior engineer call this overcomplicated?
2. **Surgical changes**: Touch only what you must. When editing existing code, don't "improve" adjacent code, comments, or formatting, and don't refactor things that aren't broken. Match the existing style even if you'd do it differently. If you notice unrelated dead code, mention it — don't delete it. Clean up only your own mess: remove imports, variables, and functions that your changes made unused, but never remove pre-existing dead code unless asked. Every changed line should trace directly to the request.
3. **Minimal dependencies**: Justify each dependency by clear value. Prefer the standard library or a small amount of code over pulling in a package.
4. **YAGNI**: Don't add functionality until it's actually needed.
5. **SLAP**: Each function should operate at a single level of abstraction.
6. **Stepdown rule**: Order code top-down so each function is followed by the lower-level functions it calls. Read like prose, from high-level intent down to details.
