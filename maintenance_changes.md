## Stablize useCompatibility.ts
- compute `selectedPayload` in App.ts instead.
- Make effect depend on i`isLoading` and `mode`

## Split App by responsibility
- Move selection/search state into a dedicated hook (usePartSelection)
- Keep request in useAI and useCompatibility
- Move more UI behavior that belongs to Selections to its own.

## Replace any with explicit types
- AI output props
- useAI.ts
- types.ts
    - SelectedPayload
    - StreamMsg
    - Option

## Reduce prop drilling
- Selections
- AutoComplete

## Clean encoding issues and shared strings


# next step: Break App into smaller responsibilities
# Fix frontend functionalities