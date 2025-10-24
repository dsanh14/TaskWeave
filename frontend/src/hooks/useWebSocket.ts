/**
 * WebSocket hook for real-time event streaming
 */

import { useEffect, useRef, useState, useCallback } from 'react'
import type { ServerEvent } from '../lib/types'

const WS_URL =
  import.meta.env.VITE_API_BASE_URL?.replace('http', 'ws') ||
  'ws://localhost:8000'

interface UseWebSocketOptions {
  onEvent?: (event: ServerEvent) => void
  onConnect?: () => void
  onDisconnect?: () => void
  autoReconnect?: boolean
}

export function useWebSocket(options: UseWebSocketOptions = {}) {
  const {
    onEvent,
    onConnect,
    onDisconnect,
    autoReconnect = true,
  } = options

  const [isConnected, setIsConnected] = useState(false)
  const ws = useRef<WebSocket | null>(null)
  const reconnectTimeout = useRef<number>()
  const shouldReconnect = useRef(autoReconnect)

  const connect = useCallback(() => {
    try {
      const socket = new WebSocket(`${WS_URL}/ws/events`)

      socket.onopen = () => {
        console.log('WebSocket connected')
        setIsConnected(true)
        onConnect?.()
      }

      socket.onmessage = (event) => {
        try {
          const serverEvent: ServerEvent = JSON.parse(event.data)
          onEvent?.(serverEvent)
        } catch (error) {
          console.error('Failed to parse WebSocket message:', error)
        }
      }

      socket.onerror = (error) => {
        console.error('WebSocket error:', error)
      }

      socket.onclose = () => {
        console.log('WebSocket disconnected')
        setIsConnected(false)
        onDisconnect?.()

        // Auto-reconnect
        if (shouldReconnect.current) {
          reconnectTimeout.current = window.setTimeout(() => {
            console.log('Reconnecting WebSocket...')
            connect()
          }, 3000)
        }
      }

      ws.current = socket
    } catch (error) {
      console.error('Failed to create WebSocket connection:', error)
    }
  }, [onEvent, onConnect, onDisconnect])

  const disconnect = useCallback(() => {
    shouldReconnect.current = false
    if (reconnectTimeout.current) {
      clearTimeout(reconnectTimeout.current)
    }
    if (ws.current) {
      ws.current.close()
      ws.current = null
    }
  }, [])

  const send = useCallback((data: any) => {
    if (ws.current?.readyState === WebSocket.OPEN) {
      ws.current.send(JSON.stringify(data))
    } else {
      console.warn('WebSocket is not connected')
    }
  }, [])

  useEffect(() => {
    connect()
    return () => {
      disconnect()
    }
  }, [connect, disconnect])

  return {
    isConnected,
    send,
    disconnect,
    reconnect: connect,
  }
}

