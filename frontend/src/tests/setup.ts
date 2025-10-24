/**
 * Test setup file
 */

import '@testing-library/jest-dom'

// Mock WebSocket
global.WebSocket = class WebSocket {
  onopen: any
  onclose: any
  onmessage: any
  onerror: any
  readyState = 1

  constructor(url: string) {
    setTimeout(() => {
      if (this.onopen) this.onopen({})
    }, 0)
  }

  send() {}
  close() {
    if (this.onclose) this.onclose({})
  }
} as any

