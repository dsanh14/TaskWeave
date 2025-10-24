/**
 * Timeline component showing event blocks
 */

import { useState } from 'react'
import type { EventBlock } from '../lib/types'

interface TimelineProps {
  blocks: EventBlock[]
  onApply: (dryRun: boolean) => void
  isApplying: boolean
}

export function Timeline({ blocks, onApply, isApplying }: TimelineProps) {
  const [dryRun, setDryRun] = useState(true)

  const formatTime = (isoString: string) => {
    const date = new Date(isoString)
    return date.toLocaleString('en-US', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    })
  }

  const getBlockColor = (sourceAgent: string) => {
    if (sourceAgent.includes('study')) return 'timeline-block-study'
    if (sourceAgent.includes('meal')) return 'timeline-block-meal'
    if (sourceAgent.includes('calendar')) return 'timeline-block-calendar'
    return 'timeline-block-study'
  }

  // Group blocks by day
  const groupByDay = (blocks: EventBlock[]) => {
    const groups: Record<string, EventBlock[]> = {}
    blocks.forEach((block) => {
      const date = new Date(block.start_iso)
      const day = date.toLocaleDateString('en-US', {
        weekday: 'long',
        month: 'long',
        day: 'numeric',
      })
      if (!groups[day]) groups[day] = []
      groups[day].push(block)
    })
    return groups
  }

  const groupedBlocks = groupByDay(blocks)

  return (
    <div className="card h-full flex flex-col">
      <div className="mb-4 flex items-center justify-between">
        <div>
          <h2 className="text-xl font-bold text-gray-900">Timeline</h2>
          <p className="text-sm text-gray-500">
            {blocks.length} event{blocks.length !== 1 ? 's' : ''}
          </p>
        </div>
        <div className="flex items-center space-x-3">
          <label className="flex items-center space-x-2 text-sm">
            <input
              type="checkbox"
              checked={dryRun}
              onChange={(e) => setDryRun(e.target.checked)}
              className="rounded border-gray-300 text-primary-600 focus:ring-primary-500"
            />
            <span>Dry-run mode</span>
          </label>
          <button
            onClick={() => onApply(dryRun)}
            disabled={isApplying || blocks.length === 0}
            className="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isApplying ? 'Applying...' : 'Apply to Calendar'}
          </button>
        </div>
      </div>

      {/* Timeline display */}
      <div className="flex-1 overflow-y-auto space-y-6">
        {Object.keys(groupedBlocks).length === 0 ? (
          <div className="text-center text-gray-500 py-8">
            <p>No events yet</p>
            <p className="text-sm mt-2">
              Submit a request in the terminal to generate a timeline
            </p>
          </div>
        ) : (
          Object.entries(groupedBlocks).map(([day, dayBlocks]) => (
            <div key={day}>
              <h3 className="font-semibold text-gray-700 mb-3 sticky top-0 bg-white py-1">
                {day}
              </h3>
              <div className="space-y-2">
                {dayBlocks.map((block) => (
                  <div key={block.id} className={getBlockColor(block.source_agent)}>
                    <div className="flex items-start justify-between">
                      <div className="flex-1">
                        <h4 className="font-medium text-gray-900">
                          {block.title}
                        </h4>
                        <p className="text-sm text-gray-600 mt-1">
                          {formatTime(block.start_iso)} →{' '}
                          {formatTime(block.end_iso)}
                        </p>
                      </div>
                      <span className="text-xs text-gray-500 capitalize">
                        {block.source_agent.replace('_', ' ')}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  )
}

