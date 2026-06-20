import axios from 'axios'

export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api'
export const WS_URL = import.meta.env.VITE_WS_URL || 'ws://127.0.0.1:8000/ws/events'

const http = axios.create({
  baseURL: API_BASE_URL,
  timeout: 3000
})

export async function safeGet(url, fallback) {
  try {
    const { data } = await http.get(url)
    return data
  } catch (error) {
    console.warn(`[NightSight] ${url} 接口暂不可用，已使用前端模拟数据`, error.message)
    return fallback
  }
}

export async function safePost(url, payload, fallback = { ok: true }) {
  try {
    const { data } = await http.post(url, payload)
    return data
  } catch (error) {
    console.warn(`[NightSight] ${url} 接口暂不可用，已使用前端模拟响应`, error.message)
    return fallback
  }
}

export default http
