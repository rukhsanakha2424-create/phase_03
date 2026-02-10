'use client'

/**
 * AgentSelect Component
 * Dropdown for selecting an AI agent to assign to a task
 */

import { useState, useEffect } from 'react'
import { apiClient } from '@/lib/api/client'

interface Agent {
  id: string
  name: string
  status: string
  version: string
}

interface AgentSelectProps {
  value?: string
  onChange: (agentId: string | null) => void
  label?: string
  className?: string
  disabled?: boolean
}

export function AgentSelect({ value, onChange, label = "Assign to Agent", className, disabled = false }: AgentSelectProps) {
  const [agents, setAgents] = useState<Agent[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchAgents = async () => {
      try {
        setLoading(true)
        const response: any[] = await apiClient.get('/api/v1/agents')
        
        // Transform backend data to match our interface
        const transformedAgents: Agent[] = response.map(agent => ({
          id: agent.id.toString(),
          name: agent.name,
          status: agent.status,
          version: agent.version
        }))
        
        setAgents(transformedAgents)
      } catch (err) {
        console.error('Error fetching agents:', err)
        setError('Failed to load agents')
      } finally {
        setLoading(false)
      }
    }

    fetchAgents()
  }, [])

  const handleSelect = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const selectedValue = e.target.value
    if (selectedValue === 'none') {
      onChange(null)
    } else {
      onChange(selectedValue)
    }
  }

  return (
    <div className={className}>
      <label className="block text-sm font-medium text-slate-light mb-1">
        {label}
      </label>
      
      {loading ? (
        <div className="w-full h-10 bg-slate-100 rounded-md animate-pulse"></div>
      ) : error ? (
        <div className="text-sm text-error">{error}</div>
      ) : (
        <select
          value={value || 'none'}
          onChange={handleSelect}
          disabled={disabled || loading}
          className={`
            w-full px-4 py-2 border rounded-lg
            focus:outline-none focus:ring-2 focus:ring-organify-primary focus:border-transparent
            transition-colors
            ${disabled ? 'bg-slate-100 text-slate-400 cursor-not-allowed' : ''}
          `}
        >
          <option value="none">No agent</option>
          {agents.map((agent) => (
            <option key={agent.id} value={agent.id}>
              {agent.name} ({agent.version})
            </option>
          ))}
        </select>
      )}
    </div>
  )
}