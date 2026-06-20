import { safeGet, safePost } from './http'
import { mockDevices, mockEvents, mockStats, mockTimeline } from './mockData'

export const fetchEvents = () => safeGet('/events/recent', mockEvents)
export const fetchDevices = () => safeGet('/devices/status', mockDevices)
export const fetchStats = () => safeGet('/dashboard/stats', mockStats)
export const fetchTimeline = () => safeGet('/events/timeline', mockTimeline)
export const sendControlAction = (payload) => safePost('/control/action', payload)
