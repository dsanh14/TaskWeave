/**
 * Basic tests for App component
 */

import { describe, it, expect } from 'vitest'
import { render } from '@testing-library/react'
import App from '../App'

describe('App', () => {
  it('renders without crashing', () => {
    const { container } = render(<App />)
    expect(container).toBeTruthy()
  })

  it('renders TaskWeave header', () => {
    const { getByText } = render(<App />)
    expect(getByText('TaskWeave')).toBeTruthy()
  })

  it('renders terminal component', () => {
    const { getByPlaceholderText } = render(<App />)
    expect(getByPlaceholderText('Enter your request...')).toBeTruthy()
  })
})

