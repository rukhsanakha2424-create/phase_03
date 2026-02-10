'use client';

import { useState, useEffect } from 'react';
import { Card } from '../../components/common/Card';
import { Button } from '../../components/common/Button';
import { AgentIndicator } from '../../components/common/AgentIndicator';
import { Bot, Plus, Settings, Play, Pause, Trash2 } from 'lucide-react';
import { apiClient } from '@/lib/api/client';

interface Agent {
  id: string;
  name: string;
  description: string;
  status: 'active' | 'inactive' | 'paused';
  lastActivity: string;
  capabilities: string[];
  version: string;
}

interface BackendAgent {
  id: string;
  name: string;
  version: string;
  status: string; // 'online' or 'offline'
  last_activity: string;
  capabilities: string[];
}

export default function AgentsPage() {
  const [agents, setAgents] = useState<Agent[]>([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  const [newAgent, setNewAgent] = useState({
    name: '',
    version: '',
    description: '',
    tags: ''
  });

  useEffect(() => {
    const fetchAgents = async () => {
      try {
        const backendAgents: BackendAgent[] = await apiClient.get('/api/v1/agents');

        // Transform backend data to frontend format
        const transformedAgents: Agent[] = backendAgents.map(agent => ({
          id: agent.id.toString(),
          name: agent.name,
          description: `AI agent for ${agent.name.toLowerCase()}`, // Generate a description
          status: agent.status === 'online' ? 'active' : 'inactive',
          lastActivity: agent.last_activity,
          capabilities: agent.capabilities,
          version: agent.version
        }));

        setAgents(transformedAgents);
      } catch (error) {
        console.error('Error fetching agents:', error);
        // Fallback to mock data if API fails
        setAgents([
          {
            id: '1',
            name: 'Task Automation Agent',
            description: 'Automates routine task assignments and scheduling',
            status: 'active',
            lastActivity: new Date().toISOString(),
            capabilities: ['Scheduling', 'Notifications', 'Analytics'],
            version: '1.2.0'
          },
          {
            id: '2',
            name: 'Priority Manager',
            description: 'Manages task priorities based on deadlines and importance',
            status: 'active',
            lastActivity: new Date().toISOString(),
            capabilities: ['Prioritization', 'Analysis', 'Recommendations'],
            version: '1.1.5'
          },
          {
            id: '3',
            name: 'Team Coordinator',
            description: 'Coordinates team tasks and manages collaboration',
            status: 'inactive',
            lastActivity: new Date().toISOString(),
            capabilities: ['Coordination', 'Communication', 'Reporting'],
            version: '1.0.8'
          }
        ]);
      } finally {
        setLoading(false);
      }
    };

    fetchAgents();
  }, []);

  const toggleAgentStatus = (id: string) => {
    setAgents(prev => prev.map(agent =>
      agent.id === id
        ? {
            ...agent,
            status: agent.status === 'active' ? 'inactive' : 'active',
            lastActivity: new Date().toISOString()
          }
        : agent
    ));
  };

  const deleteAgent = (id: string) => {
    setAgents(prev => prev.filter(agent => agent.id !== id));
  };

  const handleNewAgentChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setNewAgent(prev => ({ ...prev, [name]: value }));
  };

  const handleCreateAgent = (e: React.FormEvent) => {
    e.preventDefault();
    
    // Create new agent object
    const agentToAdd: Agent = {
      id: `agent-${Date.now()}`,
      name: newAgent.name,
      description: newAgent.description,
      status: 'active',
      lastActivity: new Date().toISOString(),
      capabilities: newAgent.tags.split(',').map(tag => tag.trim()).filter(tag => tag),
      version: newAgent.version
    };
    
    // Add to the list
    setAgents(prev => [...prev, agentToAdd]);
    
    // Reset form and close modal
    setNewAgent({ name: '', version: '', description: '', tags: '' });
    setShowModal(false);
  };

  if (loading) {
    return (
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="animate-pulse">
          <div className="h-8 bg-gray-200 rounded w-1/4 mb-8"></div>
          {[1, 2, 3].map(i => (
            <div key={i} className="h-32 bg-gray-200 rounded-lg mb-6"></div>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-8">
        <div>
          <h1 className="text-2xl font-bold text-slate">AI Agents</h1>
          <p className="text-slate-light mt-1">
            Manage and monitor your AI-powered automation agents
          </p>
        </div>
        
        <div className="flex items-center gap-3">
          <AgentIndicator />
          <Button 
            className="flex items-center gap-2"
            onClick={() => setShowModal(true)}
          >
            <Plus size={16} />
            New Agent
          </Button>
        </div>
      </div>

      {agents.length === 0 ? (
        <Card className="text-center py-12">
          <Bot className="mx-auto h-12 w-12 text-slate-light" />
          <h3 className="mt-4 text-lg font-medium text-slate">No agents yet</h3>
          <p className="mt-2 text-slate-light">
            Get started by creating your first AI agent to automate tasks.
          </p>
          <Button className="mt-6 mx-auto w-fit">
            <Plus size={16} />
            Create Agent
          </Button>
        </Card>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {agents.map((agent) => (
            <Card key={agent.id} className="overflow-hidden">
              <div className="p-5">
                <div className="flex items-start justify-between">
                  <div className="flex items-center gap-3">
                    <div className={`p-2 rounded-lg ${
                      agent.status === 'active' 
                        ? 'bg-green-500/10 text-green-500' 
                        : agent.status === 'paused'
                          ? 'bg-yellow-500/10 text-yellow-500'
                          : 'bg-slate-light/10 text-slate-light'
                    }`}>
                      <Bot size={20} />
                    </div>
                    <div>
                      <h3 className="font-semibold text-slate">{agent.name}</h3>
                      <p className="text-xs text-slate-light">{agent.version}</p>
                    </div>
                  </div>
                  
                  <div className={`px-2 py-1 rounded-full text-xs font-medium ${
                    agent.status === 'active' 
                      ? 'bg-green-500/10 text-green-600' 
                      : agent.status === 'paused'
                        ? 'bg-yellow-500/10 text-yellow-600'
                        : 'bg-slate-light/10 text-slate-light'
                  }`}>
                    {agent.status.charAt(0).toUpperCase() + agent.status.slice(1)}
                  </div>
                </div>
                
                <p className="mt-3 text-sm text-slate-light">{agent.description}</p>
                
                <div className="mt-4 pt-4 border-t border-slate-200">
                  <div className="flex flex-wrap gap-2">
                    {agent.capabilities.slice(0, 3).map((cap, idx) => (
                      <span 
                        key={idx} 
                        className="px-2 py-1 text-xs rounded-md bg-organify-primary/10 text-organify-primary"
                      >
                        {cap}
                      </span>
                    ))}
                    {agent.capabilities.length > 3 && (
                      <span className="px-2 py-1 text-xs rounded-md bg-slate-100 text-slate-light">
                        +{agent.capabilities.length - 3} more
                      </span>
                    )}
                  </div>
                </div>
              </div>
              
              <div className="bg-slate-50 px-5 py-3 flex justify-between items-center">
                <span className="text-xs text-slate-light">
                  Last activity: {new Date(agent.lastActivity).toLocaleDateString()} {new Date(agent.lastActivity).toLocaleTimeString()}
                </span>
                
                <div className="flex items-center gap-2">
                  <Button
                    variant="secondary"
                    size="sm"
                    onClick={() => toggleAgentStatus(agent.id)}
                    className="p-2"
                  >
                    {agent.status === 'active' ? <Pause size={16} /> : <Play size={16} />}
                  </Button>
                  
                  <Button
                    variant="secondary"
                    size="sm"
                    className="p-2 text-slate-light hover:text-red-500"
                  >
                    <Settings size={16} />
                  </Button>
                  
                  <Button
                    variant="secondary"
                    size="sm"
                    onClick={() => deleteAgent(agent.id)}
                    className="p-2 text-slate-light hover:text-red-500"
                  >
                    <Trash2 size={16} />
                  </Button>
                </div>
              </div>
            </Card>
          ))}
        </div>
      )}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md mx-4">
            <h2 className="text-xl font-bold mb-4">Create New Agent</h2>
            
            <form onSubmit={handleCreateAgent}>
              <div className="mb-4">
                <label className="block text-sm font-medium mb-1">Agent Name</label>
                <input
                  type="text"
                  name="name"
                  value={newAgent.name}
                  onChange={handleNewAgentChange}
                  className="w-full p-2 border rounded"
                  required
                />
              </div>
              
              <div className="mb-4">
                <label className="block text-sm font-medium mb-1">Version</label>
                <input
                  type="text"
                  name="version"
                  value={newAgent.version}
                  onChange={handleNewAgentChange}
                  className="w-full p-2 border rounded"
                  required
                />
              </div>
              
              <div className="mb-4">
                <label className="block text-sm font-medium mb-1">Description</label>
                <textarea
                  name="description"
                  value={newAgent.description}
                  onChange={handleNewAgentChange}
                  className="w-full p-2 border rounded"
                  rows={3}
                  required
                />
              </div>
              
              <div className="mb-4">
                <label className="block text-sm font-medium mb-1">Tags (comma separated)</label>
                <input
                  type="text"
                  name="tags"
                  value={newAgent.tags}
                  onChange={handleNewAgentChange}
                  className="w-full p-2 border rounded"
                  placeholder="e.g., scheduling, notifications, analytics"
                />
              </div>
              
              <div className="flex justify-end gap-2">
                <Button
                  type="button"
                  variant="secondary"
                  onClick={() => setShowModal(false)}
                >
                  Cancel
                </Button>
                <Button
                  type="submit"
                  variant="primary"
                >
                  Create Agent
                </Button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}