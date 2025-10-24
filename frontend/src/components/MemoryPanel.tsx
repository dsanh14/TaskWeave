/**
 * Memory panel for viewing and editing user preferences
 */

import { useState, useEffect } from 'react'
import type { MemoryPrefs } from '../lib/types'

interface MemoryPanelProps {
  prefs: MemoryPrefs
  onSave: (prefs: MemoryPrefs) => void
  isSaving: boolean
}

export function MemoryPanel({ prefs, onSave, isSaving }: MemoryPanelProps) {
  const [localPrefs, setLocalPrefs] = useState<MemoryPrefs>(prefs)
  const [hasChanges, setHasChanges] = useState(false)

  useEffect(() => {
    setLocalPrefs(prefs)
    setHasChanges(false)
  }, [prefs])

  const handleChange = (field: keyof MemoryPrefs, value: any) => {
    setLocalPrefs((prev) => ({ ...prev, [field]: value }))
    setHasChanges(true)
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    onSave(localPrefs)
    setHasChanges(false)
  }

  const handleReset = () => {
    setLocalPrefs(prefs)
    setHasChanges(false)
  }

  return (
    <div className="card h-full flex flex-col">
      <div className="mb-4">
        <h2 className="text-xl font-bold text-gray-900">Memory</h2>
        <p className="text-sm text-gray-500">Your preferences and settings</p>
      </div>

      <form onSubmit={handleSubmit} className="flex-1 space-y-4">
        {/* Sleep hours */}
        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Sleep Start
            </label>
            <input
              type="time"
              value={localPrefs.sleep_start}
              onChange={(e) => handleChange('sleep_start', e.target.value)}
              className="input"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">
              Sleep End
            </label>
            <input
              type="time"
              value={localPrefs.sleep_end}
              onChange={(e) => handleChange('sleep_end', e.target.value)}
              className="input"
            />
          </div>
        </div>

        {/* Study blocks */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Study Block Length (minutes)
          </label>
          <input
            type="number"
            min="30"
            max="180"
            step="15"
            value={localPrefs.study_block_minutes}
            onChange={(e) =>
              handleChange('study_block_minutes', parseInt(e.target.value))
            }
            className="input"
          />
          <p className="text-xs text-gray-500 mt-1">
            Recommended: 90 minutes (Pomodoro technique)
          </p>
        </div>

        {/* Break duration */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Break Duration (minutes)
          </label>
          <input
            type="number"
            min="5"
            max="30"
            step="5"
            value={localPrefs.break_minutes}
            onChange={(e) =>
              handleChange('break_minutes', parseInt(e.target.value))
            }
            className="input"
          />
          <p className="text-xs text-gray-500 mt-1">
            Recommended: 15 minutes between study blocks
          </p>
        </div>

        {/* Dietary preferences */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Dietary Preferences
          </label>
          <input
            type="text"
            value={localPrefs.dietary || ''}
            onChange={(e) =>
              handleChange('dietary', e.target.value || null)
            }
            placeholder="e.g., vegetarian, vegan, gluten-free"
            className="input"
          />
          <p className="text-xs text-gray-500 mt-1">
            Optional: Specify any dietary restrictions
          </p>
        </div>

        {/* Actions */}
        <div className="flex space-x-3 pt-4">
          <button
            type="submit"
            disabled={!hasChanges || isSaving}
            className="btn-primary flex-1 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {isSaving ? 'Saving...' : 'Save Preferences'}
          </button>
          <button
            type="button"
            onClick={handleReset}
            disabled={!hasChanges}
            className="btn-secondary disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Reset
          </button>
        </div>
      </form>
    </div>
  )
}

