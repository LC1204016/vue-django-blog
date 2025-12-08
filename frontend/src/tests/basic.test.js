// 简单的测试示例
import { describe, it, expect } from 'vitest'

describe('基本测试', () => {
  it('应该通过简单的数学测试', () => {
    expect(2 + 2).toBe(4)
  })
  
  it('应该通过字符串测试', () => {
    expect('hello').toBe('hello')
  })
})