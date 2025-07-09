import { describe, it, expect } from 'vitest';

describe('Basic Test', () => {
  it('should run basic math operations', () => {
    expect(2 + 2).toBe(4);
    expect(3 * 3).toBe(9);
  });

  it('should handle string operations', () => {
    expect('hello'.toUpperCase()).toBe('HELLO');
    expect('world'.length).toBe(5);
  });

  it('should handle arrays', () => {
    const arr = [1, 2, 3];
    expect(arr).toHaveLength(3);
    expect(arr).toContain(2);
  });
});
