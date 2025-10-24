/**
 * Terminal component for user input and log display
 */

import { useState, useRef, useEffect } from 'react'
import type { LogEntry } from '../lib/types'

interface TerminalProps {
  logs: LogEntry[]
  onSubmit: (query: string) => void
  isProcessing: boolean
}

export function Terminal({ logs, onSubmit, isProcessing }: TerminalProps) {
  const [input, setInput] = useState('')
  const scrollRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    // Auto-scroll to bottom
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight
    }
  }, [logs])

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (input.trim() && !isProcessing) {
      onSubmit(input.trim())
      setInput('')
    }
  }

  return (
    <div className="card h-full flex flex-col">
      <div className="mb-4">
        <h2 className="text-xl font-bold text-gray-900">Terminal</h2>
        <p className="text-sm text-gray-500">Type your request below</p>
      </div>

      {/* Log display */}
      <div
        ref={scrollRef}
        className="terminal flex-1 mb-4 max-h-96 overflow-y-auto"
      >
        {logs.length === 0 ? (
          <div className="text-gray-500">
            <p>$ TaskWeave v0.1.0</p>
            <p>$ Ready for input...</p>
            <p className="mt-2 text-green-300">
              Try: "Plan my Stanford CS midterms week"
            </p>
          </div>
        ) : (
          logs.map((log, idx) => (
            <div key={idx} className="terminal-line">
              <span className="text-gray-500">[{log.timestamp}]</span>
              {log.agent && (
                <span className="text-blue-400 ml-2">{log.agent}:</span>
              )}
              <span className="ml-2">{log.message}</span>
            </div>
          ))
        )}
        {isProcessing && (
          <div className="terminal-line text-yellow-400">
            <span className="animate-pulse">Processing...</span>
          </div>
        )}
      </div>

      {/* Input */}
      <form onSubmit={handleSubmit} className="flex space-x-2">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Enter your request..."
          disabled={isProcessing}
          className="input flex-1 font-mono"
          autoFocus
        />
        <button
          type="submit"
          disabled={isProcessing || !input.trim()}
          className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isProcessing ? 'Processing...' : 'Submit'}
        </button>
      </form>
    </div>
  )
}

