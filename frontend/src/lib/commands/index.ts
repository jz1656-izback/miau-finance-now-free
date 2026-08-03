// index.ts — Command handler registry
import { AddLine } from './shared'
import { marketHandlers } from './market'

// All domain handlers combined into one dispatch map
const allHandlers: Record<string, (args: string[], addLine: AddLine) => Promise<void>> = {
  ...marketHandlers,
}

export async function dispatchCommand(
  command: string,
  args: string[],
  addLine: AddLine,
): Promise<boolean> {
  const handler = allHandlers[command]
  if (handler) {
    await handler(args, addLine)
    return true
  }
  return false // not handled — fall through to original switch
}
