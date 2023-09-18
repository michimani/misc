import { expect, describe, test } from 'bun:test'
import { add } from './Math'

describe('test for Math.add', () => {
  type Case = {
    name: string
    a: number
    b: number
    expected: number
  }

  const cases: Case[] = [
    {
      name: '1 + 1 = 2',
      a: 1,
      b: 1,
      expected: 2
    },
    {
      name: '1 + 2 = 3',
      a: 1,
      b: 2,
      expected: 3
    },
    {
      name: '2 + -3 = -1',
      a: 2,
      b: -3,
      expected: -1
    }
  ]

  cases.forEach((c) => {
    test(c.name, () => {
      expect(add(c.a, c.b)).toBe(c.expected)
    })
  })
})
